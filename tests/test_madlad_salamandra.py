# this_file: tests/test_madlad_salamandra.py
"""MADLAD-400 and SalamandraTA support (issue 202), offline."""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from abersetz import config as config_module
from abersetz.engines import create_engine
from abersetz.providers import madlad as madlad_mod
from abersetz.providers.base import EngineError, EngineRequest
from abersetz.providers.local_models import ALIASES, KNOWN_MAPPING, family_for_model
from abersetz.providers.madlad import build_madlad_prompt, madlad_language_token
from abersetz.providers.salamandra import build_salamandra_prompt, salamandra_language_name


def _request(text="Hello", *, source="en", target="pl", voc=None, html=False) -> EngineRequest:
    return EngineRequest(
        text=text,
        source_lang=source,
        target_lang=target,
        is_html=html,
        voc=voc or {},
        prolog={},
        chunk_index=0,
        total_chunks=1,
    )


# --- MADLAD prompt ----------------------------------------------------------


@pytest.mark.parametrize(
    ("code", "token"),
    [
        ("de", "<2de>"),
        ("PL", "<2pl>"),
        ("zh", "<2zh>"),
        ("zh-Hant", "<2zh_Hant>"),
        ("zh_TW", "<2zh_Hant>"),
        ("fr-CA", "<2fr_CA>"),
        ("pt-BR", "<2pt>"),
        ("nb", "<2no>"),
        ("tl", "<2fil>"),
    ],
)
def test_madlad_language_token(code: str, token: str) -> None:
    assert madlad_language_token(code) == token


def test_madlad_language_token_when_unknown_then_engine_error() -> None:
    with pytest.raises(EngineError, match="Unsupported MADLAD-400 language"):
        madlad_language_token("xx-QQ")


def test_build_madlad_prompt() -> None:
    assert build_madlad_prompt("  I live in a big city. ", "de") == "<2de> I live in a big city."


# --- Salamandra prompt ------------------------------------------------------


def test_salamandra_language_name() -> None:
    assert salamandra_language_name("ca") == "Catalan"
    assert salamandra_language_name("nb") == "Norwegian Bokmål"
    assert salamandra_language_name("pt-BR") == "Portuguese"
    assert salamandra_language_name("ja") == "Japanese"


def test_build_salamandra_prompt_plain() -> None:
    assert build_salamandra_prompt("Hola", "es", "ca") == (
        "Translate the following text from Spanish into Catalan.\nSpanish: Hola\nCatalan:"
    )


def test_build_salamandra_prompt_when_auto_source_then_english() -> None:
    assert build_salamandra_prompt("Hi", "auto", "de").startswith(
        "Translate the following text from English into German."
    )


def test_build_salamandra_prompt_when_glossary_then_terminology_template() -> None:
    prompt = build_salamandra_prompt(
        "Kerning", "en", "pl", voc={"kerning": "kerning", "font": "font"}
    )
    assert prompt.startswith(
        "Please translate the following English text to Polish while respecting"
    )
    assert "Required Terminology:\n\n- font -> font\n- kerning -> kerning\n\n" in prompt
    assert prompt.endswith("Source Text:\n\nKerning")


def test_build_salamandra_prompt_when_markup_then_preserving_template() -> None:
    prompt = build_salamandra_prompt("<b>Hi</b>", "en", "fr", preserve_markup=True)
    assert prompt.startswith("Translate this English text into French. Preserve any formatting")
    assert prompt.endswith("human-readable parts: <b>Hi</b>")


# --- catalog ----------------------------------------------------------------


def test_catalog_has_issue_202_models() -> None:
    assert ALIASES["madlad-10b"] == "thirteenbit/madlad400-10b-mt-gguf"
    assert KNOWN_MAPPING["thirteenbit/madlad400-10b-mt-gguf"]["filename"] == "model-q8_0.gguf"
    assert ALIASES["salamandra-7b"] == "mradermacher/salamandraTA-7b-instruct-GGUF"
    assert family_for_model("madlad-10b") == "madlad"
    assert family_for_model("/x/salamandraTA-7b-instruct.Q4_K_M.gguf") == "salamandra"


# --- gg engine ----------------------------------------------------------------


def _install_fake_llama(monkeypatch: pytest.MonkeyPatch, captured: dict[str, object]) -> None:
    class FakeLlama:
        def __init__(self, **kwargs):
            captured["init"] = kwargs

        def create_chat_completion(self, **kwargs):
            captured["call"] = kwargs
            return {"choices": [{"message": {"content": " out "}}]}

    monkeypatch.setitem(sys.modules, "llama_cpp", SimpleNamespace(Llama=FakeLlama))


