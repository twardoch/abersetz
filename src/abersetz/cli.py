"""Command line interface for abersetz."""
# this_file: src/abersetz/cli.py

from __future__ import annotations

import json
import sys
from collections.abc import Iterable, Sequence
from pathlib import Path

import fire  # type: ignore
from loguru import logger
from rich.console import Console
from rich.table import Table

from .config import config_path, load_config
from .pipeline import PipelineError, TranslationResult, TranslatorOptions, translate_path

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
    table = Table(title="abersetz results")
    table.add_column("Source")
    table.add_column("Destination")
    table.add_column("Chunks", justify="right")
    table.add_column("Format")
    for result in results:
        table.add_row(
            str(result.source),
            str(result.destination),
            str(result.chunks),
            result.format.value,
        )
    console.print(table)


class ConfigCommands:
    """Configuration related helpers."""

    def show(self) -> dict[str, object]:
        cfg = load_config()
        data = cfg.to_dict()
        console.print_json(data=data)
        return data

    def path(self) -> str:
        path = str(config_path())
        console.print(path)
        return path


def _build_options_from_cli(
    path: str | Path,
    *,
    engine: str | None,
    from_lang: str | None,
    to_lang: str | None,
    recurse: bool,
    overwrite: bool,
    output: str | None,
    save_voc: bool,
    chunk_size: int | None,
    html_chunk_size: int | None,
    include: str | Sequence[str] | None,
    exclude: str | Sequence[str] | None,
    dry_run: bool,
    prolog: str | None,
    vocabulary: str | None,
) -> TranslatorOptions:
    return TranslatorOptions(
        engine=engine,
        from_lang=from_lang,
        to_lang=to_lang,
        recurse=recurse,
        overwrite=overwrite,
        output_dir=Path(output).resolve() if output else None,
        save_vocabulary=save_voc,
        chunk_size=chunk_size,
        html_chunk_size=html_chunk_size,
        include=_parse_patterns(include) or TranslatorOptions().include,
        exclude=_parse_patterns(exclude),
        dry_run=dry_run,
        prolog=_load_json_data(prolog),
        initial_vocabulary=_load_json_data(vocabulary),
    )


class AbersetzCLI:
    """Fire-powered entrypoint."""

    def translate(
        self,
        path: str,
        *,
        engine: str | None = None,
        from_lang: str | None = None,
        to_lang: str | None = None,
        recurse: bool = True,
        overwrite: bool = False,
        output: str | None = None,
        save_voc: bool = False,
        chunk_size: int | None = None,
        html_chunk_size: int | None = None,
        include: str | Sequence[str] | None = None,
        exclude: str | Sequence[str] | None = None,
        dry_run: bool = False,
        prolog: str | None = None,
        vocabulary: str | None = None,
        verbose: bool = False,
    ) -> list[str]:
        _configure_logging(verbose)
        opts = _build_options_from_cli(
            path,
            engine=engine,
            from_lang=from_lang,
            to_lang=to_lang,
            recurse=recurse,
            overwrite=overwrite,
            output=output,
            save_voc=save_voc,
            chunk_size=chunk_size,
            html_chunk_size=html_chunk_size,
            include=include,
            exclude=exclude,
            dry_run=dry_run,
            prolog=prolog,
            vocabulary=vocabulary,
        )
        try:
            results = translate_path(path, opts)
        except PipelineError as error:
            console.print(f"[red]{error}[/red]")
            raise
        _render_results(results)
        return [str(item.destination) for item in results]

    def config(self) -> ConfigCommands:
        return ConfigCommands()


def main() -> None:
    """Invoke the Fire CLI."""
    fire.Fire(AbersetzCLI)


__all__ = ["AbersetzCLI", "ConfigCommands", "main"]
