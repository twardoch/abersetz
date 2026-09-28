# this_file: src/abersetz/engine_api.py
"""Stable library surface for callers that drive an engine directly.

Localization tools (for example vexy-localizzy) build their own batches, caches and
retry policy. They need one engine, one request type and one result type, not the
file pipeline. Everything here is covered by semantic versioning; the modules it
wraps (``engines``, ``providers.*``) are internal. ``LlmEngine`` and ``EngineConfig``
are re-exported here because callers with their own OpenAI-compatible client construct it directly:
``LlmEngine(EngineConfig(name="ll"), client, model=..., temperature=..., max_attempts=1)``.

Example::

    from abersetz.engine_api import EngineRequest, create_engine

    engine = create_engine("ll::openai:gpt-4o-mini", max_attempts=1)
    result = engine.translate(EngineRequest(text="Hello", source_lang="en",
        target_lang="pl", is_html=False, voc={}, prolog={}, chunk_index=0,
        total_chunks=1))
"""

from __future__ import annotations

from typing import Any

from .config import AbersetzConfig, EngineConfig, load_config
from .providers.base import Engine, EngineError, EngineRequest, EngineResult
from .providers.llm.inference import LlmEngine


def create_engine(
    selector: str,
    *,
    config: AbersetzConfig | None = None,
    client: object | None = None,
    max_attempts: int | None = None,
    **overrides: Any,
) -> Engine:
    """Build the engine named by ``selector`` (``ll::…``, ``tr::…``, ``ml::…`` and so on).

    Args:
        selector: Engine selector, same grammar as the CLI ``--engine``.
        config: Configuration to resolve profiles and credentials; loaded from
            ``abersetz.toml`` when omitted.
        client: OpenAI-compatible client for ``ll`` engines. Injecting one bypasses
            abersetz's built-in HTTP client and its transport-level retries.
        max_attempts: Engine-level attempts per chunk (``>= 1``). ``None`` keeps the
            engine default (3 for ``ll``). ``1`` means the caller owns retries.
            Only ``ll`` engines accept it; other engines raise :class:`EngineError`.
        **overrides: ``temperature``, ``n_gpu_layers``, ``n_ctx``, ``max_tokens``,
            ``n_threads``, passed to the engine factory.

    Raises:
        EngineError: unknown selector, missing credential or model, or
            ``max_attempts`` given for an engine that does not support it.
        ValueError: ``max_attempts`` is not an integer >= 1.
    """
    from .engines import create_engine as _factory

    if max_attempts is not None and (type(max_attempts) is not int or max_attempts < 1):
        raise ValueError(f"max_attempts must be an integer >= 1, got {max_attempts!r}")
    engine = _factory(selector, config or load_config(), client=client, **overrides)
    if max_attempts is None:
        return engine
    if not isinstance(engine, LlmEngine):
        raise EngineError(
            f"max_attempts is supported only for ll engines, not {type(engine).__name__}"
        )
    engine.max_attempts = max_attempts
    return engine


__all__ = [
    "AbersetzConfig",
    "Engine",
    "EngineConfig",
    "EngineError",
    "EngineRequest",
    "EngineResult",
    "LlmEngine",
    "create_engine",
]
