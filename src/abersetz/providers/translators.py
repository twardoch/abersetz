# this_file: src/abersetz/providers/translators.py

from __future__ import annotations

from tenacity import retry, stop_after_attempt, wait_exponential

from ..config import EngineConfig
from .base import EngineBase, EngineRequest, EngineResult


class TranslatorsEngine(EngineBase):
    """Wrapper around the `translators` package with retry logic."""

    def __init__(self, provider: str, config: EngineConfig) -> None:
        super().__init__(config.name, config.chunk_size, config.html_chunk_size)
        self.provider = provider
        import translators

        self._translators = translators

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10), reraise=True)
    def _translate_with_retry(
        self, text: str, is_html: bool, source_lang: str, target_lang: str
    ) -> str:
        """Internal method with retry logic for network failures."""
        if is_html:
            return self._translators.translate_html(
                text,
                translator=self.provider,
                from_language=source_lang,
                to_language=target_lang,
            )
        else:
            return self._translators.translate_text(
                text,
                translator=self.provider,
                from_language=source_lang,
                to_language=target_lang,
            )

    def translate(self, request: EngineRequest) -> EngineResult:
        text = self._translate_with_retry(
            request.text, request.is_html, request.source_lang, request.target_lang
        )
        return EngineResult(text=text, voc=dict(request.voc))
