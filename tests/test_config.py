"""Tests for configuration handling."""
# this_file: tests/test_config.py

from __future__ import annotations

from pathlib import Path

import pytest

import abersetz.config as config_module

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 fallback
    import tomli as tomllib  # type: ignore


def test_load_config_yields_defaults(tmp_path: Path) -> None:
    cfg = config_module.load_config()
    assert cfg.defaults.engine == "translators/google"
    assert cfg.defaults.to_lang == "en"
    assert cfg.engines["hysf"].options["model"] == "tencent/Hunyuan-MT-7B"
    assert cfg.credentials["siliconflow"].env == "SILICONFLOW_API_KEY"
    assert "providers" in cfg.engines["translators"].options
    assert "providers" in cfg.engines["deep-translator"].options


def test_save_config_persists_changes(tmp_path: Path) -> None:
    cfg = config_module.load_config()
    cfg.defaults.engine = "deep-translator/google"
    config_module.save_config(cfg)
    stored = tomllib.loads(Path(config_module.config_path()).read_text(encoding="utf-8"))
    assert stored["defaults"]["engine"] == "deep-translator/google"


def test_resolve_credential_prefers_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = config_module.load_config()
    monkeypatch.setenv("SILICONFLOW_API_KEY", "from_env")
    resolved = config_module.resolve_credential(cfg, cfg.engines["hysf"].credential)
    assert resolved == "from_env"
    monkeypatch.delenv("SILICONFLOW_API_KEY")
    resolved_direct = config_module.resolve_credential(
        cfg,
        {"value": "direct"},
    )
    assert resolved_direct == "direct"


def test_load_config_handles_malformed_toml(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that malformed TOML config files are handled gracefully."""
    # Set custom config dir to tmp_path
    monkeypatch.setenv("ABERSETZ_CONFIG_DIR", str(tmp_path))

    # Write malformed TOML to config file
    config_file = tmp_path / "config.toml"
    config_file.write_text('[defaults\nengine = "invalid"', encoding="utf-8")

    # Should return defaults with a warning instead of crashing
    cfg = config_module.load_config()
    assert cfg.defaults.engine == "translators/google"

    # Config should be reset to defaults
    assert config_file.exists()
    stored = tomllib.loads(config_file.read_text(encoding="utf-8"))
    assert stored["defaults"]["engine"] == "translators/google"


def test_load_config_handles_permission_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Test that permission errors are handled gracefully."""
    # Set custom config dir to tmp_path
    monkeypatch.setenv("ABERSETZ_CONFIG_DIR", str(tmp_path))

    # Create config file and make it unreadable (skip on Windows)
    import platform

    if platform.system() != "Windows":
        config_file = tmp_path / "config.toml"
        config_file.write_text("[defaults]", encoding="utf-8")
        config_file.chmod(0o000)

        # Should return defaults without crashing
        cfg = config_module.load_config()
        assert cfg.defaults.engine == "translators/google"

        # Restore permissions for cleanup
        config_file.chmod(0o644)
