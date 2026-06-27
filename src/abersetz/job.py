"""Abersetz job-JSON format.

A *job* is a reusable description of one or more translation configurations: each
entry pairs an engine selector with languages, chunk sizes, engine parameters and
an output-naming suffix. A single job can fan one input out across many engines
(handy for benchmarking) or pin one engine for a repeatable batch.

Example::

    {
      "to_lang": "pl",
      "from_lang": "en",
      "output_dir": "out",
      "entries": [
        {"selector": "tr::google"},
        {"selector": "ll::siliconflow:Qwen/Qwen2.5-7B", "params": {"temperature": 0.3}}
      ]
    }

Per-entry fields override the job-level defaults; ``suffix`` defaults to a slug
derived from the selector."""

# this_file: src/abersetz/job.py

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .selector import parse_selector, slugify_selector


class JobEntry(BaseModel):
    """One engine configuration within a job."""

    model_config = ConfigDict(extra="forbid")

    selector: str
    from_lang: str | None = None
    to_lang: str | None = None
    chunk_size: int | None = None
    html_chunk_size: int | None = None
    suffix: str | None = None
    params: dict[str, Any] = Field(default_factory=dict)

    @field_validator("selector")
    @classmethod
    def _validate_selector(cls, value: str) -> str:
        parsed = parse_selector(value)
        if parsed is None or not parsed.engine:
            raise ValueError(f"Invalid selector: {value!r}")
        return value

    def resolved_suffix(self) -> str:
        """Return the explicit suffix or one slugified from the selector."""
        return self.suffix or slugify_selector(self.selector)


class Job(BaseModel):
    """A collection of translation entries plus shared defaults."""

    model_config = ConfigDict(extra="forbid")

    input: str | None = None
    output_dir: str | None = None
    from_lang: str | None = None
    to_lang: str | None = None
    chunk_size: int | None = None
    html_chunk_size: int | None = None
    entries: list[JobEntry] = Field(default_factory=list)

    def resolved_entries(self) -> list[JobEntry]:
        """Return entries with job-level defaults filled in where unset."""
        resolved: list[JobEntry] = []
        for entry in self.entries:
            resolved.append(
                entry.model_copy(
                    update={
                        "from_lang": entry.from_lang or self.from_lang,
                        "to_lang": entry.to_lang or self.to_lang,
                        "chunk_size": entry.chunk_size or self.chunk_size,
                        "html_chunk_size": entry.html_chunk_size or self.html_chunk_size,
                    }
                )
            )
        return resolved


def load_job(reference: str | Path) -> Job:
    """Load a job from a JSON file path or an inline JSON string."""
    text: str
    path = Path(reference)
    text = path.read_text(encoding="utf-8") if path.exists() else str(reference)
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Job is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("Job JSON must be an object")
    return Job.model_validate(data)


def job_to_dict(job: Job) -> dict[str, Any]:
    """Serialise a job to a plain dict (drops unset/None fields)."""
    return job.model_dump(exclude_none=True)


__all__ = ["Job", "JobEntry", "load_job", "job_to_dict"]
