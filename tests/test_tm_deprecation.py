# this_file: tests/test_tm_deprecation.py
"""Translation-memory features are deprecated (moved to vexy-localizzy) but still work."""

from __future__ import annotations

import warnings
from types import SimpleNamespace

import pytest

from abersetz import cli, pipeline, retrieval
from abersetz.pipeline import TranslatorOptions, translate_string
from abersetz.providers.base import EngineResult

MOVED = r"translation memories moved to vexy-localizzy; abersetz keeps examples/voc as engine hints"


def fake_engine():
    engine = SimpleNamespace(
        supports_translation_examples=True, name="test", chunk_size_for=lambda fmt: 1000
    )
    engine.translate = lambda request: EngineResult("przetłumaczone", request.voc)
    return engine


def test_plain_options_and_translation_when_no_tm_then_no_warning(monkeypatch) -> None:
    """The normal engine path must stay silent, including per-chunk helpers."""
    monkeypatch.setattr(pipeline, "create_engine", lambda *a, **kw: fake_engine())
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        opts = TranslatorOptions(engine="ll::test", to_lang="pl", initial_voc={"a": "b"})
        assert translate_string("text", opts) == "przetłumaczone"


@pytest.mark.parametrize(
    ("field", "value"),
    [("tm", "memory.db"), ("tm_top_k", 3), ("tm_exact_only", True), ("tm_origins", ["x"])],
)
def test_translator_options_when_tm_field_set_then_deprecation_warning(field, value) -> None:
    with pytest.warns(DeprecationWarning, match=MOVED) as record:
        TranslatorOptions(to_lang="pl", **{field: value})
    assert f"TranslatorOptions.{field}" in str(record[0].message)
    assert record[0].filename == __file__, "stacklevel must point at the caller"


def test_translate_string_when_tm_used_then_still_works_and_warns_once(monkeypatch) -> None:
    memory = SimpleNamespace(exact=lambda text, lang: [SimpleNamespace(target="Krój")])
    monkeypatch.setattr(pipeline, "create_engine", lambda *a, **kw: pytest.fail("no engine"))
    with pytest.warns(DeprecationWarning, match=MOVED) as record:
        opts = TranslatorOptions(to_lang="pl", tm=memory)
        assert translate_string("A font", opts) == "Krój"
    assert len(record) == 1, [str(w.message) for w in record]


def test_with_memory_when_used_publicly_then_deprecation_warning() -> None:
    with pytest.warns(DeprecationWarning, match=MOVED) as record:
        wrapped = retrieval.with_memory(lambda value, options=None: value)
    assert "with_memory" in str(record[0].message)
    assert record[0].filename == __file__
    assert wrapped("x") == "x"


def test_exact_translation_when_used_publicly_then_deprecation_warning() -> None:
    opts = SimpleNamespace(tm=None, from_lang="en", to_lang="pl")
    with pytest.warns(DeprecationWarning, match=MOVED) as record:
        assert retrieval.exact_translation("x", opts) is None
    assert "exact_translation" in str(record[0].message)


def test_cli_when_tm_flag_given_then_deprecation_warning(monkeypatch) -> None:
    calls = []
    monkeypatch.setattr(cli, "translate_string", lambda text, opts: calls.append(opts) or "ok")
    with pytest.warns(DeprecationWarning, match=MOVED) as record:
        cli.AbersetzCLI().tr("pl", "text", tm="memory.db")
    assert any("--tm flag" in str(w.message) for w in record)
    assert calls[0].tm == "memory.db", "deprecated flags keep working until 2.0"


def test_cli_when_tm_top_k_given_then_names_that_flag() -> None:
    with pytest.warns(DeprecationWarning, match=r"--tm-top-k"):
        cli._warn_tm_flags(**{**pipeline._TM_DEFAULTS, "tm_top_k": 9})


def test_cli_when_no_tm_flags_then_silent() -> None:
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        cli._warn_tm_flags(**pipeline._TM_DEFAULTS)
