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
                PapagoTranslator,
            )

            cls.PROVIDERS = {
                "google": GoogleTranslator,
                "deepl": DeeplTranslator,
                "microsoft": MicrosoftTranslator,
                "libre": LibreTranslator,
                "linguee": LingueeTranslator,
                "papago": PapagoTranslator,
            }
        return cls.PROVIDERS

    def __init__(self, provider: str, config: EngineConfig) -> None:
        super().__init__(config.name, config.chunk_size, config.html_chunk_size)
        providers = self._get_providers()
        if provider not in providers:
            raise EngineError(f"Unsupported deep-translator provider: {provider}")
        self.provider = provider
        self._provider_class = providers[provider]

    def _resolve_lang(self, lang: str) -> str:
        """Safely map standard 2-letter language codes to those supported by the provider."""
        try:
            from deep_translator.constants import (
                DEEPL_LANGUAGE_TO_CODE,
                GOOGLE_LANGUAGES_TO_CODES,
                LIBRE_LANGUAGES_TO_CODES,
                LINGUEE_LANGUAGES_TO_CODES,
                PAPAGO_LANGUAGE_TO_CODE,
            )

            STATIC_LANGUAGES = {
                "google": GOOGLE_LANGUAGES_TO_CODES,
                "deepl": DEEPL_LANGUAGE_TO_CODE,
                "libre": LIBRE_LANGUAGES_TO_CODES,
                "linguee": LINGUEE_LANGUAGES_TO_CODES,
                "papago": PAPAGO_LANGUAGE_TO_CODE,
            }
        except Exception:
            STATIC_LANGUAGES = {}

        langs = STATIC_LANGUAGES.get(self.provider, {})
        if not langs:
            try:
                if hasattr(self._provider_class, "get_supported_languages"):
                    try:
                        inst = self._provider_class(source="auto", target="en")
                        langs = inst.get_supported_languages(as_dict=True)
                    except Exception:
                        try:
                            inst = self._provider_class(source="english", target="polish")
                            langs = inst.get_supported_languages(as_dict=True)
                        except Exception:
                            pass
                if not langs and hasattr(self._provider_class, "_languages"):
                    langs = self._provider_class._languages
            except Exception:
                pass

        if not langs or not isinstance(langs, dict):
            return lang

        # Use langcodes to find the closest supported match
        try:
            import langcodes

            # 1. Resolve canonical code for query
            try:
                canonical = str(langcodes.find(lang))
            except LookupError:
                try:
                    canonical = str(langcodes.Language.get(lang))
                except Exception:
                    canonical = lang

            # 2. Extract supported codes
            supported_codes = [str(c) for c in langs.values() if c]

            # 3. Find closest match
            matched = langcodes.closest_supported_match(canonical, supported_codes)
            if matched:
                return matched
        except Exception:
            pass

        # Fallback to simple matching if langcodes failed
        lang_lower = lang.lower()
        # 1. Exact match in values (case-insensitive)
        for code in langs.values():
            if str(code).lower() == lang_lower:
                return code
        # 2. Case-insensitive key/name match (e.g. 'english')
        for name, code in langs.items():
            if str(name).lower() == lang_lower:
                return code
        # 3. Matches prefix (e.g. 'en' matches 'en-GB' or 'en-US')
        for code in langs.values():
            if str(code).lower().startswith(lang_lower + "-"):
                return code
        return lang

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10), reraise=True)
    def _translate_with_retry(self, text: str, source_lang: str, target_lang: str) -> str:
        """Internal method with retry logic for network failures."""
        resolved_source = self._resolve_lang(source_lang)
        resolved_target = self._resolve_lang(target_lang)
        translator = self._provider_class(source=resolved_source, target=resolved_target)
        return translator.translate(text)

    def translate(self, request: EngineRequest) -> EngineResult:
        text = self._translate_with_retry(request.text, request.source_lang, request.target_lang)
        return EngineResult(text=text, voc=dict(request.voc))
