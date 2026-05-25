# this_file: src/abersetz/engines.py

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .config import AbersetzConfig, EngineConfig, resolve_credential
from .engine_catalog import (
    normalize_selector,
    resolve_engine_reference,
)
from .openai_lite import OpenAI

# Import all engine classes and common components from providers
from .providers import (
    DeepTranslatorEngine,
    Engine,
    EngineBase,
    EngineError,
    EngineRequest,
    EngineResult,
    HysfEngine,
    LlmEngine,
    LocalGgufEngine,
    LocalMlxEngine,
    TranslatorsEngine,
)
from .providers.mlx import _resolve_mthy_language

# Re-export for compatibility
_resolve_mthy_language = _resolve_mthy_language


def _make_openai_client(token: str, base_url: str | None) -> OpenAI:
    """Create an OpenAI client respecting optional base URL.

    Points the client at OpenAI, SiliconFlow, or any local proxy that speaks the OpenAI protocol."""
    if base_url:
        return OpenAI(api_key=token, base_url=base_url)
    return OpenAI(api_key=token)


def _build_llm_engine(
    selector: str,
    config: AbersetzConfig,
    engine_cfg: EngineConfig,
    *,
    profile: Mapping[str, Any] | None,
    client: Any | None,
) -> Engine:
    options = dict(engine_cfg.options)
    settings = dict(profile or {})
    base_url = settings.get("base_url") or options.get("base_url")
    model = settings.get("model") or options.get("model")
    if not model:
        raise EngineError(f"No model configured for engine {selector}")
    temperature = float(settings.get("temperature", options.get("temperature", 0.9)))
    token = resolve_credential(config, engine_cfg.credential)
    if token is None:
        raise EngineError(f"Missing credential for engine {selector}")
    openai_client = client or _make_openai_client(token, base_url)
    static_prolog = settings.get("prolog") or options.get("prolog") or {}
    return LlmEngine(
        engine_cfg,
        openai_client,
        model=model,
        temperature=temperature,
        static_prolog=static_prolog,
    )


def _build_hysf_engine(
    selector: str,
    config: AbersetzConfig,
    engine_cfg: EngineConfig,
    *,
    client: Any | None,
) -> Engine:
    token = resolve_credential(config, engine_cfg.credential)
    if token is None:
        raise EngineError(f"Missing credential for engine {selector}")
    base_url = engine_cfg.options.get("base_url")
    openai_client = client or _make_openai_client(token, base_url)
    return HysfEngine(engine_cfg, openai_client)


def _translators_provider(variant: str | None, engine_cfg: EngineConfig) -> str:
    return variant or engine_cfg.options.get("provider", "google")


def _select_profile(engine_cfg: EngineConfig, variant: str | None) -> Mapping[str, Any] | None:
    profiles = engine_cfg.options.get("profiles", {})
    if not profiles:
        return None
    profile_name = variant or "default"
    if profile_name not in profiles:
        raise EngineError(f"Unknown profile '{profile_name}' for engine '{engine_cfg.name}'")
    return profiles[profile_name]


def create_engine(
    selector: str,
    config: AbersetzConfig,
    *,
    client: Any | None = None,
) -> Engine:
    """Factory that builds the requested engine supporting short aliases."""
    normalized = normalize_selector(selector) or selector
    base, variant = resolve_engine_reference(normalized)

    engine_cfg = config.engines.get(base)
    if engine_cfg is None:
        raise EngineError(f"No configuration found for engine '{base}'")
    if base == "translators":
        provider = _translators_provider(variant, engine_cfg)
        return TranslatorsEngine(provider, engine_cfg)
    if base == "deep-translator":
        provider = _translators_provider(variant, engine_cfg)
        return DeepTranslatorEngine(provider, engine_cfg)
    if base == "hysf":
        return _build_hysf_engine(normalized, config, engine_cfg, client=client)
    if base == "ullm":
        profile = _select_profile(engine_cfg, variant)
        return _build_llm_engine(normalized, config, engine_cfg, profile=profile, client=client)
    if base in {"mthy", "gemma"}:
        options = dict(engine_cfg.options)
        backend = (variant or options.get("backend") or "").strip().lower()
        if not backend:
            raise EngineError(f"No backend configured for engine {normalized}")
        models = options.get("models")
        model_map = models if isinstance(models, Mapping) else {}
        model_path = (
            options.get(f"{backend}_path") or options.get("model_path") or model_map.get(backend)
        )
        max_tokens = int(options.get("max_tokens", 2048))
        temperature = float(options.get("temperature", 0.0))
        n_gpu_layers = int(options.get("n_gpu_layers", -1))
        n_ctx = int(options.get("n_ctx", 4096))
        if backend == "mlx":
            return LocalMlxEngine(base, engine_cfg, str(model_path or ""), max_tokens=max_tokens)
        if backend == "gguf":
            return LocalGgufEngine(
                base,
                engine_cfg,
                str(model_path or ""),
                max_tokens=max_tokens,
                temperature=temperature,
                n_gpu_layers=n_gpu_layers,
                n_ctx=n_ctx,
            )
        raise EngineError(f"Unsupported backend '{backend}' for engine '{normalized}'")
    raise EngineError(f"Unsupported engine '{base}'")


__all__ = [
    "Engine",
    "EngineBase",
    "EngineError",
    "EngineRequest",
    "EngineResult",
    "create_engine",
]
