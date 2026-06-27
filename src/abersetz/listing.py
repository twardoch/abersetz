"""Engine / provider / model discovery for the ``abersetz ls`` command.

Produces a catalog of usable selectors. Listing engines and provider names is
fast (static tables); enumerating models is slow (queries provider APIs or scans
local disk) and therefore only happens when the requested selector narrows to a
model-bearing engine. Slow results are cached under the config directory and
reused unless ``force`` is set."""

# this_file: src/abersetz/listing.py

from __future__ import annotations

import fnmatch
import json
import time
from dataclasses import dataclass
from pathlib import Path

from loguru import logger

from .config import AbersetzConfig, config_dir, load_config
from .engine_catalog import (
    PAID_TRANSLATOR_PROVIDERS,
    collect_deep_translator_providers,
    collect_translator_providers,
)
from .job import Job, JobEntry
from .selector import parse_selector

#: Cache lifetime for slow discovery results (24 hours).
CACHE_TTL_SECONDS = 24 * 60 * 60

#: Engines whose providers are themselves models (no static provider list).
_MODEL_ENGINES = frozenset({"lm", "ml", "gg"})


@dataclass(slots=True)
class CatalogEntry:
    """One discovered selector with display metadata."""

    selector: str
    kind: str  # "engine" | "provider" | "model" | "endpoint"
    available: bool = True
    requires_key: bool = False
    notes: str = ""


def _cache_path(key: str) -> Path:
    return config_dir() / "ls_cache" / f"{key}.json"


def _read_cache(key: str, force: bool) -> list[str] | None:
    if force:
        return None
    path = _cache_path(key)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if time.time() - float(data["ts"]) > CACHE_TTL_SECONDS:
            return None
        return list(data["items"])
    except Exception:  # pragma: no cover - corrupt cache is non-fatal
        return None


