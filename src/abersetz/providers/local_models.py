# this_file: src/abersetz/providers/local_models.py
"""Known local translation checkpoints and the alias -> path resolver.

Used by the ``ml`` (MLX) and ``gg`` (GGUF) engines. A provider string can be a
path on disk, a short alias from :data:`ALIASES`, a Hugging Face repo id
(optionally ``repo:QUANT`` for GGUF repos with several quantisations), or any
model name that local discovery (LM Studio, HF cache, Ollama, …) can find.
"""

from __future__ import annotations

from pathlib import Path

from .base import EngineError

#: Hugging Face repos abersetz knows how to fetch. ``filename`` is the default
#: GGUF file; pass ``repo:QUANT`` to pick another quantisation from the repo.
KNOWN_MAPPING: dict[str, dict[str, str]] = {
    # --- Hy-MT2, MLX -------------------------------------------------------
    "kuotient/Hy-MT2-1.8B-1.25Bit-MLX": {
        "repo": "kuotient/Hy-MT2-1.8B-1.25Bit-MLX",
        "type": "mlx",
        "family": "mthy",
    },
    "mlx-community/Hy-MT2-1.8B-8bit": {
        "repo": "mlx-community/Hy-MT2-1.8B-8bit",
        "type": "mlx",
        "family": "mthy",
    },
    "mlx-community/Hy-MT2-1.8B-bf16": {
        "repo": "mlx-community/Hy-MT2-1.8B-bf16",
        "type": "mlx",
        "family": "mthy",
    },
    "mlx-community/Hy-MT2-7B-8bit": {
        "repo": "mlx-community/Hy-MT2-7B-8bit",
        "type": "mlx",
        "family": "mthy",
    },
    "mlx-community/Hy-MT2-7B-bf16": {
        "repo": "mlx-community/Hy-MT2-7B-bf16",
        "type": "mlx",
        "family": "mthy",
    },
    "dawncr0w/Hy-MT2-30B-A3B-oQ8-MLX": {
        "repo": "dawncr0w/Hy-MT2-30B-A3B-oQ8-MLX",
        "type": "mlx",
        "family": "mthy",
    },
    # --- Hy-MT2, GGUF ------------------------------------------------------
    "tencent/Hy-MT2-1.8B-1.25Bit-GGUF": {
        "repo": "tencent/Hy-MT2-1.8B-1.25Bit-GGUF",
        "filename": "Hy-MT2-1.8B-1.25Bit.gguf",
        "type": "gguf",
        "family": "mthy",
    },
    "tencent/Hy-MT2-1.8B-2Bit-GGUF": {
        "repo": "tencent/Hy-MT2-1.8B-2Bit-GGUF",
        "filename": "Hy-MT2-1.8B-2Bit.gguf",
        "type": "gguf",
        "family": "mthy",
    },
    "tencent/Hy-MT2-1.8B-GGUF": {
        "repo": "tencent/Hy-MT2-1.8B-GGUF",
        "filename": "Hy-MT2-1.8B-Q8_0.gguf",
        "type": "gguf",
        "family": "mthy",
    },
    "tencent/Hy-MT2-7B-GGUF": {
        "repo": "tencent/Hy-MT2-7B-GGUF",
        "filename": "HY-MT2-7B-Q8_0.gguf",
        "type": "gguf",
        "family": "mthy",
    },
    "mradermacher/Hy-MT2-30B-A3B-GGUF": {
        "repo": "mradermacher/Hy-MT2-30B-A3B-GGUF",
        "filename": "Hy-MT2-30B-A3B.Q4_K_M.gguf",
        "type": "gguf",
        "family": "mthy",
    },
    # --- MADLAD-400 (T5), GGUF ---------------------------------------------
    "thirteenbit/madlad400-10b-mt-gguf": {
        "repo": "thirteenbit/madlad400-10b-mt-gguf",
        "filename": "model-q8_0.gguf",
        "type": "gguf",
        "family": "madlad",
    },
    # --- SalamandraTA, GGUF ------------------------------------------------
    "mradermacher/salamandraTA-7b-instruct-GGUF": {
        "repo": "mradermacher/salamandraTA-7b-instruct-GGUF",
        "filename": "salamandraTA-7b-instruct.Q8_0.gguf",
        "type": "gguf",
        "family": "salamandra",
    },
    # --- TranslateGemma, MLX ----------------------------------------------
    "mlx-community/translategemma-4b-it-8bit": {
        "repo": "mlx-community/translategemma-4b-it-8bit",
        "type": "mlx",
        "family": "gemma",
    },
    "mlx-community/translategemma-12b-it-8bit": {
        "repo": "mlx-community/translategemma-12b-it-8bit",
        "type": "mlx",
        "family": "gemma",
    },
    "mlx-community/translategemma-27b-it-8bit": {
        "repo": "mlx-community/translategemma-27b-it-8bit",
        "type": "mlx",
        "family": "gemma",
    },
    "mlx-community/translategemma-27b-it-4bit": {
        "repo": "mlx-community/translategemma-27b-it-4bit",
        "type": "mlx",
        "family": "gemma",
    },
    # --- TranslateGemma, GGUF ---------------------------------------------
    "mradermacher/translategemma-4b-it-GGUF": {
        "repo": "mradermacher/translategemma-4b-it-GGUF",
        "filename": "translategemma-4b-it.Q8_0.gguf",
        "type": "gguf",
        "family": "gemma",
    },
    "mradermacher/translategemma-12b-it-GGUF": {
        "repo": "mradermacher/translategemma-12b-it-GGUF",
        "filename": "translategemma-12b-it.Q8_0.gguf",
        "type": "gguf",
        "family": "gemma",
    },
    "mradermacher/translategemma-27b-it-GGUF": {
        "repo": "mradermacher/translategemma-27b-it-GGUF",
        "filename": "translategemma-27b-it.Q4_K_M.gguf",
        "type": "gguf",
        "family": "gemma",
    },
}

