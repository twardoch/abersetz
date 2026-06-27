# this_file: tests/test_local_discovery.py
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from abersetz.providers.llm.local_discovery import LocalModelFinder
from abersetz.providers.mlx import EngineError, resolve_and_download_model


def test_local_model_finder_scans_correctly(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that LocalModelFinder scans directories and finds target formats."""
    # Create mock home directory structure
    mock_home = tmp_path / "home"
    mock_home.mkdir()

    # 1. HuggingFace cache
    hf_path = mock_home / ".cache" / "huggingface" / "hub"
    hf_path.mkdir(parents=True)
    (hf_path / "model.safetensors").write_text(
        "dummy content for safetensors model", encoding="utf-8"
    )
    # Write a small file that should be filtered out by size filter
    (hf_path / "config.json").write_text("{}", encoding="utf-8")

    # 2. Ollama blobs
    ollama_path = mock_home / ".ollama" / "models" / "blobs"
    ollama_path.mkdir(parents=True)
    # Extensionless sha256 blob
    (ollama_path / "sha256-12345abcde").write_text(
        "dummy content for ollama gguf model blob", encoding="utf-8"
    )

    # 3. LM Studio models
    lm_pointer = mock_home / ".lmstudio-home-pointer"
    lm_pointer.write_text(str(mock_home / "custom_lmstudio"), encoding="utf-8")

    lm_models_path = mock_home / "custom_lmstudio" / "models" / "tencent" / "Hy-MT2-7B-GGUF"
    lm_models_path.mkdir(parents=True)
    (lm_models_path / "HY-MT2-7B-Q8_0.gguf").write_text("gguf dummy content", encoding="utf-8")

    # 4. CoreML bundle (directory)
    pinokio_path = mock_home / "pinokio"
    pinokio_path.mkdir()
    coreml_bundle = pinokio_path / "my-model.mlpackage"
    coreml_bundle.mkdir()
    (coreml_bundle / "weights.bin").write_text("coreml weight content", encoding="utf-8")

    # Monkeypatch the home path to our mock home
    finder = LocalModelFinder()
    monkeypatch.setattr(finder, "home", mock_home)
    monkeypatch.setattr("shutil.which", lambda _: None)

    # Scan with a min size of 0 to match our small dummy files
    models = finder.discover_models(min_size_mb=0.0)

    apps = {m.app for m in models}
    formats = {m.format for m in models}

    assert "HuggingFace" in apps
    assert "Ollama" in apps
    assert "LMStudio" in apps
    assert "Pinokio" in apps

    assert "Safetensors" in formats
    assert "GGUF" in formats
    assert "CoreML" in formats

    # Test filtering by format
    gguf_models = finder.discover_models(format_filter="gguf", min_size_mb=0.0)
    assert all(m.format == "GGUF" for m in gguf_models)
    assert len(gguf_models) == 2  # Ollama blob and LM Studio gguf


def test_resolve_local_situation_model(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that resolve_and_download_model detects and prefers local discovered models."""
    mock_home = tmp_path / "home"

    # Create LMStudio mock path and a mock model file
    lm_models_path = mock_home / ".cache" / "lm-studio" / "models" / "tencent" / "Hy-MT2-1.8B-GGUF"
    lm_models_path.mkdir(parents=True)
    model_file = lm_models_path / "Hy-MT2-1.8B-Q8_0.gguf"
    model_file.write_text("model weights", encoding="utf-8")

    # Monkeypatch Path.home so it queries mock_home
    monkeypatch.setattr(Path, "home", lambda: mock_home)
    monkeypatch.setattr("shutil.which", lambda _: None)

    # Monkeypatch Path.stat to simulate files larger than 100MB
    original_stat = Path.stat

    def mock_stat(self, *args, **kwargs):
        res = original_stat(self, *args, **kwargs)

        class MockStat:
            def __init__(self, orig):
                self._orig = orig

            @property
            def st_size(self):
                return 200 * 1024 * 1024

            def __getattr__(self, name):
                return getattr(self._orig, name)

        return MockStat(res)

    monkeypatch.setattr(Path, "stat", mock_stat)

    # Monkeypatch Path.exists to isolate tests from real filesystems
    original_exists = Path.exists

    def mock_exists(self, *args, **kwargs):
        try:
            self.resolve().relative_to(mock_home.resolve())
            return original_exists(self, *args, **kwargs)
        except ValueError:
            return False

    monkeypatch.setattr(Path, "exists", mock_exists)

    # 1. Resolve alias "1.8b-gguf" -> tencent/Hy-MT2-1.8B-GGUF -> should find model_file
    resolved = resolve_and_download_model("1.8b-gguf", "gguf")
    assert resolved == str(model_file.resolve())

    # 2. Resolve MLX alias "1.8b-mlx" which doesn't exist locally -> should try snapshot_download
    # We mock snapshot_download to verify it falls back to it
    download_called = False

    def mock_snapshot_download(repo_id: str, **kwargs) -> str:
        nonlocal download_called
        download_called = True
        return "/downloaded/path"

    monkeypatch.setattr("huggingface_hub.snapshot_download", mock_snapshot_download)
    resolved_mlx = resolve_and_download_model("1.8b-mlx", "mlx")
    assert download_called is True
    assert resolved_mlx == "/downloaded/path"


def test_obsolete_model_rejection() -> None:
    """Test that legacy Hunyuan-MT1.x models raise EngineError."""
    with pytest.raises(EngineError) as excinfo:
        resolve_and_download_model("Hunyuan-MT-7B", "mlx")
    assert "no longer supported" in str(excinfo.value)

    with pytest.raises(EngineError) as excinfo:
        resolve_and_download_model("tencent/Hunyuan-MT-7B-GGUF", "gguf")
    assert "no longer supported" in str(excinfo.value)


def test_resolve_local_mlx_situation_model(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that resolve_and_download_model detects local MLX models and returns their parent folder path."""
    mock_home = tmp_path / "home"

    # Create HF hub mock path with a weights file inside snapshots
    mlx_model_path = (
        mock_home
        / ".cache"
        / "huggingface"
        / "hub"
        / "models--p0we7--Hy-MT2-1.8B-oQ8-fp16"
        / "snapshots"
        / "1234abcd"
    )
    mlx_model_path.mkdir(parents=True)
    weights_file = mlx_model_path / "weights.safetensors"
    weights_file.write_text("mlx model weights", encoding="utf-8")

    # Monkeypatch Path.home so it queries mock_home
    monkeypatch.setattr(Path, "home", lambda: mock_home)
    monkeypatch.setattr("shutil.which", lambda _: None)

    # Monkeypatch Path.stat to simulate files larger than 100MB
    original_stat = Path.stat

    def mock_stat(self, *args, **kwargs):
        res = original_stat(self, *args, **kwargs)

        class MockStat:
            def __init__(self, orig):
                self._orig = orig

            @property
            def st_size(self):
                return 200 * 1024 * 1024

            def __getattr__(self, name):
                return getattr(self._orig, name)

        return MockStat(res)

    monkeypatch.setattr(Path, "stat", mock_stat)

    # Monkeypatch Path.exists to isolate tests from real filesystems
    original_exists = Path.exists

    def mock_exists(self, *args, **kwargs):
        try:
            self.resolve().relative_to(mock_home.resolve())
            return original_exists(self, *args, **kwargs)
        except ValueError:
            return False

    monkeypatch.setattr(Path, "exists", mock_exists)

    # Resolve MLX alias "1.8b-mlx" which should find weights_file but return snapshot dir
    resolved = resolve_and_download_model("1.8b-mlx", "mlx")
    assert resolved == str(mlx_model_path.resolve())


def test_local_model_finder_uses_lmstudio_cli_grouped_models(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that LM Studio discovery uses `lms ls --json` grouped model entries."""
    mock_home = tmp_path / "home"
    lmstudio_home = mock_home / "lmstudio"
    lm_models_path = lmstudio_home / "models"
    lm_models_path.mkdir(parents=True)
    mock_home.mkdir(exist_ok=True)
    (mock_home / ".lmstudio-home-pointer").write_text(str(lmstudio_home), encoding="utf-8")

    finder = LocalModelFinder()
    monkeypatch.setattr(finder, "home", mock_home)
    monkeypatch.setattr("shutil.which", lambda _: "/usr/local/bin/lms")

    payload = """[
      {
        "modelKey": "qwen3-test",
        "format": "safetensors",
        "path": "publisher/qwen3-test",
        "sizeBytes": 209715200
      },
      {
        "modelKey": "small-skipped",
        "format": "gguf",
        "path": "publisher/small-skipped",
        "sizeBytes": 1
      }
    ]"""

    def fake_run(*args, **kwargs):
        kwargs["stdout"].write(payload)
        return SimpleNamespace()

    monkeypatch.setattr("subprocess.run", fake_run)

    models = finder.discover_models(min_size_mb=100.0)

    assert len(models) == 1
    assert models[0].name == "qwen3-test"
    assert models[0].app == "LMStudio"
    assert models[0].format == "Safetensors"
    assert models[0].path == lm_models_path / "publisher" / "qwen3-test"
