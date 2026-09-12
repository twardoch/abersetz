# this_file: src/abersetz/providers/gguf.py

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..config import EngineConfig
from ..retrieval import reference_context
from .base import EngineBase, EngineError, EngineRequest, EngineResult
from .hymt2 import build_hymt2_prompt, hymt2_messages, hymt2_sampling
from .local_models import resolve_and_download_model
from .madlad import (
    MADLAD_CHUNK_SIZE,
    MADLAD_MAX_CONTEXT,
    MADLAD_MAX_TOKENS,
    MADLAD_TEMPERATURE,
    build_madlad_prompt,
    t5_generate,
)
from .salamandra import SALAMANDRA_MAX_TOKENS, SALAMANDRA_TEMPERATURE, build_salamandra_prompt
from .translategemma import (
    TRANSLATEGEMMA_MAX_TOKENS,
    TRANSLATEGEMMA_TEMPERATURE,
    clean_translategemma_output,
    translategemma_messages,
)

#: llama.cpp context window used when neither CLI nor config sets ``n_ctx``.
DEFAULT_N_CTX = 4096

#: Per-family decoding defaults: (max_tokens, temperature).
_FAMILY_DEFAULTS: dict[str, tuple[int, float]] = {
    "gemma": (TRANSLATEGEMMA_MAX_TOKENS, TRANSLATEGEMMA_TEMPERATURE),
    "salamandra": (SALAMANDRA_MAX_TOKENS, SALAMANDRA_TEMPERATURE),
    "madlad": (MADLAD_MAX_TOKENS, MADLAD_TEMPERATURE),
}

SUPPORTED_FAMILIES = ("mthy", "gemma", "salamandra", "madlad")


