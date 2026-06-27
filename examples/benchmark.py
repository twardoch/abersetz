#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#     "fire>=0.5",
#     "rich>=13.9",
#     "abersetz[all]",
# ]
# ///
# this_file: examples/benchmark.py
"""Benchmark abersetz engines described by a job-JSON file.

Reads an abersetz job (see ``abersetz ls --job`` / ``benchmark_prep.py``),
translates a single input document with every entry, names each output with the
entry's slugified suffix, and writes a JSON timing report.

Engine and model configuration lives entirely in the job file — there are no
hard-coded model paths here."""

from __future__ import annotations

import json
import time
from pathlib import Path

import fire  # type: ignore[import-untyped]
from rich.console import Console
from rich.table import Table

from abersetz.job import load_job
from abersetz.pipeline import TranslatorOptions, translate_path

console = Console()


def _options_for(entry, dry_run: bool) -> TranslatorOptions:
    """Build TranslatorOptions for one job entry."""
    params = entry.params or {}
    return TranslatorOptions(
        engine=entry.selector,
        from_lang=entry.from_lang or "auto",
        to_lang=entry.to_lang or "en",
        chunk_size=entry.chunk_size,
        html_chunk_size=entry.html_chunk_size,
        dry_run=dry_run,
        temperature=params.get("temperature"),
        max_tokens=params.get("max_tokens"),
        n_gpu_layers=params.get("n_gpu_layers"),
        n_ctx=params.get("n_ctx"),
        n_threads=params.get("n_threads"),
    )


def _output_path(input_path: Path, output_dir: Path, to_lang: str, suffix: str) -> Path:
    """Name an output file from the input stem, target language and suffix."""
    return output_dir / f"{input_path.stem}.{to_lang}--{suffix}{input_path.suffix}"


class BenchmarkRunner:
    """Run a benchmark job against one input document."""

    def run(
        self,
        job: str,
        input: str,
        report: str,
        *,
        output_dir: str | None = None,
        force: bool = False,
        dry_run: bool = False,
        verbose: bool = False,
    ) -> None:
        """Benchmark every job entry on ``input`` and write a JSON ``report``.

        Args:
            job: Path to (or inline JSON of) an abersetz job file.
            input: Path to the source document to translate.
            report: Path to write the JSON timing report.
            output_dir: Where to write translated files (defaults to the input's folder).
            force: Re-translate even when an output file already exists.
            dry_run: Skip real API calls (pipeline dry-run).
            verbose: Print per-entry progress.
        """
        job_obj = load_job(job)
        input_path = Path(input).resolve()
        if not input_path.exists():
            console.print(f"[red]Input document not found: {input_path}[/red]")
            raise SystemExit(1)

        out_dir = Path(output_dir).resolve() if output_dir else input_path.parent
        out_dir.mkdir(parents=True, exist_ok=True)
        report_path = Path(report).resolve()

        src_text = input_path.read_text(encoding="utf-8")
        char_count = len(src_text)

        results: list[dict] = []
        for entry in job_obj.resolved_entries():
            suffix = entry.resolved_suffix()
            to_lang = entry.to_lang or "en"
            dest_path = _output_path(input_path, out_dir, to_lang, suffix)

            console.print(f"[bold yellow]{entry.selector}[/bold yellow] -> {dest_path.name}")

            if dest_path.exists() and not force:
                results.append(
                    {
                        "selector": entry.selector,
                        "suffix": suffix,
                        "file": input_path.name,
                        "chars": char_count,
                        "time_s": 0.0,
                        "speed_cps": 0.0,
                        "success": True,
                        "skipped": True,
                        "output": dest_path.name,
                        "error": "",
                    }
                )
                console.print("  - skipped (output exists)", style="yellow")
                continue

            opts = _options_for(entry, dry_run)
            opts.output_dir = out_dir
            start = time.perf_counter()
            success = True
            error_msg = ""
            try:
                produced = translate_path(input_path, opts)
                if produced:
                    res_path = produced[0].destination
                    if res_path != dest_path:
                        if dest_path.exists():
                            dest_path.unlink()
                        res_path.rename(dest_path)
                else:
                    success = False
                    error_msg = "No results returned"
            except Exception as exc:  # noqa: BLE001 - record any engine failure
                success = False
                error_msg = str(exc)
            elapsed = time.perf_counter() - start
            speed = char_count / elapsed if elapsed > 0 else 0.0

            results.append(
                {
                    "selector": entry.selector,
                    "suffix": suffix,
                    "file": input_path.name,
                    "chars": char_count,
                    "time_s": elapsed,
                    "speed_cps": speed,
                    "success": success,
                    "skipped": False,
                    "output": dest_path.name if success else "-",
                    "error": error_msg,
                }
            )
            if success:
                console.print(f"  ✓ {elapsed:.2f}s | {speed:.1f} char/s")
            else:
                console.print(f"  ✗ {error_msg}", style="red")

        self._render(results)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
        console.print(f"\n[green]✓[/green] Report written to {report_path}")

    def _render(self, results: list[dict]) -> None:
        table = Table(title="abersetz benchmark", show_header=True, header_style="bold magenta")
        table.add_column("Selector", style="cyan")
        table.add_column("Status")
        table.add_column("Time (s)", justify="right")
        table.add_column("Speed (cps)", justify="right")
        table.add_column("Output")
        for r in results:
            if r["skipped"]:
                status, t, s = "[yellow]Skipped[/yellow]", "-", "-"
            else:
                status = "[green]OK[/green]" if r["success"] else "[red]Fail[/red]"
                t = f"{r['time_s']:.2f}"
                s = f"{r['speed_cps']:.1f}" if r["success"] else "-"
            table.add_row(str(r["selector"]), status, t, s, str(r["output"]))
        console.print(table)


def main() -> None:
    fire.Fire(BenchmarkRunner)


if __name__ == "__main__":
    main()
