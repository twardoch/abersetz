"""Legacy shim exporting the primary pipeline API.

Kept around so scripts relying on `from abersetz.abersetz import translate_path` don't suddenly break."""
# this_file: src/abersetz/abersetz.py

from __future__ import annotations

from .pipeline import PipelineError, TranslationResult, TranslatorOptions, translate_path

__all__ = [
    "PipelineError",
    "TranslationResult",
    "TranslatorOptions",
    "translate_path",
]
