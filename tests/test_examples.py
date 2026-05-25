"""Tests for the translation benchmark example utility."""
# this_file: tests/test_examples.py

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest


# Load benchmark module dynamically
def _load_benchmark() -> Any:
    module_path = Path(__file__).resolve().parents[1] / "examples" / "benchmark.py"
    spec = importlib.util.spec_from_file_location("examples.benchmark", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load examples/benchmark.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


benchmark_mod = _load_benchmark()
sanitize_name = benchmark_mod.sanitize_name
get_engine_descriptor = benchmark_mod.get_engine_descriptor
BenchmarkRunner = benchmark_mod.BenchmarkRunner
main = benchmark_mod.main


class DummyEngineConfig:
    def __init__(
        self, name: str, options: dict[str, Any], credential: dict[str, Any] | None = None
    ) -> None:
        self.name = name
        self.options = options
        self.credential = credential
        self.chunk_size = options.get("chunk_size", 800)
        self.html_chunk_size = options.get("html_chunk_size", 1200)


class DummyConfig:
    def __init__(self, engines: dict[str, Any]) -> None:
        self.engines = engines


def test_sanitize_name_when_input_has_special_chars_then_replaces_with_hyphens() -> None:
    """Test sanitize_name replaces non-alphanumeric chars with hyphens."""
    assert sanitize_name("engine/name-1.0") == "engine-name-1-0"
    assert sanitize_name("some_model@name!") == "some_model-name"


def test_sanitize_name_when_input_has_leading_trailing_hyphens_then_strips_them() -> None:
    """Test sanitize_name strips leading/trailing hyphens."""
    assert sanitize_name("---my-model---") == "my-model"


def test_get_engine_descriptor_when_translators_then_returns_correct_prefix() -> None:
    """Test get_engine_descriptor formatting for translators engine."""
    engine_cfg = DummyEngineConfig("translators", {"provider": "google"})
    cfg = DummyConfig({"translators": engine_cfg})

    # Variant specified in selector
    assert get_engine_descriptor("translators/bing", cfg) == "tr-bing"
    # Fallback to provider option
    assert get_engine_descriptor("translators", cfg) == "tr-google"


def test_get_engine_descriptor_when_deep_translator_then_returns_correct_prefix() -> None:
    """Test get_engine_descriptor formatting for deep-translator engine."""
    engine_cfg = DummyEngineConfig("deep-translator", {"provider": "my_memory"})
    cfg = DummyConfig({"deep-translator": engine_cfg})

    assert get_engine_descriptor("deep-translator/google", cfg) == "dt-google"
    assert get_engine_descriptor("deep-translator", cfg) == "dt-my_memory"


def test_get_engine_descriptor_when_hysf_then_returns_tencent_details() -> None:
    """Test get_engine_descriptor formatting for hysf engine."""
    engine_cfg = DummyEngineConfig("hysf", {"model": "Hunyuan-MT-7B"})
    cfg = DummyConfig({"hysf": engine_cfg})

    assert get_engine_descriptor("hysf", cfg) == "hysf-siliconflow-Hunyuan-MT-7B"


def test_get_engine_descriptor_when_ullm_then_returns_profile_details() -> None:
    """Test get_engine_descriptor formatting for ullm engine."""
    profiles = {
        "default": {"model": "Hunyuan-MT-7B"},
        "custom": {"model": "my-custom-model"},
    }
    engine_cfg = DummyEngineConfig("ullm", {"profiles": profiles})
    cfg = DummyConfig({"ullm": engine_cfg})

    assert get_engine_descriptor("ullm/default", cfg) == "ullm-default-Hunyuan-MT-7B"
    assert get_engine_descriptor("ullm/custom", cfg) == "ullm-custom-my-custom-model"
    # Default variant fallback
    assert get_engine_descriptor("ullm", cfg) == "ullm-default-Hunyuan-MT-7B"


def test_get_engine_descriptor_when_mthy_or_gemma_then_returns_backend_details() -> None:
    """Test get_engine_descriptor formatting for local engines like mthy and gemma."""
    engine_cfg_mthy = DummyEngineConfig(
        "mthy", {"backend": "mlx", "mlx_path": "/path/to/my-model-1.8B"}
    )
    cfg = DummyConfig({"mthy": engine_cfg_mthy})

    assert get_engine_descriptor("mthy/mlx", cfg) == "mthy-mlx-my-model-1-8B"
    # Backend fallback
    assert get_engine_descriptor("mthy", cfg) == "mthy-mlx-my-model-1-8B"


def test_get_engine_descriptor_when_unknown_engine_then_returns_sanitized_selector() -> None:
    """Test get_engine_descriptor fallbacks for unknown engines."""
    cfg = DummyConfig({})
    assert get_engine_descriptor("unknown-engine/variant", cfg) == "unknown-engine-variant"


def test_runner_run_when_dry_run_then_completes_successfully(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test standard runner execution on dry-run mode."""
    # Write temporary mock files inside examples/data
    root_dir = tmp_path / "mock_project"
    poem_dir = root_dir / "examples" / "data" / "poem"
    fontlab_dir = root_dir / "examples" / "data" / "fontlab"
    poem_dir.mkdir(parents=True)
    fontlab_dir.mkdir(parents=True)

    poem_file = poem_dir / "poem.en.md"
    fontlab_file = fontlab_dir / "fontlab-7-tldr.en.md"

    poem_file.write_text("Poem text content", encoding="utf-8")
    fontlab_file.write_text("Fontlab text content", encoding="utf-8")

    # Mock Path resolution in benchmark to use our temp path
    original_path = Path

    def mock_path(*args: Any, **kwargs: Any) -> Any:
        if args and isinstance(args[0], str) and "benchmark.py" in args[0]:
            return original_path(root_dir / "examples" / "benchmark.py")
        return original_path(*args, **kwargs)

    monkeypatch.setattr(benchmark_mod, "Path", mock_path)

    # Mock translate_path to simulate translation
    from abersetz.chunking import TextFormat
    from abersetz.pipeline import TranslationResult

    def mock_translate_path(source: Path, opts: Any, config: Any) -> list[TranslationResult]:
        dest = source.parent / "pl" / source.name
        return [
            TranslationResult(
                source=source,
                destination=dest,
                chunks=1,
                voc={},
                format=TextFormat.PLAIN,
            )
        ]

    monkeypatch.setattr(benchmark_mod, "translate_path", mock_translate_path)

    # Instantiate runner and run with dry-run
    runner = BenchmarkRunner()
    runner.run(engines=["tr/google"], dry_run=True)

    # Verify that the expected json results file was created
    results_json = root_dir / "examples" / "benchmark_results.json"
    assert results_json.exists()

    with open(results_json, encoding="utf-8") as f:
        data = json.load(f)
        assert len(data) == 2
        assert data[0]["engine"] == "tr/google"
        assert data[0]["success"] is True


def test_runner_run_when_no_engines_specified_and_api_key_set_then_discovers_siliconflow(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test runner engine auto-discovery logic when SILICONFLOW_API_KEY is present."""
    root_dir = tmp_path / "mock_project"
    poem_dir = root_dir / "examples" / "data" / "poem"
    fontlab_dir = root_dir / "examples" / "data" / "fontlab"
    poem_dir.mkdir(parents=True)
    fontlab_dir.mkdir(parents=True)

    poem_file = poem_dir / "poem.en.md"
    fontlab_file = fontlab_dir / "fontlab-7-tldr.en.md"
    poem_file.write_text("Poem text content", encoding="utf-8")
    fontlab_file.write_text("Fontlab text content", encoding="utf-8")

    # Mock Path resolution in benchmark to use our temp path
    original_path = Path

    def mock_path(*args: Any, **kwargs: Any) -> Any:
        if args and isinstance(args[0], str) and "benchmark.py" in args[0]:
            return original_path(root_dir / "examples" / "benchmark.py")
        return original_path(*args, **kwargs)

    monkeypatch.setattr(benchmark_mod, "Path", mock_path)
    monkeypatch.setenv("SILICONFLOW_API_KEY", "mock-key")

    mock_cfg = DummyConfig(
        {
            "hysf": DummyEngineConfig("hysf", {}),
            "ullm": DummyEngineConfig("ullm", {}),
            "translators": DummyEngineConfig("translators", {}),
            "deep-translator": DummyEngineConfig("deep-translator", {}),
        }
    )
    monkeypatch.setattr(benchmark_mod, "load_config", lambda: mock_cfg)

    recorded_engines = []

    def mock_translate_path(source: Path, opts: Any, config: Any) -> list[Any]:
        if opts.engine not in recorded_engines:
            recorded_engines.append(opts.engine)
        dest = source.parent / "pl" / source.name
        return [
            TranslationResult(
                source=source,
                destination=dest,
                chunks=1,
                voc={},
                format=TextFormat.PLAIN,
            )
        ]

    from abersetz.chunking import TextFormat
    from abersetz.pipeline import TranslationResult

    monkeypatch.setattr(benchmark_mod, "translate_path", mock_translate_path)

    runner = BenchmarkRunner()
    # Run with engines=None to trigger auto-discovery
    runner.run(engines=None, dry_run=True)

    # Auto-discovered engines should include standard translators plus hysf/ullm when API key is set
    assert "hysf" in recorded_engines
    assert "ullm/default" in recorded_engines


def test_runner_run_when_translate_path_raises_exception_then_captures_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test runner handles exceptions raised by translate_path gracefully."""
    root_dir = tmp_path / "mock_project"
    poem_dir = root_dir / "examples" / "data" / "poem"
    fontlab_dir = root_dir / "examples" / "data" / "fontlab"
    poem_dir.mkdir(parents=True)
    fontlab_dir.mkdir(parents=True)

    poem_file = poem_dir / "poem.en.md"
    fontlab_file = fontlab_dir / "fontlab-7-tldr.en.md"
    poem_file.write_text("Poem text content", encoding="utf-8")
    fontlab_file.write_text("Fontlab text content", encoding="utf-8")

    # Mock Path resolution in benchmark to use our temp path
    original_path = Path

    def mock_path(*args: Any, **kwargs: Any) -> Any:
        if args and isinstance(args[0], str) and "benchmark.py" in args[0]:
            return original_path(root_dir / "examples" / "benchmark.py")
        return original_path(*args, **kwargs)

    monkeypatch.setattr(benchmark_mod, "Path", mock_path)

    def mock_translate_path_failed(source: Path, opts: Any, config: Any) -> list[Any]:
        raise RuntimeError("Network rate limit exceeded")

    monkeypatch.setattr(benchmark_mod, "translate_path", mock_translate_path_failed)

    runner = BenchmarkRunner()
    runner.run(engines=["tr/google"], dry_run=True)

    results_json = root_dir / "examples" / "benchmark_results.json"
    with open(results_json, encoding="utf-8") as f:
        data = json.load(f)
        assert data[0]["success"] is False
        assert "Network rate limit exceeded" in data[0]["error"]


def test_runner_run_when_source_files_missing_then_exits_with_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test runner exits when the test documents are not found."""
    root_dir = tmp_path / "mock_project"

    # Mock Path resolution in benchmark to use our temp path
    original_path = Path

    def mock_path(*args: Any, **kwargs: Any) -> Any:
        if args and isinstance(args[0], str) and "benchmark.py" in args[0]:
            return original_path(root_dir / "examples" / "benchmark.py")
        return original_path(*args, **kwargs)

    monkeypatch.setattr(benchmark_mod, "Path", mock_path)

    runner = BenchmarkRunner()
    with pytest.raises(SystemExit) as excinfo:
        runner.run()
    assert excinfo.value.code == 1


def test_main_when_called_then_invokes_fire() -> None:
    """Test main function invokes fire.Fire correctly."""
    with patch("fire.Fire") as mock_fire:
        main()
        mock_fire.assert_called_once_with(BenchmarkRunner)
