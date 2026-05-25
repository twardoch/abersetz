# this_file: src/abersetz/providers/llm/api/deepseek.py
from __future__ import annotations

name = "deepseek"
base_url = "https://api.deepseek.com/v1"
api_key_env = "DEEPSEEK_API_KEY"
known_models = [
    "deepseek-chat",
    "deepseek-reasoner",
]
