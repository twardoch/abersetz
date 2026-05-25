"""Public package surface for abersetz.

Abersetz is an AI-powered translation pipeline designed to be fast, reliable, and invisible.
It chunks text, hands it to language models, and stitches the translated pieces back together
without breaking formatting or structure.

We export only what you need to run translations or handle their failures:
- `translate_path`: The main workhorse for files and directories.
- `TranslatorOptions`: Knobs and dials for the translation pipeline.
- `TranslationResult`: The outcome, good or bad.
- `PipelineError`: When things break, this tells you why.
"""
# this_file: src/abersetz/__init__.py

from __future__ import annotations

from importlib import metadata as _metadata
from typing import TYPE_CHECKING, Any

# Only import types for static analysis
if TYPE_CHECKING:
    from .pipeline import PipelineError, TranslationResult, TranslatorOptions, translate_path
    from .tasks import translate_flow, translate_task

# Lazy loading implementation
_LAZY_IMPORTS: dict[str, Any] = {}


def __getattr__(name: str) -> Any:
    """Lazy load heavy modules only when accessed."""
    if name in _LAZY_IMPORTS:
        return _LAZY_IMPORTS[name]

    # Lazy load pipeline module components
    if name in ("PipelineError", "TranslationResult", "TranslatorOptions", "translate_path"):
        from . import pipeline

        _LAZY_IMPORTS["PipelineError"] = pipeline.PipelineError
        _LAZY_IMPORTS["TranslationResult"] = pipeline.TranslationResult
        _LAZY_IMPORTS["TranslatorOptions"] = pipeline.TranslatorOptions
        _LAZY_IMPORTS["translate_path"] = pipeline.translate_path
        return _LAZY_IMPORTS[name]

    # Lazy load tasks module components
    if name in ("translate_task", "translate_flow"):
        from . import tasks

        _LAZY_IMPORTS["translate_task"] = tasks.translate_task
        _LAZY_IMPORTS["translate_flow"] = tasks.translate_flow
        return _LAZY_IMPORTS[name]

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


# Version handling - lightweight
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
    "translate_task",
    "translate_flow",
]
