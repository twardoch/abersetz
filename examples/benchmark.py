#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#     "fire>=0.5",
#     "rich>=13.9",
# ]
# ///
# this_file: examples/benchmark.py

import contextlib
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import fire  # type: ignore[import-untyped]
from rich.console import Console
from rich.table import Table

# Add src/ to sys.path to run from source if not installed
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from abersetz.config import load_config
from abersetz.engine_catalog import normalize_selector
from abersetz.pipeline import TranslatorOptions, translate_path

console = Console()


MODEL_PATHS = {
    # MLX
    "30b-mlx": "/Volumes/Falstaff4T/RomeoData2/lmstudio/models/QwQbb/Hy-MT2-30B-A3B-MLX-4bit",
    "1.8b-mlx": "/Volumes/Falstaff4T/RomeoData2/lmstudio/models/p0we7/Hy-MT2-1.8B-oQ8-fp16",
    # GGUF
    "7b-gguf": "/Volumes/Falstaff4T/RomeoData2/lmstudio/models/tencent/Hy-MT2-7B-GGUF/HY-MT2-7B-Q8_0.gguf",
    "1.8b-heretic": "/Volumes/Falstaff4T/RomeoData2/lmstudio/models/mradermacher/Hy-MT2-1.8B-heretic-GGUF/Hy-MT2-1.8B-heretic.Q8_0.gguf",
    "1.8b-gguf": "/Volumes/Falstaff4T/RomeoData2/lmstudio/models/tencent/Hy-MT2-1.8B-GGUF/Hy-MT2-1.8B-Q8_0.gguf",
    "1.8b-2bit": "/Volumes/Falstaff4T/RomeoData2/lmstudio/models/tencent/Hy-MT2-1.8B-2Bit-GGUF/Hy-MT2-1.8B-2Bit.gguf",
    "1.8b-1.25bit": "/Volumes/Falstaff4T/RomeoData2/lmstudio/models/tencent/Hy-MT2-1.8B-1.25Bit-GGUF/Hy-MT2-1.8B-1.25Bit.gguf",
}


def sanitize_name(name: str) -> str:
    """Make a name safe for filenames by replacing non-alphanumeric chars with hyphens."""
    return re.sub(r"[^a-zA-Z0-9_-]", "-", name).strip("-")


def get_engine_descriptor(selector: str, cfg: Any) -> str:
    """Build a detailed descriptor (NNN) from engine config without initializing it."""
    from abersetz.engine_catalog import resolve_engine_reference

    selector_norm = normalize_selector(selector) or selector
    base, variant = resolve_engine_reference(selector_norm)

    if base == "mthy" and variant in MODEL_PATHS:
        backend = "mlx" if "mlx" in variant else "gguf"
        return f"mthy-{backend}-{variant}"

    if base == "ullm" and variant == "lmstudio":
        return "ullm-lmstudio-local-model"

    engine_cfg = cfg.engines.get(base)
    if not engine_cfg:
        return sanitize_name(selector_norm)

    if base == "translators":
        provider = variant or engine_cfg.options.get("provider", "google")
        return f"tr-{provider}"
    if base == "deep-translator":
        provider = variant or engine_cfg.options.get("provider", "google")
        return f"dt-{provider}"
    if base == "hysf":
        model = engine_cfg.options.get("model", "Hunyuan-MT-7B")
        return f"hysf-siliconflow-{sanitize_name(model)}"
    if base == "ullm":
        profile_name = variant or "default"
        profiles = engine_cfg.options.get("profiles", {})
        profile = profiles.get(profile_name, {}) if isinstance(profiles, dict) else {}
        model = profile.get("model", "Hunyuan-MT-7B")
        return f"ullm-{profile_name}-{sanitize_name(model)}"
    if base in {"mthy", "gemma"}:
        backend = variant or engine_cfg.options.get("backend", "local")
        model_path = engine_cfg.options.get("model_path") or engine_cfg.options.get(
            f"{backend}_path"
        )
        model_name = Path(model_path).name if model_path else "default"
        return f"{base}-{backend}-{sanitize_name(model_name)}"

    return sanitize_name(selector_norm)


