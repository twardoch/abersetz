# this_file: src/abersetz/providers/llm/api/openai.py
from __future__ import annotations

name = "openai"
base_url = "https://api.openai.com/v1"
api_key_env = "OPENAI_API_KEY"
known_models = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4-turbo",
    "gpt-3.5-turbo",
]
