"""Command line interface for abersetz.

The user-facing CLI. This translates terminal commands into pipeline options, formats output nicely with Rich, and handles the `abersetz tr` and `abersetz config` subcommands."""
# this_file: src/abersetz/cli.py

from __future__ import annotations

import json
import os
import sys
from collections.abc import Iterable, Sequence
from pathlib import Path

import fire  # type: ignore
import tomli_w
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="WARNING", enqueue=False)

from rich.console import Console  # noqa: E402
from rich.table import Table  # noqa: E402

from .config import config_path, load_config  # noqa: E402
from .engine_catalog import (  # noqa: E402
    DEEP_TRANSLATOR_PAID_PROVIDERS,
    PAID_TRANSLATOR_PROVIDERS,
    EngineEntry,
    collect_deep_translator_providers,
    collect_translator_providers,
    normalize_selector,
)

with open(os.devnull, "w") as devnull:
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = devnull
    sys.stderr = devnull
    try:
        from .pipeline import (  # noqa: E402
            PipelineError,
            TranslationResult,
            TranslatorOptions,
            translate_path,
            translate_string,
        )
        from .setup import setup_command  # noqa: E402
        from .validation import ValidationResult, validate_engines  # noqa: E402
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr

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


def _render_engine_entries(entries: list[EngineEntry]) -> None:
    if not entries:
        console.print("No engines detected.")
        return
    table = Table(title="Available Translation Engines", show_header=True, header_style="bold cyan")
    table.add_column("Selector", style="white")
    table.add_column("Family", style="cyan")
    table.add_column("Configured", style="green")
    table.add_column("Credential", style="yellow")
    table.add_column("Notes", style="magenta")

    for entry in entries:
        base = entry.selector.split("/", 1)[0]
        table.add_row(
            entry.selector,
            base,
            "✓" if entry.configured else "✗",
            "required" if entry.requires_api_key else "free",
            entry.notes,
        )
    console.print(table)


def _render_validation_entries(results: list[ValidationResult]) -> None:
    if not results:
        console.print("No engines available for validation.")
        return

    table = Table(title="Engine Validation", show_header=True, header_style="bold cyan")
    table.add_column("Selector", style="white")
    table.add_column("Status", style="green")
    table.add_column("Latency (s)", justify="right", style="yellow")
    table.add_column("Sample Output", style="magenta")
    table.add_column("Error", style="red")

    for result in results:
        status = "[green]✓[/green]" if result.success else "[red]✗[/red]"
        latency = f"{result.latency:.2f}"
        sample = result.translation[:80]
        error = result.error or ""
        table.add_row(result.selector, status, latency, sample, error)

    console.print(table)


