# this_file: src/abersetz/providers/llm/api/together.py
from __future__ import annotations

name = "together"
base_url = "https://api.together.xyz/v1"
api_key_env = "TOGETHERAI_API_KEY"
known_models = [
    "togethercomputer/llama-2-7b-chat",
    "meta-llama/Llama-3-70b-chat-hf",
    "meta-llama/Llama-3-8b-chat-hf",
]
