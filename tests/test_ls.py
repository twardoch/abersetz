"""Tests for the ls / discovery catalog."""
# this_file: tests/test_ls.py

from __future__ import annotations

import pytest

import abersetz.listing as listing
from abersetz.listing import build_catalog, catalog_to_job


def test_no_prefix_lists_engines_fast(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(listing, "collect_translator_providers", lambda **_: ["google", "bing"])
    monkeypatch.setattr(listing, "collect_deep_translator_providers", lambda **_: ["google"])
    monkeypatch.setattr(listing, "_endpoint_entries", lambda: [])
    # No model enumeration should occur without a prefix.
    monkeypatch.setattr(
        listing,
        "_local_model_entries",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("slow scan should not run")),
    )
    entries = build_catalog()
    selectors = {e.selector for e in entries}
    assert "tr::" in selectors
    assert "gg::" in selectors
    assert "tr::google" in selectors
    assert "dt::google" in selectors


def test_prefix_narrows_to_engine(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(listing, "collect_translator_providers", lambda **_: ["google", "bing"])
    monkeypatch.setattr(
        listing,
        "collect_deep_translator_providers",
        lambda **_: (_ for _ in ()).throw(AssertionError("dt should not be listed for tr prefix")),
    )
    entries = build_catalog("tr")
    selectors = {e.selector for e in entries}
    assert selectors == {"tr::google", "tr::bing"}


def test_wildcard_filter(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        listing, "collect_translator_providers", lambda **_: ["google", "bing", "googletrans"]
    )
    entries = build_catalog("tr::goog*")
    selectors = {e.selector for e in entries}
    assert selectors == {"tr::google", "tr::googletrans"}


def test_local_model_entries_cached(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setenv("ABERSETZ_CONFIG_DIR", str(tmp_path / "cfg"))

    calls = {"n": 0}

    class FakeModel:
        def __init__(self, name, path, fmt):
            self.name = name
            self.path = path
            self.format = fmt

    class FakeFinder:
        def discover_models(self, format_filter=None):
            calls["n"] += 1
            return [FakeModel("m.gguf", "/models/m.gguf", "GGUF")]

    import abersetz.providers.llm.local_discovery as ld

    monkeypatch.setattr(ld, "LocalModelFinder", FakeFinder)

    first = build_catalog("gg::", force=True)
    assert any(e.selector == "gg::/models/m.gguf" for e in first)
    assert calls["n"] == 1
    # Second call uses cache (no extra discovery).
    build_catalog("gg::", force=False)
    assert calls["n"] == 1


def test_catalog_to_job() -> None:
    entries = [
        listing.CatalogEntry("tr::", "engine"),
        listing.CatalogEntry("tr::google", "provider"),
        listing.CatalogEntry("ll::openai:gpt-4o", "model"),
    ]
    job = catalog_to_job(entries, to_lang="pl")
    assert job.to_lang == "pl"
    # Engine-level entries are excluded; only concrete combos remain.
    assert {e.selector for e in job.entries} == {"tr::google", "ll::openai:gpt-4o"}
