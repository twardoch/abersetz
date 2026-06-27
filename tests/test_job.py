"""Tests for the abersetz job-JSON format."""
# this_file: tests/test_job.py

from __future__ import annotations

import json

import pytest

from abersetz.job import Job, JobEntry, job_to_dict, load_job


def test_job_entry_defaults_suffix_from_selector() -> None:
    entry = JobEntry(selector="tr::google")
    assert entry.resolved_suffix() == "tr-google"


def test_job_entry_explicit_suffix() -> None:
    entry = JobEntry(selector="tr::google", suffix="my-suffix")
    assert entry.resolved_suffix() == "my-suffix"


def test_job_entry_rejects_invalid_selector() -> None:
    with pytest.raises(ValueError):
        JobEntry(selector="   ")


def test_resolved_entries_fill_defaults() -> None:
    job = Job(
        to_lang="pl",
        from_lang="en",
        chunk_size=1000,
        entries=[JobEntry(selector="tr::google"), JobEntry(selector="dt::deepl", to_lang="de")],
    )
    resolved = job.resolved_entries()
    assert resolved[0].to_lang == "pl"
    assert resolved[0].from_lang == "en"
    assert resolved[0].chunk_size == 1000
    # Entry-level value wins over job default.
    assert resolved[1].to_lang == "de"


def test_load_job_from_inline_json() -> None:
    raw = json.dumps({"to_lang": "pl", "entries": [{"selector": "tr::google"}]})
    job = load_job(raw)
    assert job.to_lang == "pl"
    assert job.entries[0].selector == "tr::google"


def test_load_job_from_file(tmp_path) -> None:
    path = tmp_path / "job.json"
    path.write_text(json.dumps({"entries": [{"selector": "ll::siliconflow:m"}]}), encoding="utf-8")
    job = load_job(path)
    assert job.entries[0].selector == "ll::siliconflow:m"


def test_load_job_rejects_non_object() -> None:
    with pytest.raises(ValueError):
        load_job("[1, 2, 3]")


def test_job_to_dict_roundtrip() -> None:
    job = Job(to_lang="pl", entries=[JobEntry(selector="tr::google", params={"temperature": 0.3})])
    data = job_to_dict(job)
    assert data["to_lang"] == "pl"
    assert data["entries"][0]["selector"] == "tr::google"
    restored = load_job(json.dumps(data))
    assert restored.entries[0].params == {"temperature": 0.3}