#: Short names accepted after ``::`` in ``ml``/``gg`` selectors.
ALIASES: dict[str, str] = {
    # Hy-MT2 MLX
    "1.8b-1.25bit-mlx": "kuotient/Hy-MT2-1.8B-1.25Bit-MLX",
    "1.8b-mlx": "mlx-community/Hy-MT2-1.8B-8bit",
    "1.8b-8bit-mlx": "mlx-community/Hy-MT2-1.8B-8bit",
    "1.8b-bf16-mlx": "mlx-community/Hy-MT2-1.8B-bf16",
    "7b-mlx": "mlx-community/Hy-MT2-7B-8bit",
    "7b-8bit-mlx": "mlx-community/Hy-MT2-7B-8bit",
    "7b-bf16-mlx": "mlx-community/Hy-MT2-7B-bf16",
    "30b-mlx": "dawncr0w/Hy-MT2-30B-A3B-oQ8-MLX",
    # Hy-MT2 GGUF
    "1.8b-1.25bit": "tencent/Hy-MT2-1.8B-1.25Bit-GGUF",
    "1.8b-2bit": "tencent/Hy-MT2-1.8B-2Bit-GGUF",
    "1.8b-gguf": "tencent/Hy-MT2-1.8B-GGUF",
    "7b-gguf": "tencent/Hy-MT2-7B-GGUF",
    "30b-gguf": "mradermacher/Hy-MT2-30B-A3B-GGUF",
    # MADLAD-400 / SalamandraTA GGUF
    "madlad-10b": "thirteenbit/madlad400-10b-mt-gguf",
    "salamandra-7b": "mradermacher/salamandraTA-7b-instruct-GGUF",
    # TranslateGemma MLX
    "tg-4b-mlx": "mlx-community/translategemma-4b-it-8bit",
    "tg-12b-mlx": "mlx-community/translategemma-12b-it-8bit",
    "tg-27b-mlx": "mlx-community/translategemma-27b-it-8bit",
    "tg-27b-4bit-mlx": "mlx-community/translategemma-27b-it-4bit",
    # TranslateGemma GGUF
    "tg-4b-gguf": "mradermacher/translategemma-4b-it-GGUF",
    "tg-12b-gguf": "mradermacher/translategemma-12b-it-GGUF",
    "tg-27b-gguf": "mradermacher/translategemma-27b-it-GGUF",
}

_LEGACY_HYMT1_MARKERS = ("Hunyuan-MT-7B", "Hunyuan-MT1", "Hy-MT1", "HY-MT1")


def default_model_for(backend: str) -> str:
    """Smallest Hy-MT2 checkpoint, used when a selector names no model at all."""
    return "1.8b-mlx" if backend == "mlx" else "1.8b-gguf"


