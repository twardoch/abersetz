"""High level translation pipeline.

The brain of the operation. This takes a file or directory, figures out what text format it is, chops it up into digestible chunks, sends it to the translation engine, and stitches it all back together into a finished file."""
# this_file: src/abersetz/pipeline.py

from __future__ import annotations

import json
import threading
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .chunking import TextFormat, chunk_text, detect_format
from .config import AbersetzConfig, load_config
from .engine_catalog import normalize_selector
from .engines import Engine, EngineRequest, EngineResult, create_engine

try:
    from twat_cache.decorators import bcache
except ImportError:
    # Fallback decorator if twat_cache is not present
    def bcache(*args, **kwargs):
        def decorator(func):
            return func

        return decorator


DEFAULT_PATTERNS = ("*.txt", "*.md", "*.mdx", "*.html", "*.htm")


@dataclass(slots=True)
class TranslatorOptions:
    """Runtime options controlling translation behaviour.

    All the settings passed down from the CLI or library call: what engine to use, where to save things, what to include/exclude, etc."""

    engine: str | None = None
    from_lang: str | None = None
    to_lang: str | None = None
    recurse: bool = True
    write_over: bool = False
    output_dir: Path | None = None
    save_voc: bool = False
    chunk_size: int | None = None
    html_chunk_size: int | None = None
    include: tuple[str, ...] = DEFAULT_PATTERNS
    xclude: tuple[str, ...] = tuple()
    dry_run: bool = False
    prolog: dict[str, str] = field(default_factory=dict)
    initial_voc: dict[str, str] = field(default_factory=dict)
    temperature: float | None = None
    n_gpu_layers: int | None = None
    n_ctx: int | None = None
    max_tokens: int | None = None
    n_threads: int | None = None


@dataclass(slots=True)
class TranslationResult:
    """Information about a translated artefact.

    Returned when a file is finished. Tells you where the output was saved, what engine was used, how many chunks it took, and what vocabulary was accumulated."""

    source: Path
    destination: Path
    chunks: int
    voc: dict[str, str]
    format: TextFormat
    engine: str = ""
    source_lang: str = ""
    target_lang: str = ""
    chunk_size: int = 0


class PipelineError(RuntimeError):
    """Raised when translation cannot proceed.

    Catch this if you pass a bad path, lack read permissions, or something breaks catastrophically in the middle of translation."""


def translate_path(
    path: Path | str,
    options: TranslatorOptions | None = None,
    *,
    config: AbersetzConfig | None = None,
    client: object | None = None,
) -> list[TranslationResult]:
    """Translate a file or directory tree.

    The main entry point. Resolves paths, merges user options with defaults, finds all matching files, spins up the right engine, and feeds everything through the pipeline."""
    resolved = Path(path).resolve()

    # Validate input path exists and is accessible
    if not resolved.exists():
        raise PipelineError(f"Path does not exist: {resolved}")

    # Check readability
    try:
        if resolved.is_file():
            # Try to open the file to check read permissions
            resolved.open("r").close()
        elif resolved.is_dir():
            # Try to list directory to check read permissions
            list(resolved.iterdir())
    except (PermissionError, OSError) as e:
        raise PipelineError(f"Cannot read {resolved}: {e}") from e

    cfg = config or load_config()
    opts = _merge_defaults(options, cfg)
    targets = list(_discover_files(resolved, opts))
    if not targets:
        raise PipelineError(f"No files matched under {resolved}")
    engine_selector = normalize_selector(opts.engine or cfg.defaults.engine) or cfg.defaults.engine
    import inspect

    sig = inspect.signature(create_engine)
    kwargs: dict[str, Any] = {}
    if "temperature" in sig.parameters and opts.temperature is not None:
        kwargs["temperature"] = opts.temperature
    if "n_gpu_layers" in sig.parameters and getattr(opts, "n_gpu_layers", None) is not None:
        kwargs["n_gpu_layers"] = opts.n_gpu_layers
    if "n_ctx" in sig.parameters and getattr(opts, "n_ctx", None) is not None:
        kwargs["n_ctx"] = opts.n_ctx
    if "max_tokens" in sig.parameters and getattr(opts, "max_tokens", None) is not None:
        kwargs["max_tokens"] = opts.max_tokens
    if "n_threads" in sig.parameters and getattr(opts, "n_threads", None) is not None:
        kwargs["n_threads"] = opts.n_threads

    engine = create_engine(engine_selector, cfg, client=client, **kwargs)
    results: list[TranslationResult] = []

    # Simple translation without progress bar
    for file_path in targets:
        result = _translate_file(file_path, engine, opts, cfg)
        results.append(result)

    return results


def _merge_defaults(options: TranslatorOptions | None, config: AbersetzConfig) -> TranslatorOptions:
    opts = options or TranslatorOptions()
    if opts.engine is None:
        opts.engine = config.defaults.engine
    else:
        normalized_engine = normalize_selector(opts.engine)
        if normalized_engine:
            opts.engine = normalized_engine
    if opts.from_lang is None:
        opts.from_lang = config.defaults.from_lang
    if opts.to_lang is None:
        opts.to_lang = config.defaults.to_lang
    if opts.chunk_size is None:
        opts.chunk_size = config.defaults.chunk_size
    if opts.html_chunk_size is None:
        opts.html_chunk_size = config.defaults.html_chunk_size
    return opts


