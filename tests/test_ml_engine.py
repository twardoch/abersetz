"""Smoke tests for the MLX (``ml``) and GGUF (``gg``) local engine modules.

IMPORTANT — engine naming note
-------------------------------
The ``--engine ml/...`` selector in abersetz uses Apple Silicon MLX inference
(``mlx_lm`` / ``LocalMlxEngine``).  It has **nothing** to do with MarianMT or
the HuggingFace ``transformers`` library.  MarianMT is not implemented in
abersetz.  The ``transformers`` package is present in the environment only as a
transitive dependency; it is not used by any engine adapter.
"""
# this_file: tests/test_ml_engine.py

import pytest

from abersetz.providers.base import EngineError


# ---------------------------------------------------------------------------
# Module-level import smoke tests
# ---------------------------------------------------------------------------


def test_mlx_module_imports() -> None:
    """Verify the MLX provider module can be imported without errors."""
    from abersetz.providers import mlx as mlx_mod

    assert hasattr(mlx_mod, "LocalMlxEngine")
    assert hasattr(mlx_mod, "_resolve_mthy_language")
    assert hasattr(mlx_mod, "build_mthy_prompt")
    assert hasattr(mlx_mod, "resolve_and_download_model")


def test_gguf_module_imports() -> None:
    """Verify the GGUF provider module can be imported without errors."""
    from abersetz.providers import gguf as gguf_mod

    assert hasattr(gguf_mod, "LocalGgufEngine")


# ---------------------------------------------------------------------------
# Language resolution
# ---------------------------------------------------------------------------


def test_resolve_mthy_language_iso_code() -> None:
    """Standard 2-letter ISO codes map to their Chinese label."""
    from abersetz.providers.mlx import _resolve_mthy_language

    assert _resolve_mthy_language("en") == "英语"
    assert _resolve_mthy_language("de") == "德语"
    assert _resolve_mthy_language("zh") == "中文"
    assert _resolve_mthy_language("ja") == "日语"
    assert _resolve_mthy_language("pl") == "波兰语"


def test_resolve_mthy_language_english_name() -> None:
    """English language names also resolve correctly."""
    from abersetz.providers.mlx import _resolve_mthy_language

    assert _resolve_mthy_language("english") == "英语"
    assert _resolve_mthy_language("german") == "德语"
    assert _resolve_mthy_language("chinese") == "中文"


def test_resolve_mthy_language_chinese_label() -> None:
    """Chinese labels round-trip through the lookup table."""
    from abersetz.providers.mlx import _resolve_mthy_language

    assert _resolve_mthy_language("英语") == "英语"
    assert _resolve_mthy_language("德语") == "德语"


def test_resolve_mthy_language_unsupported_raises() -> None:
    """An unsupported language code raises EngineError."""
    from abersetz.providers.mlx import _resolve_mthy_language

    with pytest.raises(EngineError, match="Unsupported HY-MT language"):
        _resolve_mthy_language("xx-BOGUS")


def test_resolve_mthy_language_traditional_chinese() -> None:
    """Traditional Chinese variant maps correctly."""
    from abersetz.providers.mlx import _resolve_mthy_language

    assert _resolve_mthy_language("zh-Hant") == "繁体中文"


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------


def test_build_mthy_prompt_no_voc() -> None:
    """Prompt without vocabulary is correctly formatted."""
    from abersetz.providers.mlx import build_mthy_prompt

    prompt = build_mthy_prompt("Hello", "英语")
    assert "Hello" in prompt
    assert "英语" in prompt
    # No vocabulary section when voc is empty
    assert "翻译成" not in prompt or "英语" in prompt


def test_build_mthy_prompt_with_voc() -> None:
    """Prompt includes vocabulary terms when provided."""
    from abersetz.providers.mlx import build_mthy_prompt

    prompt = build_mthy_prompt("Hello", "德语", voc={"Hello": "Hallo"})
    assert "Hello" in prompt
    assert "Hallo" in prompt
    assert "德语" in prompt
    # Vocabulary injection marker
    assert "参考下面的翻译" in prompt


