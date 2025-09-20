"""CLI behaviour tests."""
# this_file: tests/test_cli.py

from __future__ import annotations

from pathlib import Path

import pytest

from abersetz.cli import AbersetzCLI
from abersetz.pipeline import TranslatorOptions


def test_cli_translate_wires_arguments(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    calls: dict[str, object] = {}

    def fake_translate_path(path: str, options: TranslatorOptions):
        calls["path"] = path
        calls["options"] = options
        return []

    monkeypatch.setattr("abersetz.cli.translate_path", fake_translate_path)

    cli = AbersetzCLI()
    cli.tr(
        str(tmp_path),
        engine="translators/google",
        include="*.txt,*.md",
        exclude="*.tmp",
        dry_run=True,
    )

    assert calls["path"] == str(tmp_path)
    opts = calls["options"]
    assert isinstance(opts, TranslatorOptions)
    assert opts.include == ("*.txt", "*.md")
    assert opts.exclude == ("*.tmp",)
    assert opts.dry_run is True


def test_cli_config_path_outputs(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: list[str] = []
    monkeypatch.setattr(
        "abersetz.cli.console.print", lambda message, **_: captured.append(str(message))
    )
    cli = AbersetzCLI()
    path = cli.config().path()
    assert captured
    assert Path(path).name == "config.json"
