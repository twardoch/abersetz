"""Test configuration for abersetz."""
# this_file: tests/conftest.py

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
if SRC.exists():
    sys.path.insert(0, str(SRC))

# Isolate twat-cache by using a clean in-memory mock during test runs.
# twat_cache is optional and its installed build may be broken; degrade gracefully.
try:
    import twat_cache.decorators  # noqa: E402

    _HAS_TWAT_CACHE = True
except Exception:  # pragma: no cover - environment dependent
    twat_cache = None  # type: ignore[assignment]
    _HAS_TWAT_CACHE = False

test_caches: list[dict] = []


def mock_bcache(*args, **kwargs):
    def decorator(func):
        cache_dict = {}
        test_caches.append(cache_dict)

        from functools import wraps

        @wraps(func)
        def wrapper(*args_inner, **kwargs_inner):
            # Create a simple, serializable key for arguments
            # Note: dict or other unhashable inputs are converted to strings/tuples
            def make_hashable(val):
                if isinstance(val, dict):
                    return tuple(sorted((k, make_hashable(v)) for k, v in val.items()))
                elif isinstance(val, (list, tuple)):
                    return tuple(make_hashable(x) for x in val)
                elif isinstance(val, set):
                    return tuple(sorted(make_hashable(x) for x in val))
                return val

            key = (
                tuple(make_hashable(x) for x in args_inner),
                tuple(sorted((k, make_hashable(v)) for k, v in kwargs_inner.items())),
            )
            if key not in cache_dict:
                cache_dict[key] = func(*args_inner, **kwargs_inner)
            return cache_dict[key]

        wrapper.clear = cache_dict.clear
        return wrapper

    return decorator


if _HAS_TWAT_CACHE:
    twat_cache.decorators.bcache = mock_bcache


@pytest.fixture(autouse=True)
def _temp_config_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Isolate persisted config for each test run."""
    config_root = tmp_path / "config"
    monkeypatch.setenv("ABERSETZ_CONFIG_DIR", str(config_root))
    return config_root


@pytest.fixture(autouse=True)
def _clear_cache() -> None:
    """Clear all mock cache dictionaries to ensure complete test isolation."""
    for cache_dict in test_caches:
        cache_dict.clear()
