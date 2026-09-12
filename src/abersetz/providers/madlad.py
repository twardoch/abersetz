# this_file: src/abersetz/providers/madlad.py
"""Google MADLAD-400 (T5 encoder-decoder) support for the ``gg`` engine.

MADLAD is prompted with a target-language token: ``<2de> I live in a big city``.
The GGUF conversions run on llama.cpp, but llama-cpp-python's high-level
``create_completion`` only drives decoder-only models (it never calls
``llama_encode`` and aborts inside ``llama_decode``), so :func:`t5_generate`
performs the encode -> greedy-decode loop through the low-level bindings.
"""

from __future__ import annotations

import ctypes
from typing import Any

from .base import EngineError

#: MADLAD-400 encoder context (``t5.context_length`` in the GGUF header).
MADLAD_MAX_CONTEXT = 512
#: Deterministic decoding, as in the candle / transformers examples.
MADLAD_TEMPERATURE = 0.0
#: Generous ceiling; the decoder stops at ``</s>`` long before this.
MADLAD_MAX_TOKENS = 512
#: Small chunks: encoder input is capped at 512 tokens.
MADLAD_CHUNK_SIZE = 300

# ``<2xx>`` target tokens present in the MADLAD-400 vocabulary (script/region
# variants use underscores, e.g. ``zh_Hant``, ``fr_CA``).
_MADLAD_CODES = frozenset(
    """
abt ace ace_Arab acf ada adh ady af agr ahk ak akb alt alz am amu an ang ann ape ar arn ary arz
as av awa ay az az_RU ba ban bar bas bbc bci be ber ber_Latn bew bg bg_Latn bgp bho bi bik bim
bjn bjn_Arab bm bn bn_Latn bo bqc br bru brx bs bts btx bua bug bum bus bzj ca cab cac cak cbk
cce ce ceb cfm ch chk chm chr ckb cnh co cr_Latn crh crh_Latn crs cs ctd_Latn ctu cuk cv cy da
de din dje djk dln doi dov dtp dv dwr dyu dz ee el el_Latn emp en enq eo es et eu fa ff ffm fi
fil fip fj fo fon fr fr_CA frp fur fuv fy ga gag gbm gd gl gn gof gom gom_Latn gor grc gsw gu
gu_Latn gub guc guh gui gv gvl gym ha haw he hi hi_Latn hif hil hmn hne ho hr ht hu hui hus hvn
hy iba ibb id ify ig ilo inb io is iso it iu ium izz ja jac jam jiv jv jvn ka kaa kaa_Latn kac
kbd kbp kek kg kha kj kjg kjh kk kl km kmb kmz_Latn kn kn_Latn knj ko koi kos kr kr_Arab krc kri
ks ks_Deva ksd ksw ktu ku kum kv kw kwi ky la laj lb lg lhu li lij lmo ln lo lrc lt ltg lu lus
lv mad mag mai mak mam mas mass maz mbt mdf meo meu mfe mg mgh mh mi min miq mk mkn ml ml_Latn
mn mni mps mqy mr mrj mrw ms ms_Arab ms_Arab_BN msb msi msm mt mwl my myv nan_Latn_TW ndc_ZW nds
nds_NL ne new ngu nhe nia nij niq nl nn nnb no noa nog nr nso nus nut nv ny nyu nzi oc oj om or
os otq pa pag pap pau pck pis pl pon ppk prs ps pt qu qub quc quf quh qup quy qvc qvi qvz qxr
raj rcf rki rm rmc rn ro rom ru ru_Latn rw rwo sa sah sat_Latn sc scn sd sda se seh sg sh shn
shp si sja sk skr sl sm smt sn so spp sq sr srm srn ss st stq su sus suz sv sw sxn syr szl ta
ta_Latn tab taj taq taq_Tfng tbz tca tcy tdx te te_Latn teo tet tg th ti tiv tk tks tlh tll
tly_IR tn to toj tr trp ts tsc tsg tt tuc tvl twu tyv tyz tzh tzj tzm tzo ubu udm ug uk ur uz ve
vec vi wa wal war wo wuu xal xh yap yi yo yua zap zh zh_Hant zh_Latn zne zu zza
""".split()  # noqa: SIM905  (compact vocabulary list)
)

