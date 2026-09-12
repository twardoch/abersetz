# this_file: src/abersetz/providers/hymt2.py
"""Prompt and sampling helpers for Tencent Hy-MT2 translation models.

Every abersetz engine that can run a Hy-MT2 model (``ml``/``gg`` local weights,
``lm`` LM Studio, ``ll`` OpenRouter / Tencent TokenHub) builds its request here so
the official instruction format lives in exactly one place.

The templates follow the "Translation Task Instruction Examples" table in
https://github.com/Tencent-Hunyuan/Hy-MT2 (English column): the model has no
default system prompt, expects a single user turn, and wants the *full English
language name* as the target when the prompt itself is written in English.
"""

from __future__ import annotations

from dataclasses import dataclass

from .base import EngineError

#: (English name, ISO-ish abbreviation, Chinese name) — the 38 rows of the
#: "Supported Languages" table in the upstream README.
HYMT2_LANGUAGE_TABLE: tuple[tuple[str, str, str], ...] = (
    ("Chinese", "zh", "中文"),
    ("English", "en", "英语"),
    ("French", "fr", "法语"),
    ("Portuguese", "pt", "葡萄牙语"),
    ("Spanish", "es", "西班牙语"),
    ("Japanese", "ja", "日语"),
    ("Turkish", "tr", "土耳其语"),
    ("Russian", "ru", "俄语"),
    ("Arabic", "ar", "阿拉伯语"),
    ("Korean", "ko", "韩语"),
    ("Thai", "th", "泰语"),
    ("Italian", "it", "意大利语"),
    ("German", "de", "德语"),
    ("Vietnamese", "vi", "越南语"),
    ("Malay", "ms", "马来语"),
    ("Indonesian", "id", "印尼语"),
    ("Filipino", "tl", "菲律宾语"),
    ("Hindi", "hi", "印地语"),
    ("Traditional Chinese", "zh-Hant", "繁体中文"),
    ("Polish", "pl", "波兰语"),
    ("Czech", "cs", "捷克语"),
    ("Dutch", "nl", "荷兰语"),
    ("Khmer", "km", "高棉语"),
    ("Burmese", "my", "缅甸语"),
    ("Persian", "fa", "波斯语"),
    ("Gujarati", "gu", "古吉拉特语"),
    ("Urdu", "ur", "乌尔都语"),
    ("Telugu", "te", "泰卢固语"),
    ("Marathi", "mr", "马拉地语"),
    ("Hebrew", "he", "希伯来语"),
    ("Bengali", "bn", "孟加拉语"),
    ("Tamil", "ta", "泰米尔语"),
    ("Ukrainian", "uk", "乌克兰语"),
    ("Tibetan", "bo", "藏语"),
    ("Kazakh", "kk", "哈萨克语"),
    ("Mongolian", "mn", "蒙古语"),
    ("Uyghur", "ug", "维吾尔语"),
    ("Cantonese", "yue", "粤语"),
)

#: Extra spellings users type that map onto a table abbreviation.
_LANGUAGE_ALIASES: dict[str, str] = {
    "zh-cn": "zh",
    "zh-hans": "zh",
    "zh-sg": "zh",
    "zh-tw": "zh-hant",
    "zh-hk": "zh-hant",
    "zh-mo": "zh-hant",
    "zh_hant": "zh-hant",
    "fil": "tl",
    "iw": "he",
    "in": "id",
    "pt-br": "pt",
    "pt-pt": "pt",
}

_BY_KEY: dict[str, tuple[str, str, str]] = {}
for _row in HYMT2_LANGUAGE_TABLE:
    _english, _code, _chinese = _row
    _BY_KEY[_english.lower()] = _row
    _BY_KEY[_code.lower()] = _row
    _BY_KEY[_chinese] = _row


def _lookup(code: str) -> tuple[str, str, str]:
    key = code.strip().lower().replace("_", "-")
    key = _LANGUAGE_ALIASES.get(key, key)
    row = _BY_KEY.get(key)
    if row is None and "-" in key:
        row = _BY_KEY.get(key.split("-", 1)[0])
    if row is None:
        raise EngineError(f"Unsupported Hy-MT2 language: {code}")
    return row


def hymt2_language_name(code: str) -> str:
    """Return the English language name Hy-MT2 expects in an English prompt."""
    return _lookup(code)[0]


def hymt2_language_name_zh(code: str) -> str:
    """Return the Chinese language name Hy-MT2 expects in a Chinese prompt."""
    return _lookup(code)[2]


def is_hymt2_model(model_name: str | None) -> bool:
    """Heuristic: does a model id / path / file name denote a Hy-MT2 checkpoint?"""
    if not model_name:
        return False
    flat = model_name.lower().replace("_", "-")
    return "hy-mt2" in flat or "hymt2" in flat


def build_hymt2_prompt(
    source_text: str,
    target_lang: str,
    *,
    voc: dict[str, str] | None = None,
    preamble: str = "",
) -> str:
    """Render the official English Hy-MT2 instruction for one chunk.

    ``voc`` (source term -> target term) becomes the "Terminology" variant of the
    template; ``preamble`` is prepended verbatim (used for translation-memory
    reference pairs from :func:`abersetz.retrieval.reference_context`)."""
    target = hymt2_language_name(target_lang)
    parts: list[str] = []
    if preamble:
        parts.append(preamble.rstrip("\n") + "\n\n")
    if voc:
        lines = "\n".join(f"{src} translates to {tgt}" for src, tgt in sorted(voc.items()))
        parts.append(f"Reference the following translations:\n{lines}\n\n")
        parts.append(
            f"Translate the following text into {target}. Note that you must **ONLY output "
            f"the translated result without any additional explanation**:\n\n{source_text}"
        )
    else:
        parts.append(
            f"Translate the following text into {target}. Note that you should **only output "
            f"the translated result without any additional explanation**:\n\n{source_text}"
        )
    return "".join(parts)


def hymt2_messages(prompt: str) -> list[dict[str, str]]:
    """Hy-MT2 ships without a system prompt: a single user turn is the whole chat."""
    return [{"role": "user", "content": prompt}]


@dataclass(frozen=True, slots=True)
class HyMT2Sampling:
    """Decoding parameters recommended by Tencent for a Hy-MT2 size class."""

    temperature: float
    top_p: float
    top_k: int
    repetition_penalty: float
    max_tokens: int


#: 1.8B and 7B dense models.
HYMT2_SAMPLING_DENSE = HyMT2Sampling(
    temperature=0.7, top_p=0.6, top_k=20, repetition_penalty=1.05, max_tokens=4096
)
#: 30B-A3B mixture-of-experts model (``top_k=-1`` means "disabled").
HYMT2_SAMPLING_MOE = HyMT2Sampling(
    temperature=0.7, top_p=1.0, top_k=-1, repetition_penalty=1.0, max_tokens=4096
)


def hymt2_sampling(model_name: str | None) -> HyMT2Sampling:
    """Pick the recommended sampling block from a model id, path or file name."""
    flat = (model_name or "").lower()
    if "30b" in flat or "a3b" in flat:
        return HYMT2_SAMPLING_MOE
    return HYMT2_SAMPLING_DENSE


__all__ = [
    "HYMT2_LANGUAGE_TABLE",
    "HYMT2_SAMPLING_DENSE",
    "HYMT2_SAMPLING_MOE",
    "HyMT2Sampling",
    "build_hymt2_prompt",
    "hymt2_language_name",
    "hymt2_language_name_zh",
    "hymt2_messages",
    "hymt2_sampling",
    "is_hymt2_model",
]
