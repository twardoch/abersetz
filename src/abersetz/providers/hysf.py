# this_file: src/abersetz/providers/hysf.py

from __future__ import annotations

from typing import Any

from tenacity import retry, stop_after_attempt, wait_exponential

from ..config import EngineConfig
from ..engine_catalog import HYSF_DEFAULT_MODEL, HYSF_DEFAULT_TEMPERATURE
from .base import EngineBase, EngineRequest, EngineResult


class HysfEngine(EngineBase):
    """Specialised HYSF engine with fixed prompt semantics."""

    MODEL = HYSF_DEFAULT_MODEL
    TEMPERATURE = HYSF_DEFAULT_TEMPERATURE

    def __init__(self, config: EngineConfig, client: Any) -> None:
        super().__init__(config.name, config.chunk_size, config.html_chunk_size)
        self._client = client

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1), reraise=True)
    def _invoke(self, message: str) -> str:
        response = self._client.chat.completions.create(
            model=self.MODEL,
            messages=[{"role": "user", "content": message}],
            temperature=self.TEMPERATURE,
        )
        return response.choices[0].message.content or ""

    def translate(self, request: EngineRequest) -> EngineResult:
        language_name = self._language_name(request.target_lang)
        prompt = (
            f"Translate the following segment into {language_name}, without additional explanation.\n\n"
            f"{request.text}"
        )
        text = self._invoke(prompt).strip()
        return EngineResult(text=text, voc=dict(request.voc))

    @staticmethod
    def _language_name(code: str) -> str:
        try:
            from langcodes import get as get_language  # Lazy import

            return get_language(code).language_name("en") or code
        except Exception:  # pragma: no cover
            return code
