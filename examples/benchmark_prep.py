#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#     "fire>=0.5",
#     "rich>=13.9",
#     "abersetz[all]",
# ]
# ///
# this_file: examples/benchmark_prep.py
"""Generate a benchmark job file by enumerating available engine combinations.

Equivalent to ``abersetz ls --job`` across the engines you want to benchmark. The
result is written to ``examples/benchmark_job.json``, which you can then edit
(trim entries, tweak params, set model paths) before feeding it to
``benchmark.py``."""

from __future__ import annotations

import json
from pathlib import Path

import fire  # type: ignore[import-untyped]
from rich.console import Console

from abersetz.job import job_to_dict
from abersetz.listing import build_catalog, catalog_to_job

console = Console()

#: Engine prefixes to enumerate by default. ``ll``/``lm``/``ml``/``gg`` are
#: omitted from the no-argument default because they need API keys or local
#: model scans; pass ``selectors`` explicitly to include them.
DEFAULT_PREFIXES = ("tr", "dt")


def prepare(
    output: str | None = None,
    *,
    selectors: str | None = None,
    to_lang: str = "pl",
    from_lang: str = "en",
    include_paid: bool = False,
    force: bool = False,
) -> None:
    """Build a benchmark job from discovered engine combinations.

    Args:
        output: Where to write the job JSON (default: examples/benchmark_job.json).
        selectors: Comma-separated selector prefixes to enumerate (default: tr,dt).
            Use e.g. 'tr,dt,ll::,ml,gg' to include LLM and local models.
        to_lang: Target language for the generated job.
        from_lang: Source language for the generated job.
        include_paid: Include providers requiring a paid API key.
        force: Bypass discovery caches.
    """
    prefixes = (
        [s.strip() for s in selectors.split(",") if s.strip()]
        if selectors
        else list(DEFAULT_PREFIXES)
    )

    entries = []
    for prefix in prefixes:
        entries.extend(build_catalog(prefix, include_paid=include_paid, force=force))

    job = catalog_to_job(entries, to_lang=to_lang, from_lang=from_lang)
    out_path = Path(output) if output else Path(__file__).resolve().parent / "benchmark_job.json"
    out_path.write_text(
        json.dumps(job_to_dict(job), indent=2, ensure_ascii=False), encoding="utf-8"
    )
    console.print(f"[green]✓[/green] Wrote {len(job.entries)} entries to {out_path}")


def main() -> None:
    fire.Fire(prepare)


if __name__ == "__main__":
    main()
