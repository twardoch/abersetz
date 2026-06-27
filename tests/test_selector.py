"""Tests for the engine selector grammar."""
# this_file: tests/test_selector.py

from __future__ import annotations

import pytest

from abersetz.selector import (
    Selector,
    is_new_syntax,
    parse_selector,
    slugify_selector,
)


@pytest.mark.parametrize(
    ("raw", "engine", "subvariant", "provider"),
    [
        ("tr::google", "tr", None, "google"),
        ("dt::deepl", "dt", None, "deepl"),
        ("tr::", "tr", None, None),
        ("lm::gemma-3-4b", "lm", None, "gemma-3-4b"),
        ("ll::siliconflow:Qwen/Qwen2.5-7B", "ll", None, "siliconflow:Qwen/Qwen2.5-7B"),
        ("ml/hy-mt2::/models/Hy-MT2-7B", "ml", "hy-mt2", "/models/Hy-MT2-7B"),
        ("gg/gemma::/models/gemma.gguf", "gg", "gemma", "/models/gemma.gguf"),
    ],
)
def test_parse_new_syntax(raw, engine, subvariant, provider) -> None:
    sel = parse_selector(raw)
    assert sel is not None
    assert sel.engine == engine
    assert sel.subvariant == subvariant
    assert sel.provider == provider


def test_parse_none_returns_none() -> None:
    assert parse_selector(None) is None


def test_parse_blank_returns_empty_engine() -> None:
    sel = parse_selector("   ")
    assert sel is not None
    assert sel.engine == ""


def test_legacy_engine_provider() -> None:
    sel = parse_selector("tr/google")
    assert sel is not None
    assert sel.engine == "tr"
    assert sel.provider == "google"
    assert sel.subvariant is None


def test_legacy_long_names_normalize() -> None:
    assert parse_selector("translators/google").engine == "tr"
    assert parse_selector("deep-translator/deepl").engine == "dt"
    assert parse_selector("ullm/default").engine == "ll"
    assert parse_selector("lms").engine == "lm"


def test_legacy_local_backend_maps_to_ml_gg() -> None:
    mlx = parse_selector("mthy/mlx")
    assert mlx is not None
    assert mlx.engine == "ml"
    assert mlx.family == "mthy"

    gguf = parse_selector("gemma/gguf")
    assert gguf is not None
    assert gguf.engine == "gg"
    assert gguf.family == "gemma"


def test_family_resolution() -> None:
    assert parse_selector("ml/hy-mt2::x").family == "mthy"
    assert parse_selector("gg/gemma::x").family == "gemma"
    # Bare local engine defaults to the mthy family.
    assert parse_selector("ml::/path").family == "mthy"


def test_is_new_syntax() -> None:
    assert is_new_syntax("tr::google")
    assert not is_new_syntax("tr/google")
    assert not is_new_syntax(None)


def test_canonical_roundtrip() -> None:
    assert parse_selector("tr::google").canonical() == "tr::google"
    assert parse_selector("ml/hy-mt2::/p").canonical() == "ml/hy-mt2::/p"
    assert parse_selector("tr::").canonical() == "tr::"


def test_slugify() -> None:
    assert slugify_selector("tr::google") == "tr-google"
    assert slugify_selector("dt::deepl") == "dt-deepl"
    assert slugify_selector("ll::siliconflow:Qwen/Qwen2.5-7B") == "ll-siliconflow-qwen-qwen2-5-7b"
    # Path providers keep only the final component.
    assert slugify_selector("ml/hy-mt2::/models/Hy-MT2-7B") == "ml-hy-mt2-hy-mt2-7b"
    assert slugify_selector(Selector("gg", "gemma", "/m/g.gguf", "gg/gemma::/m/g.gguf")) == (
        "gg-gemma-g-gguf"
    )