def _discover_files(root: Path, opts: TranslatorOptions) -> Iterable[Path]:
    if root.is_file():
        return [root]
    pattern_iter = root.rglob if opts.recurse else root.glob
    matched: list[Path] = []
    for pattern in opts.include:
        matched.extend(pattern_iter(pattern))
    filtered = [path for path in matched if not _is_xcluded(path, opts.xclude)]
    return sorted({path.resolve() for path in filtered if path.is_file()})


def _is_xcluded(path: Path, patterns: tuple[str, ...]) -> bool:
    return any(path.match(pattern) for pattern in patterns)


def _translate_file(
    source: Path,
    engine: Engine,
    opts: TranslatorOptions,
    config: AbersetzConfig,
) -> TranslationResult:
    text = source.read_text(encoding="utf-8")

    engine_selector = opts.engine or config.defaults.engine
    engine_selector = normalize_selector(engine_selector) or engine_selector
    source_lang = opts.from_lang or config.defaults.from_lang
    target_lang = opts.to_lang or config.defaults.to_lang

    # Handle edge cases
    if not text.strip():
        # Empty file - just create an empty output
        destination = _persist_output(
            source,
            "",
            {},
            TextFormat.PLAIN,
            opts,
            opts.to_lang or config.defaults.to_lang,
        )
        return TranslationResult(
            source=source,
            destination=destination,
            chunks=0,
            voc={},
            format=TextFormat.PLAIN,
            engine=engine_selector,
            source_lang=source_lang,
            target_lang=target_lang,
            chunk_size=0,
        )

    # Warn about very large files (>10MB)
    file_size = source.stat().st_size
    if file_size > 10 * 1024 * 1024:  # 10MB
        from loguru import logger

        logger.warning(f"Large file detected ({file_size / 1024 / 1024:.1f}MB): {source}")

    fmt = detect_format(text)
    if fmt is TextFormat.HTML:
        merged_text, total_chunks, voc = _translate_html(text, engine, opts, config)
        chunk_size = _select_chunk_size(fmt, engine, opts, config)
    else:
        chunk_size = _select_chunk_size(fmt, engine, opts, config)
        chunks = chunk_text(text, chunk_size, fmt)
        # logger.debug("%s: %s chunk(s) of size %s", source, len(chunks) or 1, chunk_size)
        results, voc = _apply_engine(engine, chunks, fmt, opts, config)
        merged_text = "".join(item.text for item in results)
        total_chunks = len(chunks) or 1

    destination = _persist_output(
        source,
        merged_text,
        voc,
        fmt,
        opts,
        opts.to_lang or config.defaults.to_lang,
    )
    return TranslationResult(
        source=source,
        destination=destination,
        chunks=total_chunks,
        voc=voc,
        format=fmt,
        engine=engine_selector,
        source_lang=source_lang,
        target_lang=target_lang,
        chunk_size=chunk_size,
    )


def _translate_html(
    text: str,
    engine: Engine,
    opts: TranslatorOptions,
    config: AbersetzConfig,
) -> tuple[str, int, dict[str, str]]:
    """Translate HTML using htmladapt for structured preservation."""
    import copy

    from bs4 import BeautifulSoup
    from htmladapt import HTMLExtractMergeTool

    tool = HTMLExtractMergeTool()
    map_html, comp_html = tool.extract(text)

    soup = BeautifulSoup(comp_html, "html.parser")
    body = soup.body
    elements = list(body.children) if body else []
    elements = [el for el in elements if getattr(el, "name", None) is not None]

    if not elements:
        return text, 1, {}

    chunk_size = _select_chunk_size(TextFormat.HTML, engine, opts, config)
    chunks: list[list[Any]] = []
    current_chunk: list[Any] = []
    current_size = 0

    for el in elements:
        el_str = str(el)
        el_size = len(el_str)
        if current_chunk and current_size + el_size > chunk_size:
            chunks.append(current_chunk)
            current_chunk = [el]
            current_size = el_size
        else:
            current_chunk.append(el)
            current_size += el_size
    if current_chunk:
        chunks.append(current_chunk)

    chunk_htmls = []
    for chunk_els in chunks:
        chunk_soup = BeautifulSoup("<html><body></body></html>", "html.parser")
        for el in chunk_els:
            chunk_soup.body.append(copy.copy(el))
        chunk_htmls.append(str(chunk_soup))

    results, voc = _apply_engine(engine, chunk_htmls, TextFormat.HTML, opts, config)

    translated_elements = []
    for r in results:
        r_soup = BeautifulSoup(r.text, "html.parser")
        r_body = r_soup.body
        source_root = r_body if r_body else r_soup
        found_elements = [
            el for el in source_root.children if getattr(el, "name", None) is not None
        ]
        if not found_elements and source_root is r_body:
            found_elements = [el for el in r_soup.children if getattr(el, "name", None) is not None]
        translated_elements.extend(found_elements)

    final_comp_soup = BeautifulSoup("<html><body></body></html>", "html.parser")
    for el in translated_elements:
        final_comp_soup.body.append(copy.copy(el))
    final_comp_html = str(final_comp_soup)

    final_html = tool.merge(final_comp_html, comp_html, map_html, text)
    return final_html, len(chunks), voc


