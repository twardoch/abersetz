"""Text detection and chunking utilities.

We need chunks because language models have limits, and web translators have temper tantrums if you send them too much at once. This splits text cleanly."""
# this_file: src/abersetz/chunking.py

from __future__ import annotations

import re
from collections.abc import Iterable
from enum import Enum

_HTML_PATTERN = re.compile(r"<\s*(html|body|head|div|span|p|br|!DOCTYPE)", re.IGNORECASE)


class TextFormat(Enum):
    """Minimal set of supported text formats.

We keep this dead simple: plain text or HTML. That tells the splitter how to slice."""

    PLAIN = "plain"
    HTML = "html"


def detect_format(text: str) -> TextFormat:
    """Detect whether `text` looks like HTML.

It searches for basic HTML tags. If it finds one, it assumes HTML. Otherwise, plain text."""
    if _HTML_PATTERN.search(text):
        return TextFormat.HTML
    return TextFormat.PLAIN


def _fallback_chunks(text: str, max_size: int) -> list[str]:
    """Simple slicing fallback when semantic splitter is unavailable.

Brute-force slices a string into chunks of `max_size`. Not pretty, but it works if the semantic splitter is missing."""
    return [text[i : i + max_size] for i in range(0, len(text), max_size)]


def _semantic_chunks(text: str, max_size: int) -> Iterable[str]:
    """Prefer semantic-text-splitter when installed.

Slices text at sensible boundaries (like sentences or paragraphs) rather than cutting words in half.
Falls back to brute-force slicing if the library isn't installed."""
    try:
        from semantic_text_splitter import TextSplitter
    except ImportError:  # pragma: no cover - exercised in environments without dependency
        yield from _fallback_chunks(text, max_size)
        return
    splitter = TextSplitter(max_size, trim=False)
    yield from splitter.chunks(text)


def chunk_text(text: str, max_size: int, fmt: TextFormat) -> list[str]:
    """Chunk text according to the detected format.

HTML currently gets passed whole (we don't split it yet). Plain text gets semantic splitting."""
    if not text:
        return []
    if fmt is TextFormat.HTML:
        return [text]
    return list(_semantic_chunks(text, max_size))


__all__ = ["TextFormat", "chunk_text", "detect_format"]