_ALIASES = {
    "zh-hant": "zh_Hant",
    "zh-tw": "zh_Hant",
    "zh-hk": "zh_Hant",
    "zh-hans": "zh",
    "zh-cn": "zh",
    "fr-ca": "fr_CA",
    "nb": "no",
    "iw": "he",
    "in": "id",
    "tl": "fil",
    "jw": "jv",
}

_CODES_LOWER = {code.lower(): code for code in _MADLAD_CODES}


def is_madlad_model(model_name: str | None) -> bool:
    """Heuristic: does a model id / path / file name denote MADLAD-400?"""
    return model_name is not None and "madlad" in model_name.lower()


def madlad_language_token(code: str) -> str:
    """Map a language code to MADLAD's ``<2xx>`` target token."""
    key = code.strip().lower().replace("_", "-")
    key = _ALIASES.get(key, key).lower()
    resolved = _CODES_LOWER.get(key.replace("-", "_"))
    if resolved is None and "-" in key:
        resolved = _CODES_LOWER.get(key.split("-", 1)[0])
    if resolved is None:
        raise EngineError(f"Unsupported MADLAD-400 language: {code}")
    return f"<2{resolved}>"


def build_madlad_prompt(source_text: str, target_lang: str) -> str:
    """``<2de> text`` — the only instruction MADLAD understands."""
    return f"{madlad_language_token(target_lang)} {source_text.strip()}"


def t5_generate(llm: Any, prompt: str, max_tokens: int = MADLAD_MAX_TOKENS) -> str:
    """Greedy encoder-decoder generation on a loaded ``llama_cpp.Llama`` instance.

    Runs ``llama_encode`` on the prompt, then feeds the decoder start token and
    greedily picks the arg-max token until end-of-generation."""
    import llama_cpp
    import numpy as np

    ctx = llm.ctx
    model = llm.model
    vocab = llama_cpp.llama_model_get_vocab(model)
    llm.reset()
    llama_cpp.llama_memory_clear(llama_cpp.llama_get_memory(ctx), True)

    tokens = llm.tokenize(prompt.encode("utf-8"), add_bos=False, special=True)
    if len(tokens) > MADLAD_MAX_CONTEXT:
        raise EngineError(
            f"MADLAD input of {len(tokens)} tokens exceeds the {MADLAD_MAX_CONTEXT}-token "
            "encoder window; lower chunk_size."
        )
    enc_tokens = (llama_cpp.llama_token * len(tokens))(*tokens)
    if llama_cpp.llama_encode(ctx, llama_cpp.llama_batch_get_one(enc_tokens, len(tokens))) != 0:
        raise EngineError("llama_encode failed on MADLAD input")

    start = llama_cpp.llama_model_decoder_start_token(model)
    if start == -1:
        start = llama_cpp.llama_vocab_bos(vocab)
    n_vocab = llama_cpp.llama_vocab_n_tokens(vocab)

    out: list[int] = []
    current = int(start)
    for _ in range(max_tokens):
        step = (llama_cpp.llama_token * 1)(current)
        if llama_cpp.llama_decode(ctx, llama_cpp.llama_batch_get_one(step, 1)) != 0:
            raise EngineError("llama_decode failed while generating MADLAD output")
        logits_ptr = llama_cpp.llama_get_logits_ith(ctx, -1)
        logits = np.ctypeslib.as_array(
            ctypes.cast(logits_ptr, ctypes.POINTER(ctypes.c_float)), shape=(n_vocab,)
        )
        current = int(logits.argmax())
        if llama_cpp.llama_vocab_is_eog(vocab, current):
            break
        out.append(current)
    return llm.detokenize(out).decode("utf-8", "replace").strip()


__all__ = [
    "MADLAD_CHUNK_SIZE",
    "MADLAD_MAX_CONTEXT",
    "MADLAD_MAX_TOKENS",
    "MADLAD_TEMPERATURE",
    "build_madlad_prompt",
    "is_madlad_model",
    "madlad_language_token",
    "t5_generate",
]
