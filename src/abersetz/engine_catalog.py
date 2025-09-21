"""Engine catalog utilities for abersetz."""
# this_file: src/abersetz/engine_catalog.py

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

# Provider lists derived from translators README tables
# (see external/translators.txt:1030-1100 for catalogue of public engines)
FREE_TRANSLATOR_PROVIDERS = (
    "google",
    "bing",
    "yandex",
    "argos",
    "apertium",
    "elia",
    "iciba",
    "libre",
    "linguee",
    "myMemory",
    "papago",
    "reverso",
    "tilde",
    "translateCom",
    "translateMe",
    "utibet",
    "youdao",
)

PAID_TRANSLATOR_PROVIDERS = (
    "alibaba",
    "baidu",
    "caiyun",
    "cloudTranslation",
    "deepl",
    "hujiang",
    "iflytek",
    "iflyrec",
    "itranslate",
    "judic",
    "languageWire",
    "lingvanex",
    "mglip",
    "mirai",
    "modernMt",
    "niutrans",
    "qqFanyi",
    "qqTranSmart",
    "sogou",
    "sysTran",
    "volcEngine",
    "yeekit",
)

# Deep-translator engines (external/deep-translator.txt modules list)
DEEP_TRANSLATOR_FREE_PROVIDERS = (
    "google",
    "libre",
    "linguee",
    "my_memory",
)
DEEP_TRANSLATOR_PAID_PROVIDERS = (
    "deepl",
    "microsoft",
    "papago",
)

HYSF_DEFAULT_MODEL = "tencent/Hunyuan-MT-7B"
HYSF_DEFAULT_TEMPERATURE = 0.9


def _filter_available(pool: Iterable[str], allowed: Iterable[str]) -> list[str]:
    pool_set = {item for item in pool}
    ordered: list[str] = []
    for candidate in allowed:
        if candidate in pool_set and candidate not in ordered:
            ordered.append(candidate)
    return ordered


def collect_translator_providers(*, include_paid: bool = False) -> list[str]:
    """Return translator providers available in current environment."""
    try:
        import translators  # type: ignore
    except Exception:
        return []
    pool = translators.translators_pool
    allowed = list(FREE_TRANSLATOR_PROVIDERS)
    if include_paid:
        allowed.extend(PAID_TRANSLATOR_PROVIDERS)
    return _filter_available(pool, allowed)


def collect_deep_translator_providers(*, include_paid: bool = False) -> list[str]:
    """Return deep-translator providers supported by abersetz."""
    pool = list(DEEP_TRANSLATOR_FREE_PROVIDERS)
    if include_paid:
        pool.extend(DEEP_TRANSLATOR_PAID_PROVIDERS)
    seen: set[str] = set()
    ordered: list[str] = []
    for item in pool:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


@dataclass(slots=True)
class EngineEntry:
    """Descriptor for CLI listing."""

    selector: str
    configured: bool
    requires_api_key: bool
    notes: str = ""
