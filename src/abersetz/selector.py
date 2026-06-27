"""Engine selector grammar for abersetz.

A *selector* names an engine, an optional subvariant, and an optional provider
in the form ``engine[/subvariant]::provider``. The six engine codes are:

| Code | Engine |
|------|--------|
| ``tr`` | ``translators`` package (web scrapers) |
| ``dt`` | ``deep-translator`` package |
| ``lm`` | LMStudio Python SDK |
| ``ll`` | OpenAI-compatible LLM API |
| ``ml`` | local MLX model (``mlx_lm``) |
| ``gg`` | local GGUF model (``llama.cpp``) |

Examples::

    tr::google              translators / Google
    dt::deepl               deep-translator / DeepL
    lm::gemma-3-4b          LMStudio model id
    ll::siliconflow:Qwen/Qwen2.5-7B-Instruct
    ml/hy-mt2::/models/Hy-MT2-7B
    gg/gemma::/models/gemma.gguf

The legacy ``engine/provider`` form (``tr/google``, ``ll/default``) is still
accepted so existing configs keep working; it is parsed into the same
:class:`Selector`."""

# this_file: src/abersetz/selector.py

from __future__ import annotations

import re
from dataclasses import dataclass

#: Canonical two-letter engine codes.
ENGINE_CODES: frozenset[str] = frozenset({"tr", "dt", "lm", "ll", "ml", "gg"})

#: Map every accepted spelling (legacy long names, old short codes) to a
#: canonical engine code.
_ENGINE_ALIASES: dict[str, str] = {
    "tr": "tr",
    "translators": "tr",
    "dt": "dt",
    "deep-translator": "dt",
    "deep_translator": "dt",
    "lm": "lm",
    "lms": "lm",
    "lmstudio": "lm",
    "ll": "ll",
    "ullm": "ll",
    "ml": "ml",
    "mlx": "ml",
    "gg": "gg",
    "gguf": "gg",
}

#: Subvariant names for local engines collapse onto an internal prompt family.
_SUBVARIANT_TO_FAMILY: dict[str, str] = {
    "hy-mt2": "mthy",
    "hymt2": "mthy",
    "mthy": "mthy",
    "hunyuan": "mthy",
    "gemma": "gemma",
}

#: Default prompt family for local engines when no subvariant is given.
DEFAULT_LOCAL_FAMILY = "mthy"


@dataclass(slots=True, frozen=True)
class Selector:
    """A parsed engine selector.

    ``engine`` is always a canonical code from :data:`ENGINE_CODES` (or the raw
    base if it could not be recognised). ``subvariant`` is the optional token
    between the slash and ``::``. ``provider`` is the free-form text after
    ``::`` (a translation backend, model id, ``endpoint:model`` spec, or model
    path)."""

    engine: str
    subvariant: str | None
    provider: str | None
    raw: str

    @property
    def family(self) -> str:
        """Internal prompt family for local (``ml``/``gg``) engines."""
        if self.subvariant is None:
            return DEFAULT_LOCAL_FAMILY
        return _SUBVARIANT_TO_FAMILY.get(self.subvariant.lower(), self.subvariant.lower())

    def canonical(self) -> str:
        """Render the canonical ``engine[/subvariant]::provider`` string."""
        head = self.engine
        if self.subvariant:
            head = f"{head}/{self.subvariant}"
        if self.provider is not None:
            return f"{head}::{self.provider}"
        return f"{head}::"


def parse_selector(raw: str | None) -> Selector | None:
    """Parse a selector string into a :class:`Selector`.

    Accepts both the new ``engine[/subvariant]::provider`` grammar and the
    legacy ``engine[/provider]`` form. Returns ``None`` for ``None`` input and a
    selector with empty engine for blank input."""
    if raw is None:
        return None
    trimmed = raw.strip()
    if not trimmed:
        return Selector(engine="", subvariant=None, provider=None, raw=trimmed)

    if "::" in trimmed:
        left, _, provider = trimmed.partition("::")
        provider_clean = provider.strip() or None
        base, _, sub = left.strip().partition("/")
        engine = _ENGINE_ALIASES.get(base.strip().lower(), base.strip().lower())
        subvariant = sub.strip() or None
        return Selector(engine=engine, subvariant=subvariant, provider=provider_clean, raw=trimmed)

    # Legacy form: engine[/provider]. The slashed token is the provider here.
    base, _, variant = trimmed.partition("/")
    base_clean = base.strip().lower()
    engine = _ENGINE_ALIASES.get(base_clean, base_clean)
    variant_clean = variant.strip() or None
    # Legacy local engines encode the backend in the variant (mthy/mlx).
    if base_clean in {"mthy", "gemma"} and variant_clean in {"mlx", "gguf"}:
        family = "mthy" if base_clean == "mthy" else "gemma"
        engine = "ml" if variant_clean == "mlx" else "gg"
        return Selector(engine=engine, subvariant=family, provider=None, raw=trimmed)
    return Selector(engine=engine, subvariant=None, provider=variant_clean, raw=trimmed)


def is_new_syntax(raw: str | None) -> bool:
    """Return whether the selector uses the new ``::`` grammar."""
    return bool(raw) and "::" in raw


def slugify_selector(selector: Selector | str) -> str:
    """Build a filesystem-safe suffix identifying engine, subvariant and provider.

    Used to name benchmark output files, e.g. ``tr::google`` -> ``tr-google`` and
    ``ll::siliconflow:Qwen/Qwen2.5-7B`` -> ``ll-siliconflow-qwen-qwen2-5-7b``."""
    sel = parse_selector(selector) if isinstance(selector, str) else selector
    if sel is None:
        return "engine"
    parts = [sel.engine]
    if sel.subvariant:
        parts.append(sel.subvariant)
    if sel.provider:
        # For local model paths, keep only the final path component for brevity.
        provider = sel.provider
        if sel.engine in {"ml", "gg"} and "/" in provider:
            tail = provider.rstrip("/").split("/")[-1]
            provider = tail or provider
        parts.append(provider)
    slug = "-".join(parts).lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return slug or "engine"


__all__ = [
    "ENGINE_CODES",
    "DEFAULT_LOCAL_FAMILY",
    "Selector",
    "parse_selector",
    "is_new_syntax",
    "slugify_selector",
]
