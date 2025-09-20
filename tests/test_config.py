"""Tests for configuration handling."""
# this_file: tests/test_config.py

from __future__ import annotations

import json
from pathlib import Path

import pytest

import abersetz.config as config_module


def test_load_config_yields_defaults(tmp_path: Path) -> None:
    cfg = config_module.load_config()
    assert cfg.defaults.engine == "translators/google"
    assert cfg.defaults.to_lang == "en"
    assert cfg.engines["hysf"].options["model"] == "tencent/Hunyuan-MT-7B"
    assert cfg.credentials["siliconflow"].env == "SILICONFLOW_API_KEY"


def test_save_config_persists_changes(tmp_path: Path) -> None:
    cfg = config_module.load_config()
    cfg.defaults.engine = "deep-translator/google"
    config_module.save_config(cfg)
    stored = json.loads(Path(config_module.config_path()).read_text())
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