def _collect_engine_entries(
    include_paid: bool,
    *,
    family: str | None = None,
    configured_only: bool = False,
) -> list[EngineEntry]:
    cfg = load_config()
    entries: list[EngineEntry] = []

    # translators engine
    translator_cfg = cfg.engines.get("translators")
    entries.append(
        EngineEntry(
            selector=str(normalize_selector("translators")),
            configured=translator_cfg is not None,
            requires_api_key=False,
            notes="use tr/<provider>",
        )
    )
    configured_translators: list[str] = []
    if translator_cfg:
        providers_value = translator_cfg.options.get("providers")
        if isinstance(providers_value, list | tuple):
            configured_translators.extend(str(p).strip() for p in providers_value if str(p).strip())
        elif isinstance(providers_value, str) and providers_value.strip():
            configured_translators.append(providers_value.strip())
        single_provider = translator_cfg.options.get("provider")
        if isinstance(single_provider, str) and single_provider.strip():
            configured_translators.append(single_provider.strip())
    available_translators = collect_translator_providers(include_paid=include_paid)
    translator_candidates = sorted(
        {
            *configured_translators,
            *available_translators,
        },
        key=str.lower,
    )
    for provider in translator_candidates:
        selector = str(normalize_selector(f"translators/{provider}"))
        notes = "free" if provider not in PAID_TRANSLATOR_PROVIDERS else "requires API"
        entries.append(
            EngineEntry(
                selector=selector,
                configured=provider in configured_translators,
                requires_api_key=provider in PAID_TRANSLATOR_PROVIDERS,
                notes=notes,
            )
        )

    # deep-translator engine
    deep_cfg = cfg.engines.get("deep-translator")
    entries.append(
        EngineEntry(
            selector=str(normalize_selector("deep-translator")),
            configured=deep_cfg is not None,
            requires_api_key=False,
            notes="use dt/<provider>",
        )
    )
    configured_deep: list[str] = []
    if deep_cfg:
        providers_value = deep_cfg.options.get("providers")
        if isinstance(providers_value, list | tuple):
            configured_deep.extend(str(p).strip() for p in providers_value if str(p).strip())
        elif isinstance(providers_value, str) and providers_value.strip():
            configured_deep.append(providers_value.strip())
        single_provider = deep_cfg.options.get("provider")
        if isinstance(single_provider, str) and single_provider.strip():
            configured_deep.append(single_provider.strip())
    available_deep = collect_deep_translator_providers(include_paid=include_paid)
    deep_candidates = sorted({*configured_deep, *available_deep}, key=str.lower)
    for provider in deep_candidates:
        selector = str(normalize_selector(f"deep-translator/{provider}"))
        notes = "free" if provider not in DEEP_TRANSLATOR_PAID_PROVIDERS else "requires API"
        entries.append(
            EngineEntry(
                selector=selector,
                configured=provider in configured_deep,
                requires_api_key=provider in DEEP_TRANSLATOR_PAID_PROVIDERS,
                notes=notes,
            )
        )

    # lmstudio engine
    if "lmstudio" in cfg.engines:
        entries.append(
            EngineEntry(
                selector=str(normalize_selector("lmstudio")),
                configured=True,
                requires_api_key=False,
                notes="local",
            )
        )

    for local_name in ("mthy", "gemma"):
        local_cfg = cfg.engines.get(local_name)
        if local_cfg:
            backend = str(local_cfg.options.get("backend", "")).strip()
            selector = f"{local_name}/{backend}" if backend else local_name
            entries.append(
                EngineEntry(
                    selector=selector,
                    configured=True,
                    requires_api_key=False,
                    notes=backend or "local",
                )
            )

    ullm_cfg = cfg.engines.get("ullm")
    if ullm_cfg:
        profiles = ullm_cfg.options.get("profiles", {})
        if isinstance(profiles, dict):
            for profile_name in sorted(profiles):
                selector = str(normalize_selector(f"ullm/{profile_name}"))
                entries.append(
                    EngineEntry(
                        selector=selector,
                        configured=True,
                        requires_api_key=True,
                        notes=profiles[profile_name].get("model", ""),
                    )
                )
        else:
            entries.append(
                EngineEntry(
                    selector=str(normalize_selector("ullm/default")),
                    configured=True,
                    requires_api_key=True,
                    notes="",
                )
            )

    if family:
        family_selector = normalize_selector(family)
        base = (family_selector or family).split("/", 1)[0].strip().lower()
        entries = [entry for entry in entries if entry.selector.split("/", 1)[0] == base]

    if configured_only:
        entries = [entry for entry in entries if entry.configured]

    return entries


class ConfigCommands:
    """Configuration related helpers.

    Subcommands under `abersetz config` to show the current setup or print the config file path."""

    def show(self) -> str:
        """Show current configuration as TOML.

        Reads the configuration from disk (or default settings) and prints the serialization.

        Returns:
            str: The configuration formatted as TOML.
        """
        cfg = load_config()
        data = cfg.to_dict()
        toml_output = tomli_w.dumps(data)
        return toml_output

    def path(self) -> str:
        """Print the absolute path to the configuration file.

        Returns:
            str: The path to the config file on the local filesystem.
        """
        path = str(config_path())
        return path


