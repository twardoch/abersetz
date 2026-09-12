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
from .providers.hymt2 import hymt2_sampling
from .providers.llm.inference import llm_prompt_family
from .providers.lmstudio import lmstudio_family
from .providers.local_models import family_for_model
from .providers.salamandra import SALAMANDRA_TEMPERATURE
from .providers.translategemma import TRANSLATEGEMMA_TEMPERATURE
from .selector import Selector, is_new_syntax, parse_selector


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
    subvariant: str | None = None,
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
    family = llm_prompt_family(model, subvariant)
    configured_temp = settings.get("temperature", options.get("temperature"))
    temp = _llm_temperature(temperature, configured_temp, family, model, fallback=0.9)
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
        prompt_family=family,
    )


def _credential_matches(reference: Any, endpoint_name: str) -> bool:
    from .config import Credential

    credential = Credential.from_any(reference)
    return bool(credential and credential.name and credential.name.lower() == endpoint_name)


def _llm_temperature(
    override: float | None, configured: Any, family: str, model: str, *, fallback: float
) -> float:
    """CLI override > config value > model-family recommendation > generic fallback."""
    if override is not None:
        return override
    if configured is not None:
        return float(configured)
    if family == "mthy":
        return hymt2_sampling(model).temperature
    if family == "gemma":
        return TRANSLATEGEMMA_TEMPERATURE
    if family == "salamandra":
        return SALAMANDRA_TEMPERATURE
    return fallback


def _create_dynamic_llm_engine(
    variant: str | None,
    config: AbersetzConfig,
    engine_cfg: EngineConfig | None,
    *,
    client: Any | None,
    temperature: float | None,
    subvariant: str | None = None,
) -> Engine:
    """Build an ``ll`` engine from an ``endpoint:model`` spec (no config profile)."""
    from .providers.llm.discovery import (
        endpoint_api_key,
        load_recommended_settings,
        resolve_model,
    )

    try:
        sel = variant if variant else "siliconflow"
        endpoint, resolved_model_name = resolve_model(sel)
    except Exception as e:
        raise EngineError(f"Failed to resolve LLM model from '{variant}': {e}") from e

    rec = load_recommended_settings(endpoint.name)

    token = endpoint_api_key(endpoint)
    if not token and engine_cfg and _credential_matches(engine_cfg.credential, endpoint.name):
        # Only borrow the configured ``ullm`` credential when it belongs to this
        # provider; never send one vendor's key to another vendor's endpoint.
        token = resolve_credential(config, engine_cfg.credential)

    if not token:
        raise EngineError(
            f"Missing API key for provider '{endpoint.name}'. "
            f"Please set the environment variable '{endpoint.api_key_env}'."
        )

    model = resolved_model_name
    family = llm_prompt_family(model, subvariant)
    temp = _llm_temperature(
        temperature, None, family, model, fallback=float(rec.get("temperature", 0.3))
    )

    openai_client = client or _make_openai_client(token, endpoint.base_url)
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
        prompt_family=family,
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


def _optional_int(override: int | None, configured: Any) -> int | None:
    """CLI override wins, then the config value; ``None`` lets the engine pick a default."""
    if override is not None:
        return override
    return int(configured) if configured is not None else None


def _optional_float(override: float | None, configured: Any) -> float | None:
    if override is not None:
        return override
    return float(configured) if configured is not None else None


def _local_engine_config(config: AbersetzConfig, family: str) -> EngineConfig:
    """Return the configured block for a local family or a bare default."""
    return config.engines.get(family) or EngineConfig(name=family)


