# this_file: src/abersetz/providers/deep_translator.py

from __future__ import annotations

from collections.abc import Mapping

from tenacity import retry, stop_after_attempt, wait_exponential

from ..config import EngineConfig
from .base import EngineBase, EngineError, EngineRequest, EngineResult


class DeepTranslatorEngine(EngineBase):
    """Adapter for `deep-translator` providers with retry logic."""

    PROVIDERS: Mapping[str, type] | None = None

    @classmethod
    def _get_providers(cls) -> Mapping[str, type]:
        """Lazy load deep-translator providers."""
        if cls.PROVIDERS is None:
            from deep_translator import (  # type: ignore[import-untyped]
                DeeplTranslator,
                GoogleTranslator,
                LibreTranslator,
                LingueeTranslator,
                MicrosoftTranslator,
                MyMemoryTranslator,
                PapagoTranslator,
            )

            cls.PROVIDERS = {
                "google": GoogleTranslator,
                "deepl": DeeplTranslator,
                "microsoft": MicrosoftTranslator,
                "libre": LibreTranslator,
                "linguee": LingueeTranslator,
                "papago": PapagoTranslator,
                "my_memory": MyMemoryTranslator,
            }
        return cls.PROVIDERS

    def __init__(self, provider: str, config: EngineConfig) -> None:
        super().__init__(config.name, config.chunk_size, config.html_chunk_size)
        providers = self._get_providers()
        if provider not in providers:
            raise EngineError(f"Unsupported deep-translator provider: {provider}")
        self.provider = provider
        self._provider_class = providers[provider]

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10), reraise=True)
    def _translate_with_retry(self, text: str, source_lang: str, target_lang: str) -> str:
        """Internal method with retry logic for network failures."""
        translator = self._provider_class(source=source_lang, target=target_lang)
        return translator.translate(text)

    def translate(self, request: EngineRequest) -> EngineResult:
        text = self._translate_with_retry(request.text, request.source_lang, request.target_lang)
        return EngineResult(text=text, voc=dict(request.voc))
