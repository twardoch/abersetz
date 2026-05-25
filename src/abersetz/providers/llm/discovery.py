# this_file: src/abersetz/providers/llm/discovery.py
from __future__ import annotations

import fnmatch
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import httpx
from loguru import logger

from .api import (
    anthropic,
    deepseek,
    gemini,
    groq,
    lmstudio,
    openai,
    openrouter,
    siliconflow,
    together,
)


@dataclass
class Endpoint:
    name: str
    base_url: str
    api_key_env: str
    known_models: list[str] = field(default_factory=list)


BUILTIN_ENDPOINTS = {
    "openai": Endpoint(openai.name, openai.base_url, openai.api_key_env, openai.known_models),
    "siliconflow": Endpoint(
        siliconflow.name, siliconflow.base_url, siliconflow.api_key_env, siliconflow.known_models
    ),
    "groq": Endpoint(groq.name, groq.base_url, groq.api_key_env, groq.known_models),
    "deepseek": Endpoint(
        deepseek.name, deepseek.base_url, deepseek.api_key_env, deepseek.known_models
    ),
    "gemini": Endpoint(gemini.name, gemini.base_url, gemini.api_key_env, gemini.known_models),
    "openrouter": Endpoint(
        openrouter.name, openrouter.base_url, openrouter.api_key_env, openrouter.known_models
    ),
    "together": Endpoint(
        together.name, together.base_url, together.api_key_env, together.known_models
    ),
    "lmstudio": Endpoint(
        lmstudio.name, lmstudio.base_url, lmstudio.api_key_env, lmstudio.known_models
    ),
    "anthropic": Endpoint(
        anthropic.name, anthropic.base_url, anthropic.api_key_env, anthropic.known_models
    ),
}


def discover_env_endpoints() -> dict[str, Endpoint]:
    endpoints = {}
    for key, value in os.environ.items():
        if not value:
            continue
        provider_name = None
        for suffix in ("_API_ENDPOINT", "_API_OPENAI", "_ENDPOINT"):
            if key.endswith(suffix):
                provider_name = key[: -len(suffix)].lower()
                break
        if provider_name:
            api_key_env = f"{provider_name.upper()}_API_KEY"
            endpoints[provider_name] = Endpoint(
                name=provider_name, base_url=value, api_key_env=api_key_env, known_models=[]
            )
    return endpoints


def all_endpoints() -> dict[str, Endpoint]:
    eps = dict(BUILTIN_ENDPOINTS)
    eps.update(discover_env_endpoints())
    return eps


def fetch_models(endpoint: Endpoint) -> list[str]:
    """Fetch model list from the provider's API endpoint."""
    api_key = os.getenv(endpoint.api_key_env)
    if not api_key and endpoint.name == "gemini":
        api_key = os.getenv("GOOGLE_API_KEY")

    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    url = endpoint.base_url.rstrip("/") + "/models"
    try:
        with httpx.Client(timeout=5.0, follow_redirects=True) as client:
            resp = client.get(url, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, dict):
                    if "data" in data and isinstance(data["data"], list):
                        return [
                            str(item["id"])
                            for item in data["data"]
                            if isinstance(item, dict) and "id" in item
                        ]
                    elif "models" in data and isinstance(data["models"], list):
                        return [
                            str(item.get("id") or item.get("name"))
                            for item in data["models"]
                            if isinstance(item, dict)
                        ]
                elif isinstance(data, list):
                    return [
                        str(item.get("id") or item.get("name"))
                        for item in data
                        if isinstance(item, dict)
                    ]
    except Exception as e:
        logger.debug(f"Failed to fetch models from {url}: {e}")
    return []


def resolve_model(selector: str) -> tuple[Endpoint, str]:
    """Resolve a selector (e.g. 'openai:gpt-4o-mini' or just 'gpt-4o-mini') to Endpoint and model_name."""
    eps = all_endpoints()

    selector_lower = selector.strip().lower()
    if selector_lower in eps:
        provider_name = selector_lower
        known = eps[provider_name].known_models
        model_name = known[0] if known else "default"
    elif ":" in selector:
        parts = selector.split(":", 1)
        provider_name = parts[0].strip().lower()
        model_name = parts[1].strip()
    else:
        model_name = selector.strip()
        provider_name = "openai"
        for name, ep in eps.items():
            if model_name in ep.known_models:
                provider_name = name
                break

    if provider_name in eps:
        endpoint = eps[provider_name]
    elif provider_name.startswith(("http://", "https://")):
        endpoint = Endpoint(name="generic", base_url=provider_name, api_key_env="OPENAI_API_KEY")
    else:
        env_url = os.getenv(f"{provider_name.upper()}_API_ENDPOINT")
        if env_url:
            endpoint = Endpoint(
                name=provider_name, base_url=env_url, api_key_env=f"{provider_name.upper()}_API_KEY"
            )
        else:
            endpoint = eps["openai"]

    # If the model_name contains wildcards, try to resolve it to a concrete model name
    if any(wildcard in model_name for wildcard in ("*", "?")):
        model_name = resolve_wildcard_to_model(provider_name, endpoint, model_name)

    return endpoint, model_name


def resolve_wildcard_to_model(provider_name: str, endpoint: Endpoint, pattern: str) -> str:
    """Resolve a wildcard pattern to a concrete model name."""
    # 1. Try matching against built-in known_models first
    matches = fnmatch.filter(endpoint.known_models, pattern)
    if matches:
        return matches[0]

    # 2. Query provider models API
    api_models = fetch_models(endpoint)
    matches = fnmatch.filter(api_models, pattern)
    if matches:
        return matches[0]

    # If no match found, fallback to the pattern as is
    return pattern


def load_recommended_settings(provider_name: str) -> dict[str, Any]:
    """Load settings from recommended_settings.json for a provider."""
    try:
        json_path = Path(__file__).parent / "recommended_settings.json"
        if json_path.exists():
            data = json.loads(json_path.read_text(encoding="utf-8"))
            return data.get(provider_name, data.get("default", {}))
    except Exception:
        pass
    return {
        "temperature": 0.3,
        "max_input_tokens": 8000,
        "max_output_tokens": 2048,
        "chunk_size": 2000,
    }