def _write_cache(key: str, items: list[str]) -> None:
    path = _cache_path(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.write_text(json.dumps({"ts": time.time(), "items": items}), encoding="utf-8")
    except OSError as exc:  # pragma: no cover - best effort
        logger.debug(f"Could not write ls cache {path}: {exc}")


# --- Fast layer: engines and provider names -------------------------------


def _engine_entries() -> list[CatalogEntry]:
    return [
        CatalogEntry("tr::", "engine", notes="translators (web)"),
        CatalogEntry("dt::", "engine", notes="deep-translator"),
        CatalogEntry("lm::", "engine", notes="LMStudio SDK"),
        CatalogEntry("ll::", "engine", notes="OpenAI-compatible LLM API"),
        CatalogEntry("ml::", "engine", notes="local MLX model"),
        CatalogEntry("gg::", "engine", notes="local GGUF model"),
    ]


def _translator_provider_entries(include_paid: bool) -> list[CatalogEntry]:
    entries: list[CatalogEntry] = []
    for provider in collect_translator_providers(include_paid=include_paid):
        entries.append(
            CatalogEntry(
                f"tr::{provider}",
                "provider",
                requires_key=provider in PAID_TRANSLATOR_PROVIDERS,
            )
        )
    return entries


def _deep_provider_entries(include_paid: bool) -> list[CatalogEntry]:
    entries: list[CatalogEntry] = []
    for provider in collect_deep_translator_providers(include_paid=include_paid):
        entries.append(CatalogEntry(f"dt::{provider}", "provider"))
    return entries


def _endpoint_entries() -> list[CatalogEntry]:
    from .providers.llm.discovery import all_endpoints

    entries: list[CatalogEntry] = []
    for name, endpoint in sorted(all_endpoints().items()):
        import os

        has_key = bool(os.getenv(endpoint.api_key_env))
        entries.append(
            CatalogEntry(
                f"ll::{name}",
                "endpoint",
                available=has_key,
                requires_key=True,
                notes="key set" if has_key else f"set {endpoint.api_key_env}",
            )
        )
    return entries


# --- Slow layer: model enumeration ----------------------------------------


def _llm_model_entries(endpoint_name: str | None, force: bool) -> list[CatalogEntry]:
    from .providers.llm.discovery import all_endpoints, fetch_models

    endpoints = all_endpoints()
    targets = (
        {endpoint_name: endpoints[endpoint_name]}
        if endpoint_name and endpoint_name in endpoints
        else endpoints
    )
    entries: list[CatalogEntry] = []
    for name, endpoint in sorted(targets.items()):
        import os

        if not os.getenv(endpoint.api_key_env):
            continue
        cache_key = f"ll_{name}"
        models = _read_cache(cache_key, force)
        if models is None:
            models = fetch_models(endpoint)
            if models:
                _write_cache(cache_key, models)
        for model in models:
            entries.append(CatalogEntry(f"ll::{name}:{model}", "model", requires_key=True))
    return entries


def _local_model_entries(engine: str, force: bool) -> list[CatalogEntry]:
    """Scan local disk for models usable by ``lm``/``ml``/``gg``."""
    cache_key = f"local_{engine}"
    cached = _read_cache(cache_key, force)
    fmt = "gguf" if engine == "gg" else None
    if cached is not None:
        return [CatalogEntry(sel, "model") for sel in cached]

    from .providers.llm.local_discovery import LocalModelFinder

    finder = LocalModelFinder()
    models = finder.discover_models(format_filter=fmt)
    selectors: list[str] = []
    for model in models:
        if engine == "gg" and model.format != "GGUF":
            continue
        if engine == "ml" and model.format not in {"Safetensors", "MLX"}:
            continue
        if engine == "lm":
            selectors.append(f"lm::{model.name}")
        else:
            selectors.append(f"{engine}::{model.path}")
    _write_cache(cache_key, selectors)
    return [CatalogEntry(sel, "model") for sel in selectors]


# --- Catalog assembly ------------------------------------------------------


def build_catalog(
    prefix: str | None = None,
    *,
    config: AbersetzConfig | None = None,
    include_paid: bool = False,
    force: bool = False,
) -> list[CatalogEntry]:
    """Return catalog entries, optionally filtered by a selector ``prefix``.

    Without a prefix only the fast layer (engines, providers, endpoints) is
    returned. A prefix that targets a model-bearing engine (``ll::``, ``lm``,
    ``ml``, ``gg``) triggers the slow model enumeration for that engine only."""
    config = config or load_config()
    entries: list[CatalogEntry] = []

    target_engine: str | None = None
    wants_models = False
    endpoint_name: str | None = None
    if prefix:
        parsed = parse_selector(prefix)
        if parsed and parsed.engine:
            target_engine = parsed.engine
            wants_models = "::" in prefix or target_engine in _MODEL_ENGINES
            if target_engine == "ll" and parsed.provider:
                endpoint_name = parsed.provider.split(":", 1)[0] or None

    def include(engine_code: str) -> bool:
        return target_engine is None or target_engine == engine_code

    if target_engine is None:
        entries.extend(_engine_entries())

    if include("tr"):
        entries.extend(_translator_provider_entries(include_paid))
    if include("dt"):
        entries.extend(_deep_provider_entries(include_paid))
    if include("ll"):
        entries.extend(_endpoint_entries())
        if wants_models:
            entries.extend(_llm_model_entries(endpoint_name, force))
    if include("lm") and wants_models:
        entries.extend(_local_model_entries("lm", force))
    if include("ml") and wants_models:
        entries.extend(_local_model_entries("ml", force))
    if include("gg") and wants_models:
        entries.extend(_local_model_entries("gg", force))

    # Wildcard / prefix filtering against the generated selectors.
    if prefix:
        pattern = prefix if any(ch in prefix for ch in "*?") else f"{prefix}*"
        entries = [e for e in entries if fnmatch.fnmatch(e.selector, pattern)]

    return entries


def catalog_to_job(entries: list[CatalogEntry], *, to_lang: str, from_lang: str = "auto") -> Job:
    """Turn concrete (provider/model) catalog entries into a job skeleton."""
    job_entries = [
        JobEntry(selector=e.selector) for e in entries if e.kind in {"provider", "model"}
    ]
    return Job(from_lang=from_lang, to_lang=to_lang, entries=job_entries)


__all__ = ["CatalogEntry", "build_catalog", "catalog_to_job", "CACHE_TTL_SECONDS"]