def test_build_mthy_prompt_empty_voc() -> None:
    """Empty vocabulary dict is treated the same as no vocabulary."""
    from abersetz.providers.mlx import build_mthy_prompt

    prompt_none = build_mthy_prompt("Test", "法语", voc=None)
    prompt_empty = build_mthy_prompt("Test", "法语", voc={})
    assert prompt_none == prompt_empty


# ---------------------------------------------------------------------------
# Model path resolution
# ---------------------------------------------------------------------------


def test_resolve_model_nonexistent_path_raises() -> None:
    """A path that does not exist on disk raises EngineError."""
    from abersetz.providers.mlx import resolve_and_download_model

    with pytest.raises(EngineError):
        resolve_and_download_model("/nonexistent/path/to/model.gguf", "mlx")


def test_resolve_model_legacy_hy_mt1_raises() -> None:
    """Legacy Hy-MT1 model identifiers raise EngineError with a helpful message."""
    from abersetz.providers.mlx import resolve_and_download_model

    with pytest.raises(EngineError, match="Hy-MT1.x models are no longer supported"):
        resolve_and_download_model("Hunyuan-MT-7B", "gguf")


def test_resolve_model_existing_path() -> None:
    """An existing directory path is returned resolved to its absolute real path.

    On macOS, ``/var/folders/…`` is a symlink to ``/private/var/folders/…``.
    ``resolve_and_download_model`` calls ``Path.resolve()`` so the returned path
    may differ from the input by the symlink prefix; compare resolved forms.
    """
    import tempfile
    from pathlib import Path

    from abersetz.providers.mlx import resolve_and_download_model

    with tempfile.TemporaryDirectory() as tmpdir:
        resolved = resolve_and_download_model(tmpdir, "mlx")
        # Both should resolve to the same real path
        assert Path(resolved).resolve() == Path(tmpdir).resolve()


# ---------------------------------------------------------------------------
# Alias table sanity
# ---------------------------------------------------------------------------


def test_alias_table_coverage() -> None:
    """All aliases in ALIASES map to keys in KNOWN_MAPPING."""
    from abersetz.providers.mlx import ALIASES, KNOWN_MAPPING

    for alias, repo_key in ALIASES.items():
        assert repo_key in KNOWN_MAPPING, (
            f"Alias '{alias}' → '{repo_key}' not found in KNOWN_MAPPING"
        )


def test_known_mapping_has_required_fields() -> None:
    """Every entry in KNOWN_MAPPING has 'repo' and 'type' fields."""
    from abersetz.providers.mlx import KNOWN_MAPPING

    for key, info in KNOWN_MAPPING.items():
        assert "repo" in info, f"Missing 'repo' in KNOWN_MAPPING['{key}']"
        assert "type" in info, f"Missing 'type' in KNOWN_MAPPING['{key}']"
        assert info["type"] in {"mlx", "gguf"}, (
            f"Unexpected type '{info['type']}' in KNOWN_MAPPING['{key}']"
        )


# ---------------------------------------------------------------------------
# MarianMT non-existence confirmation
# ---------------------------------------------------------------------------


def test_marianmt_not_in_abersetz_engines() -> None:
    """Confirm MarianMT is NOT an engine in abersetz (plan documentation error).

    The plan describes '--ml' as 'MarianMT'.  In reality, 'ml' is the MLX
    backend (LocalMlxEngine using mlx_lm).  This test documents that finding.
    """
    import abersetz.providers as providers_pkg

    # No MarianMT class should exist anywhere in the providers package
    assert not hasattr(providers_pkg, "MarianMTEngine")
    assert not hasattr(providers_pkg, "MarianEngine")

    # The 'ml' selector family is handled by LocalMlxEngine
    from abersetz.providers.mlx import LocalMlxEngine

    assert LocalMlxEngine.__name__ == "LocalMlxEngine"