def find_local_model_path(model_identifier: str, backend: str) -> str | None:
    """Query LocalModelFinder to locate the model locally on disk."""
    try:
        from .llm.local_discovery import LocalModelFinder

        finder = LocalModelFinder()

        # Determine format filter for discovery
        fmt_filter = "gguf" if backend == "gguf" else None
        discovered = finder.discover_models(format_filter=fmt_filter)

        target = model_identifier.replace("\\", "/").strip().lower()
        target_parts = [p for p in target.split("/") if p]

        for m in discovered:
            path_str = str(m.path).replace("\\", "/").lower()

            def get_return_path(p: Path) -> str:
                if backend == "mlx" and p.is_file():
                    return str(p.parent)
                return str(p)

            # 1. Direct containment match (e.g. "mlx-community/hy-mt2-1.8b-8bit")
            if target in path_str:
                return get_return_path(m.path)

            # 2. Hugging Face snapshot path style (replaces / with --)
            hf_target = target.replace("/", "--")
            if hf_target in path_str:
                return get_return_path(m.path)

            # 3. Match suffix parts if multiple parts present
            if len(target_parts) >= 2:
                subtarget = "/".join(target_parts[-2:])
                if subtarget in path_str:
                    return get_return_path(m.path)
                hf_subtarget = "--".join(target_parts[-2:])
                if hf_subtarget in path_str:
                    return get_return_path(m.path)

            # 4. Match by exact model name
            if target_parts and target_parts[-1] == m.name.lower():
                return get_return_path(m.path)
    except Exception:
        pass
    return None


def _gguf_filename(repo: str, default: str | None, quant: str | None) -> str:
    """Pick the GGUF file for ``repo``: an explicit quant wins over the default."""
    if quant:
        try:
            from huggingface_hub import list_repo_files

            for name in list_repo_files(repo):
                if name.endswith(".gguf") and quant.lower() in name.lower():
                    return name
        except Exception as exc:
            raise EngineError(f"Could not list GGUF files of {repo} to find '{quant}'") from exc
        raise EngineError(f"No GGUF file matching '{quant}' in {repo}")
    if default:
        return default
    raise EngineError(f"No GGUF filename mapped for repo {repo}; use '{repo}:<QUANT>'.")


def _download(repo: str, backend: str, filename: str | None, quant: str | None) -> str:
    if backend == "mlx":
        try:
            from huggingface_hub import snapshot_download

            return snapshot_download(repo_id=repo)
        except Exception as exc:
            raise EngineError(f"Failed to download MLX model {repo} from Hugging Face") from exc
    target = _gguf_filename(repo, filename, quant)
    try:
        from huggingface_hub import hf_hub_download

        return hf_hub_download(repo_id=repo, filename=target)
    except Exception as exc:
        raise EngineError(
            f"Failed to download GGUF model {repo}/{target} from Hugging Face"
        ) from exc


def resolve_and_download_model(model_name_or_path: str | None, backend: str) -> str:
    """Resolve a path, alias, ``repo[:QUANT]`` or local model name to a real path.

    Order: existing path -> alias -> local discovery -> Hugging Face download."""
    if not model_name_or_path:
        model_name_or_path = default_model_for(backend)

    normalized = str(model_name_or_path).replace("\\", "/")
    if any(marker in normalized for marker in _LEGACY_HYMT1_MARKERS):
        raise EngineError("Hy-MT1.x models are no longer supported. Please upgrade to Hy-MT2.")

    # 1. Direct path that exists
    p = Path(model_name_or_path)
    if p.exists():
        return str(p.resolve())

    # 2. Optional ``:QUANT`` suffix (GGUF only), then aliases
    quant: str | None = None
    key = normalized
    if backend == "gguf" and ":" in key and not Path(key.partition(":")[0]).exists():
        key, _, quant = key.partition(":")
    key = ALIASES.get(key.lower(), key)

    # 3. Try to discover model locally on disk
    local_path = find_local_model_path(key, backend)
    if local_path and not quant:
        return local_path

    # 4. Known repo, or any other ``owner/name`` repo id -> Hugging Face
    info = KNOWN_MAPPING.get(key)
    if info:
        if info["type"] != backend:
            other = "ml" if info["type"] == "mlx" else "gg"
            raise EngineError(f"{key} is a {info['type']} checkpoint; use the {other} engine")
        return _download(info["repo"], backend, info.get("filename"), quant)
    if "/" in key:
        return _download(key, backend, None, quant)

    raise EngineError(f"Model path/identifier not found: {model_name_or_path}")


def family_for_model(model_name_or_path: str | None) -> str | None:
    """Guess the prompt family (``mthy``/``gemma``) from a model id, alias or path."""
    if not model_name_or_path:
        return None
    key = ALIASES.get(model_name_or_path.lower(), model_name_or_path)
    info = KNOWN_MAPPING.get(key)
    if info:
        return info["family"]
    flat = key.lower().replace("_", "-")
    if "hy-mt2" in flat or "hymt2" in flat:
        return "mthy"
    if "madlad" in flat:
        return "madlad"
    if "salamandra" in flat:
        return "salamandra"
    if "translategemma" in flat:
        return "gemma"
    return None


__all__ = [
    "ALIASES",
    "KNOWN_MAPPING",
    "default_model_for",
    "family_for_model",
    "find_local_model_path",
    "resolve_and_download_model",
]