def _validate_language_code(code: str | None, param_name: str) -> str | None:
    """Validate language code format.

    Ensures the user didn't pass gibberish for a language code, though currently it mostly trusts the user."""
    if code is None or code == "auto":
        return code

    # Basic validation for common language codes - silently accept
    return code


def _build_options_from_cli(
    path: str | Path,
    *,
    engine: str | None,
    from_lang: str | None,
    to_lang: str | None,
    recurse: bool,
    write_over: bool,
    output: str | Path | None,
    save_voc: bool,
    chunk_size: int | None,
    html_chunk_size: int | None,
    include: str | Sequence[str] | None,
    xclude: str | Sequence[str] | None,
    dry_run: bool,
    prolog: str | None,
    voc: str | None,
    temperature: float | None = None,
    n_gpu_layers: int | None = None,
    n_ctx: int | None = None,
    max_tokens: int | None = None,
    n_threads: int | None = None,
) -> TranslatorOptions:
    # Validate language codes
    validated_from_lang = _validate_language_code(from_lang, "--from-lang")
    validated_to_lang = _validate_language_code(to_lang, "target language")
    if validated_to_lang is None:
        raise ValueError("Target language is required")

    normalized_engine = normalize_selector(engine) if engine else None

    output_dir: Path | None
    output_dir = None if output is None else Path(output).resolve()

    return TranslatorOptions(
        to_lang=validated_to_lang,
        engine=normalized_engine,
        from_lang=validated_from_lang,
        recurse=recurse,
        write_over=write_over,
        output_dir=output_dir,
        save_voc=save_voc,
        chunk_size=chunk_size,
        html_chunk_size=html_chunk_size,
        include=_parse_patterns(include) or TranslatorOptions().include,
        xclude=_parse_patterns(xclude),
        dry_run=dry_run,
        prolog=_load_json_data(prolog),
        initial_voc=_load_json_data(voc),
        temperature=temperature,
        n_gpu_layers=n_gpu_layers,
        n_ctx=n_ctx,
        max_tokens=max_tokens,
        n_threads=n_threads,
    )


def _iter_language_rows() -> list[str]:
    from langcodes import get
    from langcodes.language_lists import CLDR_LANGUAGES

    rows: list[str] = []
    for code in sorted(CLDR_LANGUAGES):
        name = get(code).language_name("en")
        rows.append(f"{code}\t{name}")
    return rows


POPULAR_LANG_CODES = ("en", "es", "fr", "de", "ja", "zh-CN", "pl")