class BenchmarkRunner:
    """Benchmark Abersetz translation engines on example files."""

    def run(
        self,
        engines: str | list[str] | None = None,
        max_chunks: int | None = None,
        dry_run: bool = False,
        verbose: bool = False,
    ) -> None:
        """Run the speed benchmark.

        Args:
            engines: Comma-separated selectors or list of selectors. Defaults to auto-discovered.
            max_chunks: Limit the number of chunks translated per file (useful for fast tests).
            dry_run: Perform a dry run without invoking external translation APIs.
            verbose: Enable verbose logging outputs.
        """
        cfg = load_config()

        # 1. Resolve engines
        target_engines: list[str] = []
        if isinstance(engines, str):
            target_engines = [e.strip() for e in engines.split(",") if e.strip()]
        elif isinstance(engines, list):
            target_engines = engines
        else:
            # Auto-discover working engines
            target_engines = ["tr/google", "tr/bing", "dt/google", "dt/my_memory"]
            # Add siliconflow models if API key present
            if os.environ.get("SILICONFLOW_API_KEY"):
                if "hysf" in cfg.engines:
                    target_engines.append("hysf")
                if "ullm" in cfg.engines:
                    target_engines.append("ullm/default")
            # Add all local models and LMStudio
            for model_key in MODEL_PATHS:
                target_engines.append(f"mthy/{model_key}")
            target_engines.append("ullm/lmstudio")

        console.print("\n[bold cyan]🚀 Starting Abersetz Speed Benchmark[/bold cyan]")
        console.print(f"Target Engines: {', '.join(target_engines)}")
        console.print(f"Dry Run: {dry_run} | Max Chunks: {max_chunks}\n")

        # Example files paths
        root_dir = Path(__file__).resolve().parents[1]
        poem_path = root_dir / "examples" / "data" / "poem" / "poem.en.md"
        fontlab_path = root_dir / "examples" / "data" / "fontlab" / "fontlab-7-tldr.en.md"

        if not poem_path.exists() or not fontlab_path.exists():
            console.print("[red]Error: Example source files not found under ./examples/data/[/red]")
            sys.exit(1)

        benchmarks = []

        # Setup mock context or custom creation wrapping
        translation_ctx: Any
        from abersetz.engine_catalog import resolve_engine_reference

        if dry_run:
            from unittest.mock import patch

            from abersetz.engines import EngineBase, EngineResult

            class BenchmarkDummyEngine(EngineBase):
                def translate(self, request):
                    time.sleep(0.005)
                    return EngineResult(
                        text=f"[Mock translation to pl]: {request.text}", voc=dict(request.voc)
                    )

            def dummy_create_engine(selector_str, config_obj, client=None):
                normalized = normalize_selector(selector_str) or selector_str
                base, variant = resolve_engine_reference(normalized)

                # Dynamically mock configuration changes so it mirrors real initialization
                if base == "mthy" and variant in MODEL_PATHS:
                    backend = "mlx" if "mlx" in variant else "gguf"
                    resolved_path = MODEL_PATHS[variant]
                    from abersetz.config import EngineConfig

                    if "mthy" not in config_obj.engines:
                        config_obj.engines["mthy"] = EngineConfig(name="mthy", options={})
                    config_obj.engines["mthy"].options["backend"] = backend
                    config_obj.engines["mthy"].options[f"{backend}_path"] = resolved_path

                if base == "ullm" and variant == "lmstudio":
                    from abersetz.config import EngineConfig

                    if "ullm" not in config_obj.engines:
                        config_obj.engines["ullm"] = EngineConfig(name="ullm", options={})
                    config_obj.engines["ullm"].options.setdefault("profiles", {})
                    config_obj.engines["ullm"].options["profiles"]["lmstudio"] = {
                        "base_url": "http://localhost:1234/v1",
                        "model": "local-model",
                        "temperature": 0.3,
                    }

                engine_cfg = config_obj.engines.get(base)
                chunk_size = engine_cfg.chunk_size if engine_cfg else None
                html_chunk_size = engine_cfg.html_chunk_size if engine_cfg else None
                return BenchmarkDummyEngine(normalized, chunk_size, html_chunk_size)

            translation_ctx = patch("abersetz.pipeline.create_engine", dummy_create_engine)
        else:
            from unittest.mock import patch

            from abersetz.engines import create_engine as real_create_engine

            def wrapped_create_engine(selector_str, config_obj, client=None):
                normalized = normalize_selector(selector_str) or selector_str
                base, variant = resolve_engine_reference(normalized)

                if base == "mthy" and variant in MODEL_PATHS:
                    backend = "mlx" if "mlx" in variant else "gguf"
                    resolved_path = MODEL_PATHS[variant]
                    from abersetz.config import EngineConfig

                    if "mthy" not in config_obj.engines:
                        config_obj.engines["mthy"] = EngineConfig(name="mthy", options={})
                    config_obj.engines["mthy"].options["backend"] = backend
                    config_obj.engines["mthy"].options[f"{backend}_path"] = resolved_path
                    return real_create_engine(f"mthy/{backend}", config_obj, client=client)

                if base == "ullm" and variant == "lmstudio":
                    from abersetz.config import EngineConfig

                    if "ullm" not in config_obj.engines:
                        config_obj.engines["ullm"] = EngineConfig(name="ullm", options={})
                    config_obj.engines["ullm"].options.setdefault("profiles", {})
                    config_obj.engines["ullm"].options["profiles"]["lmstudio"] = {
                        "base_url": "http://localhost:1234/v1",
                        "model": "local-model",
                        "temperature": 0.3,
                    }
                    return real_create_engine(selector_str, config_obj, client=client)

                return real_create_engine(selector_str, config_obj, client=client)

            translation_ctx = patch("abersetz.pipeline.create_engine", wrapped_create_engine)

        with translation_ctx:
            # Run translation for each engine
            for selector in target_engines:
                descriptor = get_engine_descriptor(selector, cfg)
                console.print(
                    f"\n[bold yellow]Testing engine: {selector} ({descriptor})[/bold yellow]"
                )

                for source_file, out_pattern in [
                    (poem_path, "poem.pl--{desc}.md"),
                    (fontlab_path, "fontlab-7-tldr.pl--{desc}.md"),
                ]:
                    dest_filename = out_pattern.format(desc=descriptor)
                    dest_path = source_file.parent / dest_filename

                    opts = TranslatorOptions(
                        engine=selector,
                        to_lang="pl",
                        from_lang="en",
                        output_dir=None,
                        write_over=False,
                        dry_run=dry_run,
                        chunk_size=max_chunks * 200 if max_chunks else None,
                    )

                    # Read source to count characters
                    src_text = source_file.read_text(encoding="utf-8")
                    char_count = len(src_text)

                    start_time = time.perf_counter()
                    success = True
                    error_msg = ""

                    try:
                        # Execute translation
                        results = translate_path(source_file, opts, config=cfg)
                        if results:
                            # Rename output to the required format
                            res_path = results[0].destination
                            if res_path.exists() and res_path != dest_path:
                                if dest_path.exists():
                                    dest_path.unlink()
                                res_path.rename(dest_path)
                            # Clean up the empty target-lang directory
                            with contextlib.suppress(OSError):
                                res_path.parent.rmdir()
                        else:
                            success = False
                            error_msg = "No results returned"
                    except Exception as e:
                        success = False
                        error_msg = str(e)

                    elapsed = time.perf_counter() - start_time
                    chars_per_sec = char_count / elapsed if elapsed > 0 else 0

                    benchmarks.append(
                        {
                            "engine": selector,
                            "descriptor": descriptor,
                            "file": source_file.name,
                            "chars": char_count,
                            "time_s": elapsed,
                            "speed_cps": chars_per_sec,
                            "success": success,
                            "output": dest_filename if success else "-",
                            "error": error_msg,
                        }
                    )

                    if success:
                        console.print(
                            f"  ✓ {source_file.name} -> {dest_filename} | "
                            f"Time: {elapsed:.2f}s | Speed: {chars_per_sec:.1f} char/s"
                        )
                    else:
                        console.print(f"  ✗ {source_file.name} failed: {error_msg}", style="red")

        # 2. Render Benchmark Results Table
        table = Table(
            title="Abersetz Translation Benchmark Summary",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Engine", style="cyan")
        table.add_column("File", style="yellow")
        table.add_column("Status")
        table.add_column("Time (s)", justify="right")
        table.add_column("Speed (cps)", justify="right")
        table.add_column("Output File")

        for b in benchmarks:
            status = "[green]Success[/green]" if b["success"] else "[red]Failed[/red]"
            time_str = f"{b['time_s']:.2f}"
            speed_str = f"{b['speed_cps']:.1f}" if b["success"] else "-"
            table.add_row(
                str(b["engine"]),
                str(b["file"]),
                status,
                time_str,
                speed_str,
                str(b["output"]),
            )

        console.print("\n")
        console.print(table)

        # 3. Save benchmark summary results
        summary_path = root_dir / "examples" / "benchmark_results.json"
        summary_path.write_text(json.dumps(benchmarks, indent=2), encoding="utf-8")
        console.print(f"\n[green]✓[/green] Benchmark JSON saved to {summary_path}")


def main() -> None:
    fire.Fire(BenchmarkRunner)


if __name__ == "__main__":
    main()
