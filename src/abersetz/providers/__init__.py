# this_file: src/abersetz/providers/__init__.py

from __future__ import annotations

from .base import Engine, EngineBase, EngineError, EngineRequest, EngineResult
from .deep_translator import DeepTranslatorEngine
from .gguf import LocalGgufEngine
from .hysf import HysfEngine
from .llm import LlmEngine
from .mlx import LocalMlxEngine
from .translators import TranslatorsEngine

__all__ = [
    "Engine",
    "EngineBase",
    "EngineError",
    "EngineRequest",
    "EngineResult",
    "DeepTranslatorEngine",
    "LocalGgufEngine",
    "HysfEngine",
    "LlmEngine",
    "LocalMlxEngine",
    "TranslatorsEngine",
]
