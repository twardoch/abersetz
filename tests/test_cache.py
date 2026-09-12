# this_file: tests/test_cache.py
"""Exercise the real Rust disk cache, including a second Python process."""

import os
import subprocess
import sys

import pytest

from abersetz.cache import cached_result, local_model_identity


def test_cache_when_local_weights_change_then_identity_changes(tmp_path):
    path = tmp_path / "model.gguf"
    path.write_bytes(b"first")
    before = local_model_identity(str(path))
    assert before == local_model_identity(str(path))
    path.write_bytes(b"other")
    assert before != local_model_identity(str(path)), "same-size replacement must invalidate cache"
    directory = local_model_identity(str(tmp_path))
    (tmp_path / "config.json").write_text("{}")
    assert directory != local_model_identity(str(tmp_path))
    assert local_model_identity(None) is None


def test_cache_when_reopened_in_another_process_then_reuses_result(tmp_path, monkeypatch):
    monkeypatch.setenv("ABERSETZ_CACHE_DIR", str(tmp_path / "cache"))
    assert cached_result("translation", {"text": "font"}, lambda: ["krój", "{}"]) == ["krój", "{}"]
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "from abersetz.cache import cached_result; "
            "print(cached_result('translation', {'text': 'font'}, lambda: ['MISS', '{}'])[0])",
        ],
        env=os.environ.copy(),
        check=True,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "krój", "cache must persist across processes"


def test_cache_when_context_changes_then_misses_and_failures_are_not_cached():
    calls = []

    def compute():
        calls.append(1)
        return ["translated", "{}"]

    for key in [{"examples": "a"}, {"examples": "a"}, {"examples": "b"}]:
        cached_result("translation", key, compute)
    assert len(calls) == 2

    def fail():
        raise RuntimeError("provider failed")

    with pytest.raises(RuntimeError, match="provider failed"):
        cached_result("translation", {"examples": "c"}, fail)
    cached_result("translation", {"examples": "c"}, compute)
    assert len(calls) == 3


def test_cache_when_disabled_or_unwritable_then_returns_translation(tmp_path, monkeypatch):
    calls = []

    def compute():
        calls.append(1)
        return ["translated", "{}"]

    monkeypatch.setenv("ABERSETZ_CACHE", "0")
    for _ in range(2):
        cached_result("translation", {}, compute)
    assert len(calls) == 2
    monkeypatch.delenv("ABERSETZ_CACHE")
    invalid = tmp_path / "file"
    invalid.write_text("not a directory")
    monkeypatch.setenv("ABERSETZ_CACHE_DIR", str(invalid))
    assert cached_result("translation", {}, compute) == ["translated", "{}"]
