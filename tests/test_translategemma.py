# this_file: tests/test_translategemma.py
"""TranslateGemma prompt rendering must match the model's own chat template."""

from __future__ import annotations

import pytest

from abersetz.providers.translategemma import (
    TRANSLATEGEMMA_TEMPERATURE,
    clean_translategemma_output,
    is_translategemma_model,
    language_display_name,
    render_translategemma_prompt,
    translategemma_messages,
    translategemma_source_lang,
)

# Rendered by google/translategemma's chat_template.jinja for ("en", "pl", "Hello world").
EXPECTED_EN_PL = (
    "You are a professional English (en) to Polish (pl) translator. Your goal is to "
    "accurately convey the meaning and nuances of the original English text while adhering "
    "to Polish grammar, vocabulary, and cultural sensitivities.\n"
    "Produce only the Polish translation, without any additional explanations or commentary. "
    "Please translate the following English text into Polish:\n\n\nHello world"
)


def test_render_prompt_when_en_pl_then_matches_chat_template_verbatim() -> None:
    assert render_translategemma_prompt("en", "pl", "Hello world") == EXPECTED_EN_PL


def test_render_prompt_when_regional_and_underscore_codes_then_normalised() -> None:
    prompt = render_translategemma_prompt("pt_BR", "de-DE", " Olá ")
    assert prompt.startswith(
        "You are a professional Portuguese (pt-BR) to German (de-DE) translator."
    )
    assert prompt.endswith("into German:\n\n\nOlá"), "text is trimmed like the template does"


def test_render_prompt_when_source_auto_then_english_assumed() -> None:
    prompt = render_translategemma_prompt("auto", "fr", "Hi")
    assert prompt.startswith("You are a professional English (en) to French (fr) translator.")


@pytest.mark.parametrize(
    ("raw", "expected"), [("auto", "en"), ("", "en"), (None, "en"), ("cs", "cs")]
)
def test_source_lang(raw: str | None, expected: str) -> None:
    assert translategemma_source_lang(raw) == expected


def test_messages_when_built_then_single_content_item_with_codes() -> None:
    messages = translategemma_messages("auto", "zh_Hant", "Hi")
    assert len(messages) == 1 and messages[0]["role"] == "user"
    assert messages[0]["content"] == [
        {"type": "text", "source_lang_code": "en", "target_lang_code": "zh-Hant", "text": "Hi"}
    ]


@pytest.mark.parametrize(
    ("code", "name"), [("en", "English"), ("de-DE", "German"), ("ja", "Japanese"), ("xx", "xx")]
)
def test_language_display_name(code: str, name: str) -> None:
    assert language_display_name(code) == name


def test_clean_output_strips_end_of_turn() -> None:
    assert clean_translategemma_output(" Cześć <end_of_turn>\n") == "Cześć"
    assert clean_translategemma_output("plain") == "plain"


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("mlx-community/translategemma-4b-it-8bit", True),
        ("translategemma-27b-it.Q4_K_M.gguf", True),
        ("translate_gemma-4b", True),
        ("gemma-3-4b-it", False),
        (None, False),
    ],
)
def test_is_translategemma_model(name: str | None, expected: bool) -> None:
    assert is_translategemma_model(name) is expected


def test_greedy_temperature() -> None:
    assert TRANSLATEGEMMA_TEMPERATURE == 0.0, "model card evaluates with do_sample=False"
