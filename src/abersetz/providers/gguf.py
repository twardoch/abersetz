# this_file: src/abersetz/providers/gguf.py

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..config import EngineConfig
from .base import EngineBase, EngineError, EngineRequest, EngineResult
from .mlx import _resolve_mthy_language, build_mthy_prompt, resolve_and_download_model


class LocalGgufEngine(EngineBase):
    """Local translation engine using GGUF models via ``llama-cpp-python``.

    Loads a ``.gguf`` quantised model file and runs inference locally using
    llama.cpp.  Works on any platform (macOS, Linux, Windows) and does not
    require Apple Silicon.

    Supported model families:
    * **mthy** — Tencent Hy-MT2 series (GGUF quantised variants).
      Use ``gg/mthy::<model-alias-or-path>`` as the selector.
    * **gemma** — Google Gemma translation variants (GGUF).
      Use ``gg/gemma::<model-alias-or-path>`` as the selector.

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
        max_tokens: int,
        temperature: float,
        n_gpu_layers: int,
        n_ctx: int,
        n_threads: int | None = None,
    ) -> None:
        super().__init__(config.name, config.chunk_size, config.html_chunk_size)
        self._family = family
        self._max_tokens = max_tokens
        self._temperature = temperature

        resolved_path = resolve_and_download_model(model_path, "gguf")
        self._model_name = Path(resolved_path).name
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

    def translate(self, request: EngineRequest) -> EngineResult:
        if self._family == "mthy":
            prompt = build_mthy_prompt(
                source_text=request.text,
                target_language=_resolve_mthy_language(request.target_lang),
                voc=request.voc,
            )
            mthy_messages: list[dict[str, Any]] = [{"role": "user", "content": prompt}]
            chat_messages = mthy_messages
        elif self._family == "gemma":
            source_lang = request.source_lang if request.source_lang != "auto" else "en"
            gemma_messages: list[dict[str, Any]] = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "source_lang_code": source_lang,
                            "target_lang_code": request.target_lang,
                            "text": request.text,
                        }
                    ],
                }
            ]
            chat_messages = gemma_messages
        else:
            raise EngineError(f"Unsupported GGUF family '{self._family}'")
        output = self._llm.create_chat_completion(
            messages=chat_messages,
            max_tokens=self._max_tokens,
            temperature=self._temperature,
        )
        chunk_result = output["choices"][0]["message"]["content"]
        return EngineResult(text=chunk_result, voc=dict(request.voc))
