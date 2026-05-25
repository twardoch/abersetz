# this_file: src/abersetz/providers/llm.py

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from typing import Any

from tenacity import retry, stop_after_attempt, wait_exponential

from ..config import EngineConfig
from .base import EngineBase, EngineRequest, EngineResult


class LlmEngine(EngineBase):
    """Shared logic for LLM backed engines."""

    OUTPUT_RE = re.compile(r"<output>(?P<body>.*?)</output>", re.DOTALL | re.IGNORECASE)
    VOCAB_RE = re.compile(r"<voc>(?P<body>.*?)</voc>", re.DOTALL | re.IGNORECASE)

    def __init__(
        self,
        config: EngineConfig,
        client: Any,
        *,
        model: str,
        temperature: float,
        static_prolog: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__(config.name, config.chunk_size, config.html_chunk_size)
        self._client = client
        self._model = model
        self._temperature = temperature
        self._static_prolog = dict(static_prolog or {})

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1), reraise=True)
    def _invoke(self, messages: list[dict[str, str]]) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=self._temperature,
        )
        return response.choices[0].message.content or ""

    def translate(self, request: EngineRequest) -> EngineResult:
        voc = dict(self._static_prolog)
        voc.update(request.prolog)
        merged = dict(request.voc)
        messages = self._build_messages(request, voc, merged)
        raw = self._invoke(messages)
        text, new_vocab = self._parse_payload(raw)
        merged.update(new_vocab)
        return EngineResult(text=text, voc=merged)

    def _build_messages(
        self,
        request: EngineRequest,
        voc: Mapping[str, str],
        merged: Mapping[str, str],
    ) -> list[dict[str, str]]:
        vocab_payload: dict[str, str] = dict(voc)
        if merged:
            vocab_payload.setdefault("__current__", json.dumps(merged, ensure_ascii=False))
        prolog = json.dumps(vocab_payload, ensure_ascii=False) if vocab_payload else "{}"
        meta = {
            "chunk": request.chunk_index + 1,
            "total": request.total_chunks,
            "is_html": str(request.is_html).lower(),
        }
        instructions = (
            "Translate the <segment> into the target language. Respond with "
            '<output>...</output> and optionally <voc>{"new": "value"}</voc>.'
        )
        user_content = (
            f"<instructions>{instructions}</instructions>\n"
            f"<meta>{json.dumps(meta, ensure_ascii=False)}</meta>\n"
            f"<prolog>{prolog}</prolog>\n"
            f"<target>{request.target_lang}</target>\n"
            f"<source>{request.source_lang}</source>\n"
            f"<segment>{request.text}</segment>"
        )
        return [
            {
                "role": "system",
                "content": "You produce deterministic translations strictly in XML tags.",
            },
            {"role": "user", "content": user_content},
        ]

    def _parse_payload(self, payload: str) -> tuple[str, dict[str, str]]:
        text_match = self.OUTPUT_RE.search(payload)
        text = text_match.group("body").strip() if text_match else payload.strip()
        vocab_match = self.VOCAB_RE.search(payload)
        if not vocab_match:
            return text, {}
        try:
            vocab = json.loads(vocab_match.group("body"))
        except json.JSONDecodeError:
            vocab = {}
        if isinstance(vocab, dict):
            return text, {str(k): str(v) for k, v in vocab.items()}
        return text, {}
