# this_file: src/abersetz/tasks.py
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from prefect import flow, task

from .pipeline import TranslatorOptions, translate_path

if TYPE_CHECKING:
    from .pipeline import TranslationResult


@task(name="abersetz-translate-task", retries=2)
def translate_task(
    path: Path | str,
    options: TranslatorOptions | None = None,
    client: object | None = None,
) -> list[TranslationResult]:
    """Prefect task to translate a file or directory tree."""
    return translate_path(path, options, client=client)


@flow(name="abersetz-translation-flow")
def translate_flow(
    path: str | Path,
    to_lang: str,
    engine: str | None = None,
    options: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Prefect flow that orchestrates the translation process."""
    opts_dict = dict(options or {})
    opts_dict["to_lang"] = to_lang
    if engine:
        opts_dict["engine"] = engine

    opts = TranslatorOptions(**opts_dict)
    results = translate_task(path, opts)
    return [
        {
            "source": str(r.source),
            "destination": str(r.destination),
            "chunks": r.chunks,
            "format": r.format.value,
            "engine": r.engine,
            "source_lang": r.source_lang,
            "target_lang": r.target_lang,
        }
        for r in results
    ]
