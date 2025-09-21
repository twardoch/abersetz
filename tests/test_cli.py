"""CLI behaviour tests."""
# this_file: tests/test_cli.py

from __future__ import annotations

from pathlib import Path

import pytest

from abersetz.chunking import TextFormat
from abersetz.cli import AbersetzCLI
from abersetz.config import AbersetzConfig, Defaults, EngineConfig
from abersetz.pipeline import TranslationResult, TranslatorOptions


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
        xclude="*.tmp",
        dry_run=True,
    )

    assert calls["path"] == str(tmp_path)
    opts = calls["options"]
    assert isinstance(opts, TranslatorOptions)
    assert opts.include == ("*.txt", "*.md")
    assert opts.xclude == ("*.tmp",)
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


def test_cli_verbose_logs_translation_details(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    class DummyLogger:
        def __init__(self) -> None:
            self.records: list[str] = []

        def remove(self) -> None:  # pragma: no cover - noop in tests
            return None

        def add(self, *args, **kwargs):  # pragma: no cover - noop in tests
            return 1

        def debug(self, message: str, *args, **kwargs) -> None:
            formatted = message.format(*args) if args else message
            self.records.append(formatted)

    dummy_logger = DummyLogger()
    monkeypatch.setattr("abersetz.cli.logger", dummy_logger, raising=False)

    sample_source = tmp_path / "input.txt"
    sample_destination = tmp_path / "pl" / "input.txt"
    result = TranslationResult(
        source=sample_source,
        destination=sample_destination,
        chunks=3,
        voc={},
        format=TextFormat.PLAIN,
        engine="translators/google",
        source_lang="auto",
        target_lang="pl",
        chunk_size=1200,
    )

    def fake_translate_path(path: str, options: TranslatorOptions):
        return [result]

    monkeypatch.setattr("abersetz.cli.translate_path", fake_translate_path)

    printed: list[str] = []
    monkeypatch.setattr("builtins.print", lambda value: printed.append(str(value)))

    cli = AbersetzCLI()
    cli.tr(
        to_lang="pl",
        path=str(sample_source),
        engine="translators/google",
        from_lang="auto",
        verbose=True,
    )

    assert dummy_logger.records == [
        f"Input: {sample_source}",
        "Engine: translators/google (from auto -> pl, chunk_size=1200, format=PLAIN)",
        "Chunks: 3",
        f"Output: {sample_destination}",
    ]
    assert printed == [str(sample_destination)]


def test_cli_engines_lists_configured_providers(monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = AbersetzConfig(
        defaults=Defaults(engine="translators/google"),
        engines={
            "translators": EngineConfig(
                name="translators", options={"providers": ["google", "bing"]}
            ),
            "deep-translator": EngineConfig(
                name="deep-translator", options={"providers": ["google"]}
            ),
        },
    )

    monkeypatch.setattr("abersetz.cli.load_config", lambda: cfg)
    monkeypatch.setattr(
        "abersetz.cli.collect_translator_providers",
        lambda include_paid=False: ["google", "bing", "yandex"],
    )
    monkeypatch.setattr(
        "abersetz.cli.collect_deep_translator_providers",
        lambda include_paid=False: ["google"],
    )

    # Capture what's rendered
    import io

    from rich.console import Console

    output = io.StringIO()
    test_console = Console(file=output, force_terminal=True)
    monkeypatch.setattr("abersetz.cli.console", test_console)

    # The engines method no longer returns entries, just renders them
    AbersetzCLI().engines()

    # Check that the table was rendered with expected content
    table_output = output.getvalue()
    assert table_output  # ensure table rendered
    assert (
        "translators/google" in table_output or "translators/go" in table_output
    )  # May be truncated
    assert "deep-translator/google" in table_output or "deep-translato" in table_output
    assert "tr/google" in table_output or "tr/go" in table_output  # Check shortcut is shown
