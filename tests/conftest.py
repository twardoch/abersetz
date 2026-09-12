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


@pytest.fixture(autouse=True, scope="session")
def _prefect_test_harness():
    """Run Prefect flows/tasks against an ephemeral, fresh temp database.

    Without this, executing a Prefect flow during tests starts a temporary
    server that runs Alembic migrations against the user's persistent
    ``~/.prefect/prefect.db``. A stale DB from a different Prefect version
    aborts startup ("Can't locate revision ..."), so the suite cannot run
    offline/deterministically. ``prefect_test_harness`` points Prefect at a
    throwaway temp DB with correct migrations and runs in-process.
    """
    try:
        from prefect.testing.utilities import prefect_test_harness
    except Exception:  # pragma: no cover - prefect optional
        yield
        return
    with prefect_test_harness():
        yield


@pytest.fixture(autouse=True)
def _temp_config_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Isolate persisted config for each test run."""
    config_root = tmp_path / "config"
    monkeypatch.setenv("ABERSETZ_CONFIG_DIR", str(config_root))
    monkeypatch.setenv("ABERSETZ_CACHE_DIR", str(tmp_path / "cache"))
    return config_root
