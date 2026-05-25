# this_file: src/abersetz/providers/llm/api/gemini.py
from __future__ import annotations

name = "gemini"
base_url = "https://generativelanguage.googleapis.com/v1beta/openai"
api_key_env = "GOOGLE_API_KEY"
known_models = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-1.5-flash",
    "gemini-1.5-pro",
]
