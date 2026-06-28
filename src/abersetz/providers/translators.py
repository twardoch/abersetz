# this_file: src/abersetz/providers/translators.py

from __future__ import annotations

from tenacity import retry, stop_after_attempt, wait_exponential

from ..config import EngineConfig
from .base import EngineBase, EngineRequest, EngineResult


class TranslatorsEngine(EngineBase):
    """Engine adapter for the ``translators`` package (web-scraping approach).

    The ``translators`` library scrapes the public web endpoints of Google, Bing,
    Yandex, and many other providers.  No API key is required, but the underlying
    services impose undocumented, per-IP rate limits.

    **Cost**: Free.
    **Rate limits**: Unofficial.  Google/Bing typically throttle after roughly
      50–100 requests/minute from a single IP.  Abersetz retries up to 3 times
      with exponential back-off (1 s, 2 s, 4 s … capped at 10 s) before raising.
    **Privacy**: Text is sent to the chosen third-party web service.
    **Offline**: No — requires internet access.
    **Recommended chunk size**: ≤ 1 200 characters to reduce throttle risk.
    """

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
