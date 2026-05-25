# this_file: src/abersetz/providers/llm/api/siliconflow.py
from __future__ import annotations

name = "siliconflow"
base_url = "https://api.siliconflow.cn/v1"
api_key_env = "SILICONFLOW_API_KEY"
known_models = [
    "Qwen/Qwen2.5-7B-Instruct",
    "Qwen/Qwen2.5-14B-Instruct",
    "Qwen/Qwen2.5-72B-Instruct",
    "THUDM/glm-4-9b-chat",
    "01-ai/Yi-1.5-9B-Chat-16K",
]