class LocalGgufEngine(EngineBase):
    """Local translation engine using GGUF models via ``llama-cpp-python``.

    Loads a ``.gguf`` quantised model file and runs inference locally using
    llama.cpp.  Works on any platform (macOS, Linux, Windows) and does not
    require Apple Silicon.

    Supported model families (``gg/<family>::<alias|repo[:QUANT]|path>``; the
    family is inferred from the model name when the subvariant is omitted):
    * **mthy** — Tencent Hy-MT2 (official ``tencent/*-GGUF`` repos and community
      quants). Official English instruction, Tencent's recommended sampler.
    * **gemma** — Google TranslateGemma. Model chat template with
      ``source_lang_code``/``target_lang_code``, greedy decoding.
    * **salamandra** — BSC-LT SalamandraTA-7b-instruct. Model-card prompts
      (plain / glossary / markup-preserving), greedy decoding.
    * **madlad** — Google MADLAD-400 (T5). ``<2xx>`` target token, greedy
      encoder-decoder loop through llama.cpp's low-level API; 512-token encoder.

    **Cost**: Free — inference runs locally.
    **Rate limits**: None.  CPU-only speed is roughly 2–10 tokens/second;
      GPU offload (``n_gpu_layers=-1``) is substantially faster.
    **Privacy**: 100 % local — no data leaves the machine.
    **Offline**: Yes — after the model file is downloaded once.
    **Platform**: Any OS with a C++ compiler; install with
      ``pip install abersetz[gguf]``.  CUDA or Metal GPU offload requires
      a matching build of ``llama-cpp-python``.
    **Model size**: Q8_0 quantisation gives good quality at ~8 GB for 7 B models;
      Q4_K_M halves that at a modest quality cost.
    """

    def __init__(
        self,
        family: str,
        config: EngineConfig,
        model_path: str,
        *,
        max_tokens: int | None = None,
        temperature: float | None = None,
        n_gpu_layers: int = -1,
        n_ctx: int | None = None,
        n_threads: int | None = None,
    ) -> None:
        if family not in SUPPORTED_FAMILIES:
            raise EngineError(f"Unsupported GGUF family '{family}'")
        chunk_size, html_chunk_size = config.chunk_size, config.html_chunk_size
        #: Hard ceiling the pipeline must respect even when a larger size is configured.
        self.max_chunk_size: int | None = None
        if family == "madlad":
            chunk_size = min(chunk_size or MADLAD_CHUNK_SIZE, MADLAD_CHUNK_SIZE)
            html_chunk_size = min(html_chunk_size or MADLAD_CHUNK_SIZE, MADLAD_CHUNK_SIZE)
            self.max_chunk_size = MADLAD_CHUNK_SIZE
        super().__init__(config.name, chunk_size, html_chunk_size)
        self._family = family

        resolved_path = resolve_and_download_model(model_path, "gguf")
        self._cache_model_path = resolved_path
        self._model_name = Path(resolved_path).name
        self._sampling = hymt2_sampling(f"{model_path} {resolved_path}")
        if family == "mthy":
            default_tokens, default_temp = self._sampling.max_tokens, self._sampling.temperature
        else:
            default_tokens, default_temp = _FAMILY_DEFAULTS[family]
        self._max_tokens = max_tokens if max_tokens is not None else default_tokens
        self._temperature = temperature if temperature is not None else default_temp
        if n_ctx is None:
            # T5: encoder input (<=512) plus the decoder's own KV cache share ``n_ctx``.
            n_ctx = MADLAD_MAX_CONTEXT + MADLAD_MAX_TOKENS if family == "madlad" else DEFAULT_N_CTX
        try:
            from llama_cpp import Llama
        except Exception as exc:  # pragma: no cover
            raise EngineError("llama-cpp-python is required for GGUF engines") from exc
        self._llm = Llama(
            model_path=resolved_path,
            n_gpu_layers=n_gpu_layers,
            n_ctx=n_ctx,
            n_threads=n_threads,
            verbose=False,
        )

    @property
    def supports_translation_examples(self) -> bool:
        return self._family == "mthy"

    def _completion_kwargs(self) -> dict[str, Any]:
        """Family-specific decoding parameters for ``create_chat_completion``."""
        if self._family != "mthy":
            return {}
        s = self._sampling
        kwargs: dict[str, Any] = {"top_p": s.top_p, "repeat_penalty": s.repetition_penalty}
        if s.top_k > 0:
            kwargs["top_k"] = s.top_k
        return kwargs

    def _messages(self, request: EngineRequest) -> list[dict[str, Any]]:
        if self._family == "mthy":
            prompt = build_hymt2_prompt(
                request.text,
                request.target_lang,
                voc=request.voc,
                preamble=reference_context(request),
            )
            return hymt2_messages(prompt)
        if self._family == "gemma":
            return translategemma_messages(request.source_lang, request.target_lang, request.text)
        if self._family == "salamandra":
            prompt = build_salamandra_prompt(
                request.text,
                request.source_lang,
                request.target_lang,
                voc=request.voc,
                preserve_markup=request.is_html,
            )
            return [{"role": "user", "content": prompt}]
        raise EngineError(f"No chat prompt for GGUF family '{self._family}'")

    def translate(self, request: EngineRequest) -> EngineResult:
        if self._family == "madlad":
            if request.is_html:
                raise EngineError(
                    "MADLAD-400 cannot preserve HTML markup; translate plain text with it or "
                    "pick another engine for HTML"
                )
            prompt = build_madlad_prompt(request.text, request.target_lang)
            text = t5_generate(self._llm, prompt, max_tokens=self._max_tokens)
            return EngineResult(text=text, voc=dict(request.voc))
        output = self._llm.create_chat_completion(
            messages=self._messages(request),
            max_tokens=self._max_tokens,
            temperature=self._temperature,
            **self._completion_kwargs(),
        )
        chunk_result = output["choices"][0]["message"]["content"] or ""
        if self._family == "gemma":
            chunk_result = clean_translategemma_output(chunk_result)
        return EngineResult(text=chunk_result.strip(), voc=dict(request.voc))
