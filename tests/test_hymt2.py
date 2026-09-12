# this_file: tests/test_hymt2.py
"""Unit tests for the shared Hy-MT2 prompt / sampling helpers."""

from __future__ import annotations

import pytest

from abersetz.providers.base import EngineError
from abersetz.providers.hymt2 import (
    HYMT2_LANGUAGE_TABLE,
    HYMT2_SAMPLING_DENSE,
    HYMT2_SAMPLING_MOE,
    build_hymt2_prompt,
    hymt2_language_name,
    hymt2_language_name_zh,
    hymt2_messages,
    hymt2_sampling,
    is_hymt2_model,
)


def test_language_table_matches_upstream_count() -> None:
    assert len(HYMT2_LANGUAGE_TABLE) == 38, "upstream README lists 38 rows"
    assert len({row[1] for row in HYMT2_LANGUAGE_TABLE}) == 38, "codes must be unique"


@pytest.mark.parametrize(
    ("code", "english", "chinese"),
    [
        ("en", "English", "英语"),
        ("PL", "Polish", "波兰语"),
        ("zh", "Chinese", "中文"),
        ("zh-Hant", "Traditional Chinese", "繁体中文"),
        ("zh_TW", "Traditional Chinese", "繁体中文"),
        ("zh-CN", "Chinese", "中文"),
        ("pt-BR", "Portuguese", "葡萄牙语"),
        ("de-AT", "German", "德语"),
        ("german", "German", "德语"),
        ("德语", "German", "德语"),
        ("yue", "Cantonese", "粤语"),
    ],
)
def test_language_name_when_code_or_alias_then_resolves(
    code: str, english: str, chinese: str
) -> None:
    assert hymt2_language_name(code) == english, f"{code} should resolve to {english}"
    assert hymt2_language_name_zh(code) == chinese, f"{code} should resolve to {chinese}"


def test_language_name_when_unsupported_then_engine_error() -> None:
    with pytest.raises(EngineError, match="Unsupported Hy-MT2 language"):
        hymt2_language_name("xx")


def test_build_prompt_when_no_terms_then_default_template() -> None:
    prompt = build_hymt2_prompt("Hello", "pl")
    assert prompt == (
        "Translate the following text into Polish. Note that you should **only output "
        "the translated result without any additional explanation**:\n\nHello"
    )


def test_build_prompt_when_terms_then_terminology_template() -> None:
    prompt = build_hymt2_prompt("Hello", "fr", voc={"hello": "bonjour", "apple": "pomme"})
    assert prompt.startswith("Reference the following translations:\n")
    assert "apple translates to pomme\nhello translates to bonjour\n\n" in prompt
    assert "Translate the following text into French. Note that you must **ONLY output" in prompt
    assert prompt.endswith(":\n\nHello")


def test_build_prompt_when_preamble_then_prepended() -> None:
    prompt = build_hymt2_prompt("Hi", "de", preamble="Reference pairs\n[]\n\n")
    assert prompt.startswith("Reference pairs\n[]\n\nTranslate the following text into German")


def test_messages_when_built_then_single_user_turn() -> None:
    messages = hymt2_messages("p")
    assert messages == [{"role": "user", "content": "p"}], "no system prompt for Hy-MT2"


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("tencent/hy-mt2-7b", HYMT2_SAMPLING_DENSE),
        ("Hy-MT2-1.8B-Q8_0.gguf", HYMT2_SAMPLING_DENSE),
        ("mlx-community/Hy-MT2-7B-8bit", HYMT2_SAMPLING_DENSE),
        ("tencent/hy-mt2-30b-a3b", HYMT2_SAMPLING_MOE),
        ("dawncr0w/Hy-MT2-30B-A3B-oQ8-MLX", HYMT2_SAMPLING_MOE),
        (None, HYMT2_SAMPLING_DENSE),
    ],
)
def test_sampling_when_model_name_then_size_class(name: str | None, expected: object) -> None:
    assert hymt2_sampling(name) is expected, f"{name} should map to {expected}"


def test_sampling_values_match_upstream_readme() -> None:
    assert (
        HYMT2_SAMPLING_DENSE.temperature,
        HYMT2_SAMPLING_DENSE.top_p,
        HYMT2_SAMPLING_DENSE.top_k,
        HYMT2_SAMPLING_DENSE.repetition_penalty,
        HYMT2_SAMPLING_DENSE.max_tokens,
    ) == (0.7, 0.6, 20, 1.05, 4096)
    assert (HYMT2_SAMPLING_MOE.top_p, HYMT2_SAMPLING_MOE.top_k) == (1.0, -1)


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("tencent/hy-mt2-7b", True),
        ("hy-mt2-pro", True),
        ("Hy_MT2-1.8B", True),
        ("HyMT2-7B-oQ8", True),
        ("Qwen/Qwen2.5-7B-Instruct", False),
        ("", False),
        (None, False),
    ],
)
def test_is_hymt2_model(name: str | None, expected: bool) -> None:
    assert is_hymt2_model(name) is expected
