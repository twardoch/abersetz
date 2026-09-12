# this_file: src/abersetz/providers/translategemma.py
"""Prompt helpers for Google TranslateGemma checkpoints.

TranslateGemma's chat template is unusual: the single user message must carry a
one-element ``content`` list whose item names ``source_lang_code`` and
``target_lang_code`` next to the text. Runtimes that apply the model's own
template (``mlx_lm``, ``llama.cpp``) get that structure from
:func:`translategemma_messages`. Runtimes that only accept a plain string (LM
Studio SDK, OpenAI-compatible servers) get the *rendered* instruction from
:func:`render_translategemma_prompt`, which reproduces the template text
verbatim so the model sees exactly what it was trained on.

The model card recommends greedy decoding (``do_sample=False``) and an explicit
source language, so :data:`TRANSLATEGEMMA_TEMPERATURE` is ``0.0`` and
:func:`translategemma_source_lang` never returns ``auto``.
"""

from __future__ import annotations

from typing import Any

#: TranslateGemma is evaluated with ``do_sample=False``; temperature 0 is the
#: closest equivalent on sampling-based runtimes.
TRANSLATEGEMMA_TEMPERATURE = 0.0
#: Generous ceiling for one chunk; the model stops at ``<end_of_turn>`` anyway.
TRANSLATEGEMMA_MAX_TOKENS = 2048
#: Source language assumed when the caller left detection to the engine.
TRANSLATEGEMMA_DEFAULT_SOURCE = "en"


def is_translategemma_model(model_name: str | None) -> bool:
    """Heuristic: does a model id / path / file name denote TranslateGemma?"""
    return model_name is not None and "translategemma" in model_name.lower().replace("_", "")


def translategemma_source_lang(source_lang: str | None) -> str:
    """TranslateGemma needs a real source code; ``auto``/empty falls back to English."""
    if not source_lang or source_lang.lower() == "auto":
        return TRANSLATEGEMMA_DEFAULT_SOURCE
    return source_lang


def _normalise_code(code: str) -> str:
    return code.strip().replace("_", "-")


def language_display_name(code: str) -> str:
    """English display name for a BCP-47 code, matching the template's lookup table."""
    try:
        from langcodes import Language

        name = Language.get(_normalise_code(code)).language_name("en")
        if name and not name.lower().startswith("unknown"):
            return name
    except Exception:
        pass
    return code


def translategemma_messages(source_lang: str, target_lang: str, text: str) -> list[dict[str, Any]]:
    """Message list in the shape TranslateGemma's own chat template expects."""
    return [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "source_lang_code": _normalise_code(translategemma_source_lang(source_lang)),
                    "target_lang_code": _normalise_code(target_lang),
                    "text": text,
                }
            ],
        }
    ]


def render_translategemma_prompt(source_lang: str, target_lang: str, text: str) -> str:
    """Render the user turn exactly as TranslateGemma's chat template would."""
    src_code = _normalise_code(translategemma_source_lang(source_lang))
    tgt_code = _normalise_code(target_lang)
    src = language_display_name(src_code)
    tgt = language_display_name(tgt_code)
    return (
        f"You are a professional {src} ({src_code}) to {tgt} ({tgt_code}) translator. "
        f"Your goal is to accurately convey the meaning and nuances of the original {src} "
        f"text while adhering to {tgt} grammar, vocabulary, and cultural sensitivities.\n"
        f"Produce only the {tgt} translation, without any additional explanations or "
        f"commentary. Please translate the following {src} text into {tgt}:\n\n\n"
        f"{text.strip()}"
    )


def clean_translategemma_output(text: str) -> str:
    """Drop a trailing ``<end_of_turn>`` marker some runtimes leak into the string."""
    return text.split("<end_of_turn>")[0].strip()


__all__ = [
    "TRANSLATEGEMMA_DEFAULT_SOURCE",
    "TRANSLATEGEMMA_MAX_TOKENS",
    "TRANSLATEGEMMA_TEMPERATURE",
    "clean_translategemma_output",
    "is_translategemma_model",
    "language_display_name",
    "render_translategemma_prompt",
    "translategemma_messages",
    "translategemma_source_lang",
]