_active_engine = threading.local()


@bcache(folder_name="abersetz_chunk_translations")
def _cached_translate_call(
    engine_name: str,
    model_name: str | None,
    text: str,
    source_lang: str,
    target_lang: str,
    is_html: bool,
    voc_json: str,
    prolog_json: str,
    temperature: float | None,
) -> tuple[str, str]:
    print(
        f"\n[CACHE MISS] engine={engine_name} text={text!r} src={source_lang} tgt={target_lang} voc={voc_json} prolog={prolog_json}"
    )
    engine = getattr(_active_engine, "current", None)
    if not engine:
        raise RuntimeError("No active engine configured in thread-local storage")

    request = EngineRequest(
        text=text,
        source_lang=source_lang,
        target_lang=target_lang,
        is_html=is_html,
        voc=json.loads(voc_json),
        prolog=json.loads(prolog_json),
        chunk_index=0,
        total_chunks=1,
    )
    result = engine.translate(request)
    return result.text, json.dumps(result.voc, ensure_ascii=False)


def _apply_engine(
    engine: Engine,
    chunks: Iterable[str],
    fmt: TextFormat,
    opts: TranslatorOptions,
    config: AbersetzConfig,
) -> tuple[list[EngineResult], dict[str, str]]:
    voc = dict(opts.initial_voc)
    prolog = dict(opts.prolog)
    results: list[EngineResult] = []
    chunk_list = list(chunks)
    len(chunk_list) or 1

    _active_engine.current = engine
    try:
        for _index, chunk in enumerate(chunk_list):
            voc_json = json.dumps(voc, sort_keys=True, ensure_ascii=False)
            prolog_json = json.dumps(prolog, sort_keys=True, ensure_ascii=False)

            model_val = getattr(engine, "_model_name", None) or getattr(engine, "_model", None)
            if model_val is not None:
                if isinstance(model_val, str):
                    model_name = model_val
                else:
                    model_name = getattr(model_val, "name", None) or model_val.__class__.__name__
            else:
                model_name = None
            temperature = getattr(engine, "_temperature", None)

            res_text, res_voc_json = _cached_translate_call(
                engine_name=engine.name,
                model_name=model_name,
                text=chunk,
                source_lang=opts.from_lang or "auto",
                target_lang=opts.to_lang or config.defaults.to_lang,
                is_html=(fmt is TextFormat.HTML),
                voc_json=voc_json,
                prolog_json=prolog_json,
                temperature=temperature,
            )

            new_voc = json.loads(res_voc_json)
            voc = new_voc
            results.append(EngineResult(text=res_text, voc=new_voc))
    finally:
        if hasattr(_active_engine, "current"):
            del _active_engine.current

    return results, voc


def _build_request(
    chunk: str,
    index: int,
    total: int,
    fmt: TextFormat,
    opts: TranslatorOptions,
    config: AbersetzConfig,
    voc: dict[str, str],
    prolog: dict[str, str],
) -> EngineRequest:
    return EngineRequest(
        text=chunk,
        source_lang=opts.from_lang or "auto",
        target_lang=opts.to_lang or config.defaults.to_lang,
        is_html=fmt is TextFormat.HTML,
        voc=voc,
        prolog=prolog,
        chunk_index=index,
        total_chunks=total,
    )


def _select_chunk_size(
    fmt: TextFormat,
    engine: Engine,
    opts: TranslatorOptions,
    config: AbersetzConfig,
) -> int:
    if fmt is TextFormat.HTML:
        html_size = (
            opts.html_chunk_size or engine.chunk_size_for(fmt) or config.defaults.html_chunk_size
        )
        return max(html_size, 1)
    plain_size = opts.chunk_size or engine.chunk_size_for(fmt) or config.defaults.chunk_size
    return max(plain_size, 1)


def _persist_output(
    source: Path,
    content: str,
    voc: dict[str, str],
    fmt: TextFormat,
    opts: TranslatorOptions,
    target_lang: str,
) -> Path:
    if opts.write_over:
        destination = source
    else:
        base = opts.output_dir or source.parent / target_lang
        base.mkdir(parents=True, exist_ok=True)
        destination = base / source.name
    if not opts.dry_run:
        destination.write_text(content, encoding="utf-8")
        if opts.save_voc:
            vocab_path = destination.with_suffix(destination.suffix + ".voc.json")
            vocab_path.write_text(json.dumps(voc, indent=2, ensure_ascii=False), encoding="utf-8")
    return destination


__all__ = [
    "PipelineError",
    "TranslationResult",
    "TranslatorOptions",
    "translate_path",
]
