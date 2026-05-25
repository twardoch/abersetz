# this_file: src/abersetz/providers/llm/api/openrouter.py
from __future__ import annotations

name = "openrouter"
base_url = "https://openrouter.ai/api/v1"
api_key_env = "OPENROUTER_API_KEY"
known_models = [
    "google/gemma-2-9b-it:free",
    "meta-llama/llama-3-8b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "openrouter/auto",
]
