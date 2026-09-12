# this_file: src/abersetz/providers/salamandra.py
"""Prompt helpers for BSC-LT SalamandraTA-7b-instruct (ChatML translation model).

Templates follow the model card (https://huggingface.co/BSC-LT/salamandraTA-7b-instruct):
languages are written as *English names*, decoding is deterministic (``temperature=0``),
and there are dedicated wordings for glossary-constrained and markup-preserving input.
"""

from __future__ import annotations

from .translategemma import language_display_name

#: Model card recommends deterministic decoding.
SALAMANDRA_TEMPERATURE = 0.0
#: Upper bound the model card uses for document-level tasks.
SALAMANDRA_MAX_TOKENS = 1000
#: Assumed when the caller left source detection to the engine.
SALAMANDRA_DEFAULT_SOURCE = "en"

#: Languages listed on the model card (ISO 639-1/3 codes -> display name override
#: where langcodes would produce a longer form).
SALAMANDRA_LANGUAGES: dict[str, str] = {
    "ar": "Arabic",
    "an": "Aragonese",
    "ast": "Asturian",
    "eu": "Basque",
    "bg": "Bulgarian",
    "ca": "Catalan",
    "zh": "Chinese",
    "hr": "Croatian",
    "cs": "Czech",
    "da": "Danish",
    "nl": "Dutch",
    "en": "English",
    "et": "Estonian",
    "fi": "Finnish",
    "fr": "French",
    "gl": "Galician",
    "de": "German",
    "el": "Greek",
    "hi": "Hindi",
    "hu": "Hungarian",
    "ga": "Irish",
    "it": "Italian",
    "ja": "Japanese",
    "ko": "Korean",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "mt": "Maltese",
    "nb": "Norwegian Bokmål",
    "no": "Norwegian Bokmål",
    "nn": "Norwegian Nynorsk",
    "oc": "Occitan",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "sr": "Serbian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "es": "Spanish",
    "sv": "Swedish",
    "uk": "Ukrainian",
    "cy": "Welsh",
}


def is_salamandra_model(model_name: str | None) -> bool:
    """Heuristic: does a model id / path / file name denote SalamandraTA?"""
    return model_name is not None and "salamandra" in model_name.lower()


def salamandra_language_name(code: str) -> str:
    """English language name as the SalamandraTA prompts expect it."""
    key = code.strip().lower().replace("_", "-")
    base = key.split("-", 1)[0]
    return (
        SALAMANDRA_LANGUAGES.get(key)
        or SALAMANDRA_LANGUAGES.get(base)
        or language_display_name(code)
    )


def build_salamandra_prompt(
    source_text: str,
    source_lang: str | None,
    target_lang: str,
    *,
    voc: dict[str, str] | None = None,
    preserve_markup: bool = False,
) -> str:
    """Render the SalamandraTA user turn for one chunk.

    Glossary entries (``voc``) select the terminology-aware wording; ``preserve_markup``
    selects the structured-text wording used for HTML chunks."""
    if not source_lang or source_lang.lower() == "auto":
        source_lang = SALAMANDRA_DEFAULT_SOURCE
    source = salamandra_language_name(source_lang)
    target = salamandra_language_name(target_lang)
    if voc:
        terms = "\n".join(f"- {src} -> {tgt}" for src, tgt in sorted(voc.items()))
        return (
            f"Please translate the following {source} text to {target} while respecting "
            f"the glossary entries.\n\nRequired Terminology:\n\n{terms}\n\n"
            f"Source Text:\n\n{source_text}"
        )
    if preserve_markup:
        return (
            f"Translate this {source} text into {target}. Preserve any formatting, tags, "
            f"delimiters, or structural elements exactly, and translate only the "
            f"human-readable parts: {source_text}"
        )
    return (
        f"Translate the following text from {source} into {target}.\n"
        f"{source}: {source_text}\n{target}:"
    )


__all__ = [
    "SALAMANDRA_DEFAULT_SOURCE",
    "SALAMANDRA_LANGUAGES",
    "SALAMANDRA_MAX_TOKENS",
    "SALAMANDRA_TEMPERATURE",
    "build_salamandra_prompt",
    "is_salamandra_model",
    "salamandra_language_name",
]
