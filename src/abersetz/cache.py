# this_file: src/abersetz/cache.py
"""Persistent translation and TM-example results in diskcache_rs.

ABERSETZ_CACHE_DIR selects the location; ABERSETZ_CACHE=0 bypasses both caches.
Only completed results are stored, as JSON bytes under versioned hashed keys.
"""

from __future__ import annotations

import hashlib
import json
import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

from diskcache_rs import Cache
from loguru import logger
from platformdirs import user_cache_path

CACHE_FORMAT = "abersetz-results-v1"


def local_model_identity(model_path: str | None) -> list | None:
    """Invalidate translations when resolved local weights/configuration change."""
    if model_path is None:
        return None
    path = Path(model_path).resolve()
    files = sorted(p for p in path.iterdir() if p.is_file()) if path.is_dir() else [path]
    identity = []
    for file in files:
        stat = file.stat()
        identity.append([str(file), stat.st_ino, stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns])
    return identity


def cached_result(namespace: str, identity: dict, compute: Callable[[], Any]) -> Any:
    """Reuse a request result; cache I/O failure must never retry provider work."""
    if os.environ.get("ABERSETZ_CACHE", "1") == "0":
        return compute()
    directory = (
        Path(os.environ.get("ABERSETZ_CACHE_DIR") or user_cache_path("abersetz")) / CACHE_FORMAT
    )
    key = hashlib.sha256(
        json.dumps([namespace, identity], sort_keys=True, ensure_ascii=False).encode()
    ).hexdigest()
    try:
        with Cache(str(directory)) as cache:
            value = cache.get(key)
            if value is not None:
                return json.loads(value)
    except Exception as error:  # Rust bindings raise plain Exception for storage errors.
        logger.warning("Cache read unavailable: {}", error)
    result = compute()
    try:
        with Cache(str(directory)) as cache:
            if not cache.set(key, json.dumps(result, ensure_ascii=False).encode()):
                logger.warning("Cache write failed; returning the completed result")
    except Exception as error:  # Only cache I/O is inside this boundary, never compute().
        logger.warning("Cache write unavailable: {}", error)
    return result