def _create_from_selector(
    sel: Selector,
    config: AbersetzConfig,
    *,
    client: Any | None,
    temperature: float | None,
    n_gpu_layers: int | None,
    n_ctx: int | None,
    max_tokens: int | None,
    n_threads: int | None,
) -> Engine:
    """Build an engine from a parsed ``engine[/subvariant]::provider`` selector.

    Delegates ``tr``/``dt``/``ll`` to the legacy factory (which already knows how
    to read provider/profile config) and builds the model-path engines
    (``lm``/``ml``/``gg``) directly so the provider can carry a model id or path."""
    engine = sel.engine
    provider = sel.provider

    if engine == "tr":
        return create_engine(f"tr/{provider}" if provider else "tr", config, client=client)
    if engine == "dt":
        return create_engine(f"dt/{provider}" if provider else "dt", config, client=client)
    if engine == "ll":
        engine_cfg = config.engines.get("ullm")
        profiles = engine_cfg.options.get("profiles", {}) if engine_cfg else {}
        if provider and engine_cfg is not None and provider in profiles:
            return _build_llm_engine(
                sel.raw,
                config,
                engine_cfg,
                profile=profiles[provider],
                client=client,
                temperature=temperature,
                subvariant=sel.subvariant,
            )
        return _create_dynamic_llm_engine(
            provider,
            config,
            engine_cfg,
            client=client,
            temperature=temperature,
            subvariant=sel.subvariant,
        )
    if engine == "lm":
        base_cfg = config.engines.get("lmstudio")
        options = dict(base_cfg.options) if base_cfg else {"base_url": "localhost:1234"}
        if provider:
            options["model"] = provider
        cfg = EngineConfig(
            name="lmstudio",
            chunk_size=base_cfg.chunk_size if base_cfg else None,
            html_chunk_size=base_cfg.html_chunk_size if base_cfg else None,
            options=options,
        )
        family = lmstudio_family(options.get("model"), sel.subvariant)
        return LmstudioEngine(cfg, temperature=temperature, family=family)
    if engine in {"ml", "gg"}:
        # ``ml/hy-mt2::x`` names the family explicitly; ``ml::translategemma-4b``
        # infers it from the model, falling back to Hy-MT2.
        family = sel.family if sel.subvariant else (family_for_model(provider) or sel.family)
        engine_cfg = _local_engine_config(config, family)
        options = dict(engine_cfg.options)
        model_path = (
            provider
            or options.get("model_path")
            or options.get("mlx_path" if engine == "ml" else "gguf_path")
        )
        max_tokens_val = _optional_int(max_tokens, options.get("max_tokens"))
        temp_val = _optional_float(temperature, options.get("temperature"))
        if engine == "ml":
            return LocalMlxEngine(
                family,
                engine_cfg,
                str(model_path or ""),
                max_tokens=max_tokens_val,
                temperature=temp_val,
            )
        n_gpu_layers_val = (
            n_gpu_layers if n_gpu_layers is not None else int(options.get("n_gpu_layers", -1))
        )
        n_ctx_val = _optional_int(n_ctx, options.get("n_ctx"))
        n_threads_val = _optional_int(n_threads, options.get("n_threads"))
        return LocalGgufEngine(
            family,
            engine_cfg,
            str(model_path or ""),
            max_tokens=max_tokens_val,
            temperature=temp_val,
            n_gpu_layers=n_gpu_layers_val,
            n_ctx=n_ctx_val,
            n_threads=n_threads_val,
        )
    raise EngineError(f"Unsupported engine code '{engine}' in selector '{sel.raw}'")


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
    # New ``engine[/subvariant]::provider`` grammar is handled separately; the
    # legacy ``engine/provider`` form falls through to the original dispatch.
    if is_new_syntax(selector):
        parsed = parse_selector(selector)
        assert parsed is not None
        return _create_from_selector(
            parsed,
            config,
            client=client,
            temperature=temperature,
            n_gpu_layers=n_gpu_layers,
            n_ctx=n_ctx,
            max_tokens=max_tokens,
            n_threads=n_threads,
        )
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
        # Dynamic loading (e.g. ullm/siliconflow:Qwen/Qwen2.5-7B-Instruct)
        return _create_dynamic_llm_engine(
            variant, config, engine_cfg, client=client, temperature=temperature
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
        max_tokens_val = _optional_int(max_tokens, options.get("max_tokens"))
        temp_val = _optional_float(temperature, options.get("temperature"))
        n_gpu_layers_val = (
            n_gpu_layers if n_gpu_layers is not None else int(options.get("n_gpu_layers", -1))
        )
        n_ctx_val = _optional_int(n_ctx, options.get("n_ctx"))
        n_threads_val = _optional_int(n_threads, options.get("n_threads"))
        if backend == "mlx":
            return LocalMlxEngine(
                base,
                engine_cfg,
                str(model_path or ""),
                max_tokens=max_tokens_val,
                temperature=temp_val,
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
