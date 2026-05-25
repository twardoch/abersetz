# this_file: src/abersetz/providers/gguf.py

from __future__ import annotations

from typing import Any

from ..config import EngineConfig
from .base import EngineBase, EngineError, EngineRequest, EngineResult
from .mlx import _resolve_mthy_language, build_mthy_prompt, resolve_and_download_model


class LocalGgufEngine(EngineBase):
    """Local GGUF-backed engine for HY-MT and TranslateGemma."""

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
    ) -> None:
        super().__init__(config.name, config.chunk_size, config.html_chunk_size)
        self._family = family
        self._max_tokens = max_tokens
        self._temperature = temperature

        resolved_path = resolve_and_download_model(model_path, "gguf")
        try:
            from llama_cpp import Llama
        except Exception as exc:  # pragma: no cover
            raise EngineError("llama-cpp-python is required for GGUF engines") from exc
        self._llm = Llama(
            model_path=resolved_path,
            n_gpu_layers=n_gpu_layers,
            n_ctx=n_ctx,
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
