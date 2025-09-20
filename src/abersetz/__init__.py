"""Public package surface for abersetz."""
# this_file: src/abersetz/__init__.py

from __future__ import annotations

from importlib import metadata as _metadata

from .pipeline import PipelineError, TranslationResult, TranslatorOptions, translate_path

try:
    __version__ = _metadata.version("abersetz")
except _metadata.PackageNotFoundError:  # pragma: no cover - fallback for local dev
    from .__about__ import __version__  # type: ignore

__all__ = [
    "PipelineError",
    "TranslationResult",
    "TranslatorOptions",
    "__version__",
    "translate_path",
]
