# this_file: src/abersetz/providers/base.py

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from ..chunking import TextFormat


class EngineError(RuntimeError):
    """Raised when an engine cannot be constructed or invoked."""


@dataclass(slots=True)
class EngineRequest:
    """Payload passed to engines."""

    text: str
    source_lang: str
    target_lang: str
    is_html: bool
    voc: dict[str, str]
    prolog: dict[str, str]
    chunk_index: int
    total_chunks: int
    examples: list[dict[str, str]] = field(default_factory=list)


@dataclass(slots=True)
class EngineResult:
    """Normalized engine output."""

    text: str
    voc: dict[str, str]


class Engine(Protocol):
    """Protocol implemented by engine adapters."""

    name: str
    chunk_size: int | None
    html_chunk_size: int | None

    def translate(self, request: EngineRequest) -> EngineResult:
        """Translate a chunk."""

    def chunk_size_for(self, fmt: TextFormat) -> int | None:
        """Return preferred chunk size for the given text format."""


class EngineBase:
    """Shared helpers for engines."""

    def __init__(
        self,
        name: str,
        chunk_size: int | None,
        html_chunk_size: int | None,
    ) -> None:
        self.name = name
        self.chunk_size = chunk_size
        self.html_chunk_size = html_chunk_size

    @property
    def supports_translation_examples(self) -> bool:
        """Whether the engine's prompt has a slot for translation-memory examples."""
        return False

    def chunk_size_for(self, fmt: TextFormat) -> int | None:
        if fmt is TextFormat.HTML and self.html_chunk_size:
            return self.html_chunk_size
        return self.chunk_size