class AbersetzCLI:
    """Abersetz translation tool.

    The main CLI application. Exposes `tr` for translation, `config` for settings, `lang` for language codes, and `engines` to see what backends are available.
    """

    def version(self) -> str:
        """Show version information.

        Prints the current version of abersetz."""
        from . import __version__

        console.print(f"abersetz version {__version__}")
        return __version__

    def _translate_files(
        self,
        to_lang: str,
        path: str | Path,
        *,
        engine: str | None = None,
        from_lang: str | None = None,
        recurse: bool = True,
        write_over: bool | None = None,
        Overwrite: bool = False,
        output: str | Path | None = None,
        save_voc: bool = False,
        chunk_size: int | None = None,
        html_chunk_size: int | None = None,
        include: str | Sequence[str] | None = None,
        xclude: str | Sequence[str] | None = None,
        dry_run: bool = False,
        prolog: str | None = None,
        voc: str | None = None,
        Vocabulary: str | None = None,
        temperature: float | None = None,
        Temperature: float | None = None,
        n_gpu_layers: int | None = None,
        n_ctx: int | None = None,
        max_tokens: int | None = None,
        n_threads: int | None = None,
        job: str | None = None,
        verbose: bool = False,
    ) -> None:
        """Shared implementation for ``tf`` (file) and ``td`` (directory)."""
        # Handle case-based overrides and fallbacks
        actual_overwrite = Overwrite or (write_over is True)
        actual_voc = Vocabulary if Vocabulary is not None else voc
        actual_temperature = Temperature if Temperature is not None else temperature

        _configure_logging(verbose)

        if job:
            self._run_file_job(path, job, output=output, dry_run=dry_run, verbose=verbose)
            return

        opts = _build_options_from_cli(
            to_lang=to_lang,
            path=path,
            engine=engine,
            from_lang=from_lang,
            recurse=recurse,
            write_over=actual_overwrite,
            output=output,
            save_voc=save_voc,
            chunk_size=chunk_size,
            html_chunk_size=html_chunk_size,
            include=include,
            xclude=xclude,
            dry_run=dry_run,
            prolog=prolog,
            voc=actual_voc,
            temperature=actual_temperature,
            n_gpu_layers=n_gpu_layers,
            n_ctx=n_ctx,
            max_tokens=max_tokens,
            n_threads=n_threads,
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

    def _run_file_job(
        self,
        path: str | Path,
        job_ref: str,
        *,
        output: str | Path | None,
        dry_run: bool,
        verbose: bool,
    ) -> None:
        """Run every entry of a job against ``path``, one suffixed output each."""
        from .job import load_job

        loaded = load_job(job_ref)
        base_output = Path(output).resolve() if output is not None else None
        for entry in loaded.resolved_entries():
            suffix = entry.resolved_suffix()
            out_dir = (base_output or Path(path).resolve().parent) / suffix
            opts = TranslatorOptions(
                engine=entry.selector,
                from_lang=entry.from_lang,
                to_lang=entry.to_lang,
                chunk_size=entry.chunk_size,
                html_chunk_size=entry.html_chunk_size,
                output_dir=out_dir,
                dry_run=dry_run,
                temperature=entry.params.get("temperature"),
                max_tokens=entry.params.get("max_tokens"),
                n_gpu_layers=entry.params.get("n_gpu_layers"),
                n_ctx=entry.params.get("n_ctx"),
                n_threads=entry.params.get("n_threads"),
            )
            try:
                results = translate_path(path, opts)
            except PipelineError as error:
                console.print(f"[red]{entry.selector}: {error}[/red]")
                continue
            for result in results:
                print(f"{entry.selector}\t{result.destination}")

    def tf(self, to_lang: str, path: str | Path, **kwargs: object) -> None:
        """Translate a single file.

        Args:
            to_lang: Target language code (e.g. 'pl').
            path: Path to the file to translate.
            **kwargs: engine, from_lang, output, chunk_size, --job, etc.
                See ``tr``/``td`` for the full option list.
        """
        self._translate_files(to_lang, path, **kwargs)  # type: ignore[arg-type]

    def td(self, to_lang: str, path: str | Path, **kwargs: object) -> None:
        """Translate a directory tree of files.

        Args:
            to_lang: Target language code (e.g. 'pl').
            path: Path to the directory to translate.
            **kwargs: engine, from_lang, output, recurse, include, xclude, --job, etc.
        """
        self._translate_files(to_lang, path, **kwargs)  # type: ignore[arg-type]

    def tr(
        self,
        to_lang: str,
        text: str,
        *,
        engine: str | None = None,
        from_lang: str | None = None,
        chunk_size: int | None = None,
        temperature: float | None = None,
        job: str | None = None,
        verbose: bool = False,
    ) -> None:
        """Translate a string and print the result to stdout.

        Args:
            to_lang: Target language code (e.g. 'pl').
            text: The text to translate.
            engine: Engine selector (e.g. 'tr::google', 'll::openai:gpt-4o-mini').
            from_lang: Source language code (defaults to 'auto').
            chunk_size: Override chunk size for the text.
            temperature: Inference temperature for LLM-based engines.
            job: JSON job (file path or inline) — translates the text with every
                entry and prints ``selector<TAB>translation`` lines.
            verbose: Enable debug log output.
        """
        _configure_logging(verbose)

        if job:
            from .job import load_job

            loaded = load_job(job)
            for entry in loaded.resolved_entries():
                opts = TranslatorOptions(
                    engine=entry.selector,
                    from_lang=entry.from_lang or from_lang,
                    to_lang=entry.to_lang or to_lang,
                    chunk_size=entry.chunk_size,
                    temperature=entry.params.get("temperature"),
                )
                try:
                    out = translate_string(text, opts)
                except PipelineError as error:
                    console.print(f"[red]{entry.selector}: {error}[/red]")
                    continue
                print(f"{entry.selector}\t{out}")
            return

        opts = TranslatorOptions(
            engine=normalize_selector(engine) if engine else engine,
            from_lang=from_lang,
            to_lang=to_lang,
            chunk_size=chunk_size,
            temperature=temperature,
        )
        try:
            output = translate_string(text, opts)
        except PipelineError as error:
            console.print(f"[red]{error}[/red]")
            raise
        print(output)

    def config(self) -> ConfigCommands:
        """Access configuration helper subcommands.

        Returns:
            ConfigCommands: Group of subcommands under `abersetz config` (show, path).
        """
        return ConfigCommands()

    def lang(self) -> list[str]:
        """List popular and all supported CLDR language codes.

        Prints popular language codes along with a list of all CLDR languages, and returns them as a list of strings.

        Returns:
            list[str]: The list of formatted language codes and names.
        """
        from langcodes import get

        popular: list[str] = []
        for code in POPULAR_LANG_CODES:
            try:
                name = get(code).language_name("en")
            except Exception:  # pragma: no cover - unexpected lookup failure
                name = code
            popular.append(f"{code} ({name})")
        header = "Popular targets: " + ", ".join(popular)

        rows = [header]
        rows.extend(_iter_language_rows())
        for line in rows:
            console.print(line)
        return rows

    def engines(
        self,
        include_paid: bool = False,
        *,
        family: str | None = None,
        configured_only: bool = False,
    ) -> None:
        """List available engines and whether they are configured.

        Prints a formatted table showing every engine we know about, whether you have it set up, and if it requires a paid API key."""
        entries = _collect_engine_entries(
            include_paid,
            family=family,
            configured_only=configured_only,
        )
        _render_engine_entries(entries)

    def ls(
        self,
        selector: str | None = None,
        *,
        include_paid: bool = False,
        force: bool = False,
        job: bool = False,
        to_lang: str = "en",
        from_lang: str = "auto",
    ) -> None:
        """List available engines, providers and models.

        Combines the old ``engines`` and ``discover`` commands. Without a
        ``selector`` it lists engines and provider names (fast). A selector
        prefix narrows the listing and — for model-bearing engines like ``ll::``,
        ``lm``, ``ml``, ``gg`` — enumerates models (slow; cached).

        Args:
            selector: Optional selector prefix or wildcard (e.g. 'tr', 'll::', 'tr::goog*').
            include_paid: Include providers that require a paid API key.
            force: Bypass the discovery cache and re-query model lists.
            job: Emit an abersetz job-JSON skeleton for the matched combos instead of a table.
            to_lang: Target language used when emitting a job (--job).
            from_lang: Source language used when emitting a job (--job).
        """
        from .job import job_to_dict
        from .listing import build_catalog, catalog_to_job

        entries = build_catalog(selector, include_paid=include_paid, force=force)
        if job:
            built = catalog_to_job(entries, to_lang=to_lang, from_lang=from_lang)
            print(json.dumps(job_to_dict(built), indent=2, ensure_ascii=False))
            return
        self._render_catalog(entries)

    def _render_catalog(self, entries: list) -> None:
        if not entries:
            console.print("No matching engines, providers, or models found.")
            return
        table = Table(title="abersetz catalog", show_header=True, header_style="bold cyan")
        table.add_column("Selector", style="white")
        table.add_column("Kind", style="cyan")
        table.add_column("Available", style="green")
        table.add_column("Key", style="yellow")
        table.add_column("Notes", style="magenta")
        for entry in entries:
            table.add_row(
                entry.selector,
                entry.kind,
                "✓" if entry.available else "✗",
                "required" if entry.requires_key else "free",
                entry.notes,
            )
        console.print(table)

    def setup(
        self,
        non_interactive: bool = False,
        verbose: bool = False,
        include_community: bool = False,
    ) -> None:
        """Run the configuration setup wizard.

        Args:
            non_interactive: Run without user interaction (for CI/automation)
            verbose: Enable verbose output with detailed logging
            include_community: Include community/self-hosted providers in defaults
        """
        setup_command(
            non_interactive=non_interactive,
            verbose=verbose,
            include_community=include_community,
        )

    def validate(
        self,
        *,
        selectors: str | Sequence[str] | None = None,
        Selectors: str | Sequence[str] | None = None,
        target_lang: str = "es",
        source_lang: str = "auto",
        sample_text: str | None = None,
        Text: str = "Hello, world!",
        include_defaults: bool = True,
    ) -> list[ValidationResult]:
        """Validate configured engines by translating a short phrase.

        Fires a test string ("Hello, world!") through the selected engines to measure latency and verify they actually work.

        Args:
            selectors: Backward compatible lowercase selectors option.
            Selectors: Comma-separated list or sequence of engine selectors to test. Maps to uppercase -S (avoids clash with source_lang -s).
            target_lang: Target language code to translate into. Maps to lowercase -t.
            source_lang: Source language code to translate from. Maps to lowercase -s.
            sample_text: Backward compatible lowercase sample text option.
            Text: Text phrase to translate for testing. Maps to uppercase -T (avoids clash with target_lang -t).
            include_defaults: Include default active engines in verification.
        """
        cfg = load_config()

        # Handle case-based overrides and fallbacks
        actual_selectors = Selectors if Selectors is not None else selectors
        actual_text = Text if Text != "Hello, world!" else (sample_text or Text)

        selector_tuple = _parse_patterns(actual_selectors)
        results = validate_engines(
            cfg,
            selectors=selector_tuple or None,
            target_lang=target_lang,
            source_lang=source_lang,
            sample_text=actual_text,
            include_defaults=include_defaults,
        )
        _render_validation_entries(results)
        return results

    def discover(
        self,
        *,
        format: str | None = None,
        min_size_mb: float = 100.0,
    ) -> None:
        """Scan and discover downloaded local LLM and AI models.

        Checks standard paths for HuggingFace, Ollama, LM Studio, Pinokio, and GPT4All.

        Args:
            format: Filter by model format extension (e.g. 'gguf', 'safetensors', 'coreml').
            min_size_mb: Minimum file size in MB to filter out metadata/configs (default: 100).
        """
        from .providers.llm.local_discovery import LocalModelFinder

        finder = LocalModelFinder()
        finder.scan(format=format, min_size_mb=min_size_mb)


def main() -> None:
    """Invoke the Fire CLI.

    Turns the `AbersetzCLI` class into a command-line application."""
    fire.Fire(AbersetzCLI(), name="abersetz")


def abtr_main() -> None:
    """Direct translation CLI.

    A shortcut command. `abtr es file.txt` is exactly the same as `abersetz tr es file.txt`."""

    # Create CLI instance and call tr method directly
    cli = AbersetzCLI()

    # Use Fire to parse arguments for the tr method specifically
    fire.Fire(cli.tr, name="abtr")


__all__ = ["AbersetzCLI", "ConfigCommands", "main", "abtr_main"]
