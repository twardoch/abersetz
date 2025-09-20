"""Tests for chunking and detection utilities."""
# this_file: tests/test_chunking.py

from __future__ import annotations

from abersetz.chunking import TextFormat, chunk_text, detect_format


def test_detect_format_identifies_html() -> None:
    snippet = "<html><body><p>Hello</p></body></html>"
    assert detect_format(snippet) is TextFormat.HTML


def test_chunk_text_preserves_round_trip() -> None:
    text = "\n".join(f"line {i}" for i in range(50))
    chunks = chunk_text(text, max_size=40, fmt=TextFormat.PLAIN)
    assert "".join(chunks) == text
    assert len(chunks) > 3


def test_html_chunking_returns_single_chunk() -> None:
    html = "<p>alpha</p><p>beta</p>"
    chunks = chunk_text(html, max_size=10, fmt=TextFormat.HTML)
    assert chunks == [html]
