# this_file: tests/test_htmladapt_twat.py
from __future__ import annotations

from pathlib import Path

import pytest

from abersetz.engines import EngineBase, EngineRequest, EngineResult
from abersetz.pipeline import AbersetzConfig, TranslatorOptions, translate_path
from abersetz.tasks import translate_flow, translate_task


class MockCounterEngine(EngineBase):
    """Engine that tracks translation call count."""

    def __init__(self, name: str = "counter"):
        super().__init__(name, chunk_size=1000, html_chunk_size=1000)
        self.call_count = 0

    def translate(self, request: EngineRequest) -> EngineResult:
        self.call_count += 1
        # Simple translation logic: swap 'Hello' to 'Witaj' and 'World' to 'Świat'
        translated = request.text.replace("Hello", "Witaj").replace("World", "Świat")
        return EngineResult(text=translated, voc=request.voc)


def test_htmladapt_translation_preserves_structure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that htmladapt successfully preserves structure and attributes during HTML translation."""
    src_file = tmp_path / "index.html"
    html_content = (
        "<!DOCTYPE html>\n"
        "<html>\n"
        "<head><title>Test Doc</title></head>\n"
        "<body>\n"
        '  <div class="content" data-attr="xyz">\n'
        "    <h1>Hello</h1>\n"
        "    <p>World</p>\n"
        "  </div>\n"
        "</body>\n"
        "</html>"
    )
    src_file.write_text(html_content, encoding="utf-8")

    engine = MockCounterEngine("mock-html")

    def fake_create_engine(
        selector: str, config: AbersetzConfig, **kwargs: object
    ) -> MockCounterEngine:
        return engine

    monkeypatch.setattr("abersetz.pipeline.create_engine", fake_create_engine)

    options = TranslatorOptions(
        engine="mock-html",
        output_dir=tmp_path / "out",
        to_lang="pl",
    )

    results = translate_path(src_file, options)
    assert len(results) == 1
    dest_path = results[0].destination
    assert dest_path.exists()

    translated_html = dest_path.read_text(encoding="utf-8")

    # Assert translations occurred
    assert "Witaj" in translated_html
    assert "Świat" in translated_html
    # Assert attributes and layout were preserved
    assert 'class="content"' in translated_html
    assert 'data-attr="xyz"' in translated_html
    assert "<title>Test Doc</title>" in translated_html


def _bcache_active() -> bool:
    """Whether a real caching bcache decorator is available in this environment."""
    try:
        from abersetz.pipeline import bcache
    except Exception:
        return False

    calls = {"n": 0}

    @bcache(folder_name="abersetz_test_probe")
    def _probe(x: int) -> int:
        calls["n"] += 1
        return x

    _probe(1)
    _probe(1)
    return calls["n"] == 1


def test_twat_cache_caching_behavior(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that twat-cache decorator successfully caches translation results on repeat calls."""
    if not _bcache_active():
        pytest.skip("twat_cache caching unavailable in this environment (no-op bcache fallback)")
    src_file = tmp_path / "sample.txt"
    src_file.write_text("Hello World", encoding="utf-8")

    engine = MockCounterEngine("mock-cache")

    def fake_create_engine(
        selector: str, config: AbersetzConfig, **kwargs: object
    ) -> MockCounterEngine:
        return engine

    monkeypatch.setattr("abersetz.pipeline.create_engine", fake_create_engine)

    # Use a unique destination output dir to ensure distinct cached workflows
    out_dir_1 = tmp_path / "out1"
    options_1 = TranslatorOptions(
        engine="mock-cache",
        output_dir=out_dir_1,
        to_lang="pl",
    )

    # First call: hits the engine
    results_1 = translate_path(src_file, options_1)
    assert results_1[0].destination.read_text(encoding="utf-8") == "Witaj Świat"
    first_call_count = engine.call_count
    assert first_call_count > 0

    # Second call (using same input content and parameters)
    out_dir_2 = tmp_path / "out2"
    options_2 = TranslatorOptions(
        engine="mock-cache",
        output_dir=out_dir_2,
        to_lang="pl",
    )

    results_2 = translate_path(src_file, options_2)
    assert results_2[0].destination.read_text(encoding="utf-8") == "Witaj Świat"

    # Assert that call count didn't increase (cache hit)
    second_call_count = engine.call_count
    assert second_call_count == first_call_count


def test_prefect_workflow_integration(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that prefect task and flow functions run successfully."""
    src_file = tmp_path / "flow_sample.txt"
    src_file.write_text("Hello", encoding="utf-8")

    engine = MockCounterEngine("mock-flow")

    def fake_create_engine(
        selector: str, config: AbersetzConfig, **kwargs: object
    ) -> MockCounterEngine:
        return engine

    monkeypatch.setattr("abersetz.pipeline.create_engine", fake_create_engine)

    out_dir = tmp_path / "flow_out"

    # Test translate_task (Prefect Task)
    opts = TranslatorOptions(
        engine="mock-flow",
        output_dir=out_dir,
        to_lang="pl",
    )
    task_results = translate_task(src_file, opts)
    assert len(task_results) == 1
    assert task_results[0].destination.read_text(encoding="utf-8") == "Witaj"

    # Test translate_flow (Prefect Flow)
    flow_results = translate_flow(
        path=src_file,
        to_lang="pl",
        engine="mock-flow",
        options={"output_dir": out_dir},
    )
    assert len(flow_results) == 1
    assert flow_results[0]["destination"] == str(task_results[0].destination)