def test_gg_madlad_when_inferred_then_t5_loop_and_small_context(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    model = tmp_path / "madlad400-10b-mt" / "model-q8_0.gguf"
    model.parent.mkdir()
    model.write_text("stub")
    captured: dict[str, object] = {}
    _install_fake_llama(monkeypatch, captured)

    def fake_t5(llm, prompt, max_tokens):
        captured["t5"] = (prompt, max_tokens)
        return "Ich lebe in einer Großstadt."

    monkeypatch.setattr("abersetz.providers.gguf.t5_generate", fake_t5)

    engine = create_engine(f"gg::{model}", config_module.load_config())
    assert engine._family == "madlad"
    assert captured["init"]["n_ctx"] == 1024, "encoder window + decoder cache"
    assert engine.max_chunk_size == madlad_mod.MADLAD_CHUNK_SIZE
    assert engine.chunk_size == madlad_mod.MADLAD_CHUNK_SIZE
    result = engine.translate(_request("I live in a big city.", target="de"))
    assert result.text == "Ich lebe in einer Großstadt."
    assert captured["t5"] == ("<2de> I live in a big city.", 512)
    assert "call" not in captured, "chat completion must not be used for T5"


def test_gg_salamandra_when_inferred_then_chat_prompt_and_greedy(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    model = tmp_path / "salamandraTA-7b-instruct.Q8_0.gguf"
    model.write_text("stub")
    captured: dict[str, object] = {}
    _install_fake_llama(monkeypatch, captured)

    engine = create_engine(f"gg::{model}", config_module.load_config())
    assert engine._family == "salamandra"
    assert captured["init"]["n_ctx"] == 4096
    result = engine.translate(_request("Hola", source="es", target="ca"))
    assert result.text == "out"
    call = captured["call"]
    assert call["temperature"] == 0.0
    assert call["max_tokens"] == 1000
    assert call["messages"] == [
        {
            "role": "user",
            "content": "Translate the following text from Spanish into Catalan.\nSpanish: Hola\nCatalan:",
        }
    ]


def test_gg_salamandra_when_html_then_markup_prompt(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    model = tmp_path / "salamandraTA-7b-instruct.Q8_0.gguf"
    model.write_text("stub")
    captured: dict[str, object] = {}
    _install_fake_llama(monkeypatch, captured)
    engine = create_engine(f"gg/salamandra::{model}", config_module.load_config())
    engine.translate(_request("<p>Hi</p>", html=True))
    assert captured["call"]["messages"][0]["content"].startswith(
        "Translate this English text into Polish. Preserve"
    )


def test_gg_unknown_family_raises(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    model = tmp_path / "x.gguf"
    model.write_text("stub")
    _install_fake_llama(monkeypatch, {})
    with pytest.raises(EngineError, match="Unsupported GGUF family"):
        create_engine(f"gg/qwen::{model}", config_module.load_config())


# --- lm / ll routing -----------------------------------------------------------


def test_lm_madlad_raises_helpful_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(
        sys.modules,
        "lmstudio",
        SimpleNamespace(configure_default_client=lambda _: None, llm=lambda n: object()),
    )
    monkeypatch.setattr("shutil.which", lambda _: None)
    with pytest.raises(EngineError, match="gg::madlad-10b"):
        create_engine("lm::madlad400-10b-mt", config_module.load_config())


def test_lm_salamandra_prompt_and_config(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    class Model:
        def respond(self, prompt, config=None):
            captured["prompt"], captured["config"] = prompt, config
            return "ok"

    monkeypatch.setitem(
        sys.modules,
        "lmstudio",
        SimpleNamespace(configure_default_client=lambda _: None, llm=lambda n: Model()),
    )
    monkeypatch.setattr("shutil.which", lambda _: None)
    engine = create_engine("lm::salamandrata-7b-instruct", config_module.load_config())
    engine.translate(_request("Hola", source="es", target="ca"))
    assert str(captured["prompt"]).startswith(
        "Translate the following text from Spanish into Catalan."
    )
    assert captured["config"] == {"temperature": 0.0, "maxTokens": 1000}


def test_ll_salamandra_family(monkeypatch: pytest.MonkeyPatch) -> None:
    from tests.test_llm_families import FakeClient

    monkeypatch.setenv("OPENAI_API_KEY", "k")
    client = FakeClient("Hola")
    engine = create_engine(
        "ll::http://localhost:8080/v1:salamandraTA-7b-instruct",
        config_module.load_config(),
        client=client,
    )
    result = engine.translate(_request("Hello", source="en", target="es"))
    assert result.text == "Hola"
    call = client.calls[0]
    assert call["temperature"] == 0.0
    assert call["max_tokens"] == 1000
    assert call["messages"][0]["content"].startswith(
        "Translate the following text from English into Spanish."
    )


# --- review follow-ups -----------------------------------------------------------


def test_t5_generate_with_fake_llama_cpp(monkeypatch: pytest.MonkeyPatch) -> None:
    """Encode once, then greedy-decode until an end-of-generation token."""
    import numpy as np

    calls: list[str] = []
    logit_rows = iter([[0.0, 0.0, 5.0, 0.0], [0.0, 0.0, 0.0, 7.0], [9.0, 0.0, 0.0, 0.0]])
    current = {"logits": None}

    def decode(ctx, batch):
        current["logits"] = np.array(next(logit_rows), dtype=np.float32)
        calls.append("decode")
        return 0

    fake = SimpleNamespace(
        llama_token=__import__("ctypes").c_int32,
        llama_model_get_vocab=lambda m: "vocab",
        llama_memory_clear=lambda mem, data: calls.append("clear"),
        llama_get_memory=lambda ctx: "mem",
        llama_batch_get_one=lambda toks, n: ("batch", n),
        llama_encode=lambda ctx, batch: calls.append(f"encode:{batch[1]}") or 0,
        llama_model_decoder_start_token=lambda m: 0,
        llama_vocab_bos=lambda v: 0,
        llama_vocab_n_tokens=lambda v: 4,
        llama_decode=decode,
        llama_get_logits_ith=lambda ctx, i: current["logits"].ctypes.data,
        llama_vocab_is_eog=lambda v, tok: tok == 0,
    )
    monkeypatch.setitem(sys.modules, "llama_cpp", fake)

    class FakeLlm:
        ctx = "ctx"
        model = "model"

        def reset(self):
            calls.append("reset")

        def tokenize(self, text, add_bos, special):
            return [1, 2, 3]

        def detokenize(self, tokens):
            return "|".join(map(str, tokens)).encode()

    assert madlad_mod.t5_generate(FakeLlm(), "<2de> hi", max_tokens=10) == "2|3"
    assert calls == ["reset", "clear", "encode:3", "decode", "decode", "decode"]


def test_pipeline_chunk_size_respects_engine_ceiling() -> None:
    from abersetz.chunking import TextFormat
    from abersetz.pipeline import TranslatorOptions, _select_chunk_size

    engine = SimpleNamespace(chunk_size_for=lambda fmt: None, max_chunk_size=300)
    cfg = config_module.load_config()
    assert (
        _select_chunk_size(TextFormat.PLAIN, engine, TranslatorOptions(chunk_size=1200), cfg) == 300
    )
    assert (
        _select_chunk_size(TextFormat.HTML, engine, TranslatorOptions(html_chunk_size=1800), cfg)
        == 300
    )


def test_gg_madlad_rejects_html(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    model = tmp_path / "madlad400-10b-mt.q8_0.gguf"
    model.write_text("stub")
    _install_fake_llama(monkeypatch, {})
    engine = create_engine(f"gg::{model}", config_module.load_config())
    with pytest.raises(EngineError, match="HTML"):
        engine.translate(_request("<p>x</p>", html=True))


def test_ll_madlad_subvariant_raises() -> None:
    from abersetz.providers.llm.inference import llm_prompt_family

    with pytest.raises(EngineError, match="gg::madlad-10b"):
        llm_prompt_family("anything", "madlad")


def test_family_for_model_when_plain_gemma_then_none() -> None:
    assert family_for_model("mlx-community/gemma-3-4b-it") is None


def test_resolve_when_alias_quant_suffix_then_split(monkeypatch: pytest.MonkeyPatch) -> None:
    from abersetz.providers import local_models

    monkeypatch.setattr(local_models, "find_local_model_path", lambda *_: None)
    monkeypatch.setattr("huggingface_hub.list_repo_files", lambda repo: ["Hy-MT2-1.8B-Q4_K_M.gguf"])
    monkeypatch.setattr(
        "huggingface_hub.hf_hub_download", lambda repo_id, filename: f"/c/{filename}"
    )
    assert (
        local_models.resolve_and_download_model("1.8b-gguf:Q4_K_M", "gguf")
        == "/c/Hy-MT2-1.8B-Q4_K_M.gguf"
    )


def test_resolve_when_backend_mismatch_then_engine_error(monkeypatch: pytest.MonkeyPatch) -> None:
    from abersetz.providers import local_models

    monkeypatch.setattr(local_models, "find_local_model_path", lambda *_: None)
    with pytest.raises(EngineError, match="use the gg engine"):
        local_models.resolve_and_download_model("tg-4b-gguf", "mlx")


def test_supports_translation_examples_off_for_gemma_and_salamandra(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from tests.test_llm_families import FakeClient

    monkeypatch.setenv("OPENAI_API_KEY", "k")
    cfg = config_module.load_config()
    assert create_engine(
        "ll::openai:gpt-4o-mini", cfg, client=FakeClient("x")
    ).supports_translation_examples
    assert not create_engine(
        "ll/tg::openai:x", cfg, client=FakeClient("x")
    ).supports_translation_examples
    assert not create_engine(
        "ll/salamandra::openai:x", cfg, client=FakeClient("x")
    ).supports_translation_examples
