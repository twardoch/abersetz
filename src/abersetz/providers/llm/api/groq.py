# this_file: src/abersetz/providers/llm/api/groq.py
from __future__ import annotations

name = "groq"
base_url = "https://api.groq.com/openai/v1"
api_key_env = "GROQ_API_KEY"
known_models = [
    "llama-3.3-70b-versatile",
    "llama3-70b-8192",
    "llama3-8b-8192",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]
