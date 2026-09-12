# this_file: src/abersetz/providers/llm/api/tencent.py
"""Tencent Cloud TokenHub (international endpoint) — hosts the Hy-MT2 API tiers."""

from __future__ import annotations

name = "tencent"
base_url = "https://tokenhub-intl.tencentcloudmaas.com/v1"
api_key_env = "TENCENTCLOUD_API_KEY"
#: Hosted Hy-MT2 tiers; ``hy-mt2-pro`` is the default when only ``tencent`` is given.
known_models = [
    "hy-mt2-pro",
    "hy-mt2-plus",
    "hy-mt2-lite",
]
