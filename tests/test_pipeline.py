"""Integration tests for the translation pipeline."""
# this_file: tests/test_pipeline.py

from __future__ import annotations

from pathlib import Path

import pytest

from abersetz.engines import EngineResult
from abersetz.pipeline import PipelineError, TranslatorOptions, translate_path


class DummyEngine:
    """Minimal engine used for pipeline tests."""

    def __init__(self) -> None:
        self.name = "dummy"
        self.chunk_size = 5
        self.html_chunk_size = None
        self.chunks: list[str] = []

    def chunk_size_for(self, _fmt) -> int:
        return self.chunk_size

    def translate(self, request) -> EngineResult:
        self.chunks.append(request.text)
        voc = dict(request.voc)
        voc[f"chunk_{len(self.chunks)}"] = request.text.upper()
        return EngineResult(text=request.text.upper(), voc=voc)


def test_translate_path_processes_files(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    src_dir = tmp_path / "docs"
    src_dir.mkdir()
    source = src_dir / "sample.txt"
    source.write_text("hello world", encoding="utf-8")

    dummy = DummyEngine()
    monkeypatch.setattr("abersetz.pipeline.create_engine", lambda *args, **kwargs: dummy)

    options = TranslatorOptions(output_dir=tmp_path / "out", save_voc=True, chunk_size=4)
    results = translate_path(src_dir, options)

    assert len(results) == 1
    output_file = tmp_path / "out" / "sample.txt"
    assert output_file.read_text(encoding="utf-8") == "HELLO WORLD"
    vocab_file = output_file.with_suffix(output_file.suffix + ".voc.json")
    saved_vocab = vocab_file.read_text(encoding="utf-8")
    assert "chunk_1" in saved_vocab
    assert dummy.chunks  # ensure engine invoked


def test_translate_path_requires_matches(tmp_path: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    with pytest.raises(PipelineError):
        translate_path(empty, TranslatorOptions(include=("*.doesnotexist",)))
