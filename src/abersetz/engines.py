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
    LlmEngine,
    LmstudioEngine,
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
    temperature: float | None = None,
) -> Engine:
    options = dict(engine_cfg.options)
    settings = dict(profile or {})
    base_url = settings.get("base_url") or options.get("base_url")
    model = settings.get("model") or options.get("model")
    if not model:
        raise EngineError(f"No model configured for engine {selector}")
    if "Hunyuan-MT-7B" in model:
        raise EngineError(
            f"The model '{model}' has been discontinued by SiliconFlow. Please update your configuration "
            f"to a supported model, such as 'Qwen/Qwen2.5-7B-Instruct'."
        )
    temp = (
        temperature
        if temperature is not None
        else float(settings.get("temperature", options.get("temperature", 0.9)))
    )
    token = resolve_credential(config, engine_cfg.credential)
    if token is None:
        raise EngineError(f"Missing credential for engine {selector}")
    openai_client = client or _make_openai_client(token, base_url)
    static_prolog = settings.get("prolog") or options.get("prolog") or {}
    return LlmEngine(
        engine_cfg,
        openai_client,
        model=model,
        temperature=temp,
        static_prolog=static_prolog,
    )


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
    temperature: float | None = None,
    n_gpu_layers: int | None = None,
    n_ctx: int | None = None,
    max_tokens: int | None = None,
    n_threads: int | None = None,
) -> Engine:
    """Factory that builds the requested engine supporting short aliases."""
    normalized = normalize_selector(selector) or selector
    base, variant = resolve_engine_reference(normalized)

    engine_cfg = config.engines.get(base)
    if engine_cfg is None and base not in {"ullm", "lmstudio"}:
        raise EngineError(f"No configuration found for engine '{base}'")
    if base == "translators":
        assert engine_cfg is not None
        provider = _translators_provider(variant, engine_cfg)
        return TranslatorsEngine(provider, engine_cfg)
    if base == "deep-translator":
        assert engine_cfg is not None
        provider = _translators_provider(variant, engine_cfg)
        return DeepTranslatorEngine(provider, engine_cfg)
    if base == "lmstudio":
        # Create a default engine config if not present in TOML config
        cfg = (
            engine_cfg
            or config.engines.get("lmstudio")
            or EngineConfig(
                name="lmstudio", options={"base_url": "localhost:1234", "model": "local-model"}
            )
        )
        return LmstudioEngine(cfg, temperature=temperature)
    if base == "ullm":
        # Check profiles
        profiles = engine_cfg.options.get("profiles", {}) if engine_cfg else {}
        profile = None
        if variant and profiles and variant in profiles:
            profile = profiles[variant]

        if profile is not None:
            assert engine_cfg is not None
            return _build_llm_engine(
                normalized,
                config,
                engine_cfg,
                profile=profile,
                client=client,
                temperature=temperature,
            )
        else:
            # Dynamic loading (e.g. ullm/siliconflow:Qwen/Qwen2.5-7B-Instruct)
            import os

            from .providers.llm.discovery import load_recommended_settings, resolve_model

            try:
                sel = variant if variant else "siliconflow"
                endpoint, resolved_model_name = resolve_model(sel)
            except Exception as e:
                raise EngineError(f"Failed to resolve LLM model from '{variant}': {e}") from e

            rec = load_recommended_settings(endpoint.name)

            token = os.getenv(endpoint.api_key_env)
            if not token and endpoint.name == "gemini":
                token = os.getenv("GOOGLE_API_KEY")
            if not token and engine_cfg:
                token = resolve_credential(config, engine_cfg.credential)

            if not token:
                raise EngineError(
                    f"Missing API key for provider '{endpoint.name}'. "
                    f"Please set the environment variable '{endpoint.api_key_env}'."
                )

            base_url = endpoint.base_url
            model = resolved_model_name
            temp = temperature if temperature is not None else rec.get("temperature", 0.3)

            openai_client = client or _make_openai_client(token, base_url)
            dummy_cfg = EngineConfig(
                name=f"ullm/{variant}" if variant else "ullm",
                chunk_size=rec.get("chunk_size", 2000),
                html_chunk_size=rec.get("chunk_size", 2000),
            )

            return LlmEngine(
                dummy_cfg,
                openai_client,
                model=model,
                temperature=temp,
                static_prolog={},
            )
    if base in {"mthy", "gemma"}:
        assert engine_cfg is not None
        options = dict(engine_cfg.options)
        backend = (variant or options.get("backend") or "").strip().lower()
        if not backend:
            raise EngineError(f"No backend configured for engine {normalized}")
        models = options.get("models")
        model_map = models if isinstance(models, Mapping) else {}
        model_path = (
            options.get(f"{backend}_path") or options.get("model_path") or model_map.get(backend)
        )
        max_tokens_val = (
            max_tokens if max_tokens is not None else int(options.get("max_tokens", 2048))
        )
        temp_val = (
            temperature if temperature is not None else float(options.get("temperature", 0.0))
        )
        n_gpu_layers_val = (
            n_gpu_layers if n_gpu_layers is not None else int(options.get("n_gpu_layers", -1))
        )
        n_ctx_val = n_ctx if n_ctx is not None else int(options.get("n_ctx", 4096))
        n_threads_raw = options.get("n_threads")
        n_threads_val = (
            n_threads
            if n_threads is not None
            else (int(n_threads_raw) if n_threads_raw is not None else None)
        )
        if backend == "mlx":
            return LocalMlxEngine(
                base, engine_cfg, str(model_path or ""), max_tokens=max_tokens_val
            )
        if backend == "gguf":
            return LocalGgufEngine(
                base,
                engine_cfg,
                str(model_path or ""),
                max_tokens=max_tokens_val,
                temperature=temp_val,
                n_gpu_layers=n_gpu_layers_val,
                n_ctx=n_ctx_val,
                n_threads=n_threads_val,
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
