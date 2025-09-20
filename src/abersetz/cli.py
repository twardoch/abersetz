"""Command line interface for abersetz."""
# this_file: src/abersetz/cli.py

from __future__ import annotations

import json
import sys
from collections.abc import Iterable, Sequence
from pathlib import Path

import fire  # type: ignore
import tomli_w
from loguru import logger
from rich.console import Console

from .config import config_path, load_config
from .pipeline import PipelineError, TranslationResult, TranslatorOptions, translate_path
from .setup import setup_command

console = Console()


def _configure_logging(verbose: bool) -> None:
    logger.remove()
    level = "DEBUG" if verbose else "INFO"
    logger.add(sys.stderr, level=level, enqueue=False)


def _parse_patterns(value: str | Sequence[str] | None) -> tuple[str, ...]:
    if value is None:
        return tuple()
    if isinstance(value, str):
        parts = [item.strip() for item in value.split(",") if item.strip()]
        return tuple(parts)
    return tuple(value)


def _load_json_data(reference: str | None) -> dict[str, str]:
    if not reference:
        return {}
    path = Path(reference)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return json.loads(reference)


def _render_results(results: Iterable[TranslationResult]) -> None:
    # Simple output - just list the output files
    for result in results:
        console.print(str(result.destination))


class ConfigCommands:
    """Configuration related helpers."""

    def show(self) -> str:
        cfg = load_config()
        data = cfg.to_dict()
        toml_output = tomli_w.dumps(data)
        return toml_output

    def path(self) -> str:
        path = str(config_path())
        return path


def _validate_language_code(code: str | None, param_name: str) -> str | None:
    """Validate language code format."""
    if code is None or code == "auto":
        return code

    # Basic validation for common language codes - silently accept
    return code


def _build_options_from_cli(
    path: str | Path,
    *,
    engine: str | None,
    from_lang: str | None,
    to_lang: str,
    recurse: bool,
    write_over: bool,
    output: str | None,
    save_voc: bool,
    chunk_size: int | None,
    html_chunk_size: int | None,
    include: str | Sequence[str] | None,
    xclude: str | Sequence[str] | None,
    dry_run: bool,
    prolog: str | None,
    voc: str | None,
) -> TranslatorOptions:
    # Validate language codes
    from_lang = _validate_language_code(from_lang, "--from-lang")
    to_lang = _validate_language_code(to_lang, "target language")

    return TranslatorOptions(
        to_lang=to_lang,
        engine=engine,
        from_lang=from_lang,
        recurse=recurse,
        write_over=write_over,
        output_dir=Path(output).resolve() if output else None,
        save_voc=save_voc,
        chunk_size=chunk_size,
        html_chunk_size=html_chunk_size,
        include=_parse_patterns(include) or TranslatorOptions().include,
        xclude=_parse_patterns(xclude),
        dry_run=dry_run,
        prolog=_load_json_data(prolog),
        initial_voc=_load_json_data(voc),
    )


def _iter_language_rows() -> list[str]:
    from langcodes import get
    from langcodes.language_lists import CLDR_LANGUAGES

    rows: list[str] = []
    for code in sorted(CLDR_LANGUAGES):
        name = get(code).language_name("en")
        rows.append(f"{code}\t{name}")
    return rows


class AbersetzCLI:
    """Abersetz translation tool - translate files between languages.

    Use 'abersetz tr' to translate files, or 'abersetz config' to manage configuration.
    """

    def version(self) -> str:
        """Show version information."""
        from . import __version__

        console.print(f"abersetz version {__version__}")
        return __version__

    def tr(
        self,
        to_lang: str,
        path: str | Path,
        *,
        engine: str | None = None,
        from_lang: str | None = None,
        recurse: bool = True,
        write_over: bool = False,
        output: str | Path | None = None,
        save_voc: bool = False,
        chunk_size: int | None = None,
        html_chunk_size: int | None = None,
        include: str | Sequence[str] | None = None,
        xclude: str | Sequence[str] | None = None,
        dry_run: bool = False,
        prolog: str | None = None,
        voc: str | None = None,
        verbose: bool = False,
    ) -> None:
        _configure_logging(verbose)
        opts = _build_options_from_cli(
            to_lang=to_lang,
            path=path,
            engine=engine,
            from_lang=from_lang,
            recurse=recurse,
            write_over=write_over,
            output=output,
            save_voc=save_voc,
            chunk_size=chunk_size,
            html_chunk_size=html_chunk_size,
            include=include,
            xclude=xclude,
            dry_run=dry_run,
            prolog=prolog,
            voc=voc,
        )
        try:
            results = translate_path(path, opts)
        except PipelineError as error:
            console.print(f"[red]{error}[/red]")
            raise
        # Minimal output - just print destinations
        for result in results:
            if verbose:
                logger.debug("Input: {}", result.source)
                logger.debug(
                    "Engine: {} (from {} -> {}, chunk_size={}, format={})",
                    result.engine or opts.engine,
                    result.source_lang or (opts.from_lang or "auto"),
                    result.target_lang or (opts.to_lang or ""),
                    result.chunk_size,
                    result.format.name,
                )
                logger.debug("Chunks: {}", result.chunks)
                logger.debug("Output: {}", result.destination)
            print(result.destination)

    def config(self) -> ConfigCommands:
        return ConfigCommands()

    def lang(self) -> list[str]:
        rows = _iter_language_rows()
        for line in rows:
            console.print(line)
        return rows

    def setup(self, non_interactive: bool = False, verbose: bool = False) -> None:
        """Run the configuration setup wizard.

        Args:
            non_interactive: Run without user interaction (for CI/automation)
            verbose: Enable verbose output with detailed logging
        """
        setup_command(non_interactive=non_interactive, verbose=verbose)


def main() -> None:
    """Invoke the Fire CLI."""
    fire.Fire(AbersetzCLI())


def abtr_main() -> None:
    """Direct translation CLI - equivalent to 'abersetz tr'."""

    # Create CLI instance and call tr method directly
    cli = AbersetzCLI()

    # Use Fire to parse arguments for the tr method specifically
    fire.Fire(cli.tr)


__all__ = ["AbersetzCLI", "ConfigCommands", "main", "abtr_main"]
