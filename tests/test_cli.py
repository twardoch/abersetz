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
        to_lang="es",
        path=str(tmp_path),
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


def test_cli_config_path_returns_path() -> None:
    cli = AbersetzCLI()
    path = cli.config().path()
    assert Path(path).name == "config.toml"


def test_cli_lang_lists_languages(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: list[str] = []
    monkeypatch.setattr("abersetz.cli.console.print", lambda message: captured.append(str(message)))

    cli = AbersetzCLI()
    rows = cli.lang()

    assert captured  # ensure output emitted
    assert rows == captured
    assert rows[0].startswith("af\t")  # alphabetical by code
