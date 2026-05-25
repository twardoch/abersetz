# this_file: src/abersetz/providers/llm/api/lmstudio.py
from __future__ import annotations

name = "lmstudio"
base_url = "http://localhost:1234/v1"
api_key_env = "LMSTUDIO_API_KEY"
known_models = [
    "local-model",
]
