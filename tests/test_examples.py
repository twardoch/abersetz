"""Tests for the job-driven translation benchmark example."""
# this_file: tests/test_examples.py

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest


def _load_module(name: str, filename: str) -> Any:
    module_path = Path(__file__).resolve().parents[1] / "examples" / filename
    spec = importlib.util.spec_from_file_location(name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load examples/{filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


benchmark_mod = _load_module("examples.benchmark", "benchmark.py")
prep_mod = _load_module("examples.benchmark_prep", "benchmark_prep.py")
BenchmarkRunner = benchmark_mod.BenchmarkRunner
main = benchmark_mod.main


def _write_job(tmp_path: Path, selectors: list[str], to_lang: str = "pl") -> Path:
    job = {"to_lang": to_lang, "from_lang": "en", "entries": [{"selector": s} for s in selectors]}
    job_path = tmp_path / "job.json"
    job_path.write_text(json.dumps(job), encoding="utf-8")
    return job_path


def _mock_translate(monkeypatch: pytest.MonkeyPatch) -> list[Path]:
    from abersetz.chunking import TextFormat
    from abersetz.pipeline import TranslationResult

    called: list[Path] = []

    def fake_translate_path(source: Path, opts: Any) -> list[TranslationResult]:
        called.append(source)
        dest = Path(opts.output_dir) / source.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text("translated", encoding="utf-8")
        return [
            TranslationResult(
                source=source,
                destination=dest,
                chunks=1,
                voc={},
                format=TextFormat.PLAIN,
                engine=opts.engine,
            )
        ]

    monkeypatch.setattr(benchmark_mod, "translate_path", fake_translate_path)
    return called


def test_output_path_uses_suffix() -> None:
    out = benchmark_mod._output_path(Path("/x/poem.en.md"), Path("/out"), "pl", "tr-google")
    assert out == Path("/out/poem.en.pl--tr-google.md")


def test_benchmark_run_writes_report(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    src = tmp_path / "poem.en.md"
    src.write_text("Hello world", encoding="utf-8")
    job_path = _write_job(tmp_path, ["tr::google", "dt::deepl"])
    report = tmp_path / "report.json"
    out_dir = tmp_path / "out"

    _mock_translate(monkeypatch)

    BenchmarkRunner().run(
        job=str(job_path), input=str(src), report=str(report), output_dir=str(out_dir)
    )

    assert report.exists()
    data = json.loads(report.read_text(encoding="utf-8"))
    assert {r["selector"] for r in data} == {"tr::google", "dt::deepl"}
    assert all(r["success"] for r in data)
    # Output files were renamed to the suffixed scheme.
    assert (out_dir / "poem.en.pl--tr-google.md").exists()
    assert (out_dir / "poem.en.pl--dt-deepl.md").exists()


def test_benchmark_skips_existing_without_force(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    src = tmp_path / "poem.en.md"
    src.write_text("Hello", encoding="utf-8")
    job_path = _write_job(tmp_path, ["tr::google"])
    report = tmp_path / "report.json"
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    # Seed the expected output so the entry is skipped.
    (out_dir / "poem.en.pl--tr-google.md").write_text("old", encoding="utf-8")

    called = _mock_translate(monkeypatch)
    BenchmarkRunner().run(
        job=str(job_path), input=str(src), report=str(report), output_dir=str(out_dir)
    )

    data = json.loads(report.read_text(encoding="utf-8"))
    assert data[0]["skipped"] is True
    assert called == []  # translate_path never invoked


def test_benchmark_records_failure(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    src = tmp_path / "poem.en.md"
    src.write_text("Hello", encoding="utf-8")
    job_path = _write_job(tmp_path, ["tr::google"])
    report = tmp_path / "report.json"

    def boom(source: Path, opts: Any) -> list[Any]:
        raise RuntimeError("rate limited")

    monkeypatch.setattr(benchmark_mod, "translate_path", boom)
    BenchmarkRunner().run(job=str(job_path), input=str(src), report=str(report))

    data = json.loads(report.read_text(encoding="utf-8"))
    assert data[0]["success"] is False
    assert "rate limited" in data[0]["error"]


def test_benchmark_missing_input_exits(tmp_path: Path) -> None:
    job_path = _write_job(tmp_path, ["tr::google"])
    with pytest.raises(SystemExit) as exc:
        BenchmarkRunner().run(
            job=str(job_path), input=str(tmp_path / "nope.md"), report=str(tmp_path / "r.json")
        )
    assert exc.value.code == 1


def test_benchmark_no_model_paths_literal() -> None:
    """The benchmark must not hard-code model paths (issue 111 requirement)."""
    source = (Path(__file__).resolve().parents[1] / "examples" / "benchmark.py").read_text()
    assert "MODEL_PATHS" not in source


def test_main_invokes_fire() -> None:
    with patch("fire.Fire") as mock_fire:
        main()
        mock_fire.assert_called_once_with(BenchmarkRunner)


def test_prep_generates_job(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from abersetz.listing import CatalogEntry

    monkeypatch.setattr(
        prep_mod,
        "build_catalog",
        lambda prefix, **k: [CatalogEntry(f"{prefix}::google", "provider")],
    )
    out = tmp_path / "job.json"
    prep_mod.prepare(output=str(out), selectors="tr,dt", to_lang="pl")

    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["to_lang"] == "pl"
    selectors = {e["selector"] for e in data["entries"]}
    assert selectors == {"tr::google", "dt::google"}
