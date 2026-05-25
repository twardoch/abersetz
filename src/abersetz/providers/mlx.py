# this_file: src/abersetz/providers/mlx.py

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..config import EngineConfig
from .base import EngineBase, EngineError, EngineRequest, EngineResult

MTHY_LANGUAGE_DATA = """
Chinese	zh	中文
English	en	英语
French	fr	法语
Portuguese	pt	葡萄牙语
Spanish	es	西班牙语
Japanese	ja	日语
Turkish	tr	土耳其语
Russian	ru	俄语
Arabic	ar	阿拉伯语
Korean	ko	韩语
Thai	th	泰语
Italian	it	意大利语
German	de	德语
Vietnamese	vi	越南语
Malay	ms	马来语
Indonesian	id	印尼语
Filipino	tl	菲律宾语
Hindi	hi	印地语
Traditional Chinese	zh-Hant	繁体中文
Polish	pl	波兰语
Czech	cs	捷克语
Dutch	nl	荷兰语
Khmer	km	高棉语
Burmese	my	缅甸语
Persian	fa	波斯语
Gujarati	gu	古吉拉特语
Urdu	ur	乌尔都语
Telugu	te	泰卢固语
Marathi	mr	马拉地语
Hebrew	he	希伯来语
Bengali	bn	孟加拉语
Tamil	ta	泰米尔语
Ukrainian	uk	乌克兰语
Tibetan	bo	藏语
Kazakh	kk	哈萨克语
Mongolian	mn	蒙古语
Uyghur	ug	维吾尔语
Cantonese	yue	粤语
"""

MTHY_LANG_MAP: dict[str, str] = {}
for line in MTHY_LANGUAGE_DATA.strip().splitlines():
    english, code, chinese = line.split("\t")
    MTHY_LANG_MAP[english.lower()] = chinese
    MTHY_LANG_MAP[code.lower()] = chinese
    MTHY_LANG_MAP[chinese] = chinese


def _resolve_mthy_language(code: str) -> str:
    """Resolve HY-MT language code/name to Chinese label."""
    resolved = MTHY_LANG_MAP.get(code.lower())
    if resolved is None:
        raise EngineError(f"Unsupported HY-MT language: {code}")
    return resolved


def build_mthy_prompt(
    source_text: str, target_language: str, voc: dict[str, str] | None = None
) -> str:
    """Build prompting format for Hy-MT2 with optional terminology intervention."""
    terms_part = ""
    if voc:
        terms = "".join(f"{src}翻译成{tgt}" for src, tgt in sorted(voc.items()))
        terms_part = f"参考下面的翻译：{terms}"
    return f"{terms_part}将以下文本翻译为{target_language}，注意只需要输出翻译后的结果，不要额外解释：{source_text}"


# Known models and their details
KNOWN_MAPPING = {
    # MLX
    "QwQbb/Hy-MT2-30B-A3B-MLX-4bit": {
        "repo": "QwQbb/Hy-MT2-30B-A3B-MLX-4bit",
        "lmstudio_path": "/Volumes/Falstaff4T/RomeoData2/lmstudio/models/QwQbb/Hy-MT2-30B-A3B-MLX-4bit",
        "type": "mlx",
    },
    "p0we7/Hy-MT2-1.8B-oQ8-fp16": {
        "repo": "p0we7/Hy-MT2-1.8B-oQ8-fp16",
        "lmstudio_path": "/Volumes/Falstaff4T/RomeoData2/lmstudio/models/p0we7/Hy-MT2-1.8B-oQ8-fp16",
        "type": "mlx",
    },
    "tevino/Hy-MT2-7B-oQ8": {
        "repo": "tevino/Hy-MT2-7B-oQ8",
        "lmstudio_path": "/Volumes/Falstaff4T/RomeoData2/lmstudio/models/tevino/Hy-MT2-7B-oQ8",
        "type": "mlx",
    },
    "sahilchachra/hy-mt2-7b-8bit-mlx": {
        "repo": "sahilchachra/hy-mt2-7b-8bit-mlx",
        "lmstudio_path": "/Volumes/Falstaff4T/RomeoData2/lmstudio/models/sahilchachra/hy-mt2-7b-8bit-mlx",
        "type": "mlx",
    },
    # GGUF
    "tencent/Hy-MT2-7B-GGUF": {
        "repo": "tencent/Hy-MT2-7B-GGUF",
        "filename": "HY-MT2-7B-Q8_0.gguf",
        "lmstudio_path": "/Volumes/Falstaff4T/RomeoData2/lmstudio/models/tencent/Hy-MT2-7B-GGUF/HY-MT2-7B-Q8_0.gguf",
        "type": "gguf",
    },
    "mradermacher/Hy-MT2-1.8B-heretic-GGUF": {
        "repo": "mradermacher/Hy-MT2-1.8B-heretic-GGUF",
        "filename": "Hy-MT2-1.8B-heretic.Q8_0.gguf",
        "lmstudio_path": "/Volumes/Falstaff4T/RomeoData2/lmstudio/models/mradermacher/Hy-MT2-1.8B-heretic-GGUF/Hy-MT2-1.8B-heretic.Q8_0.gguf",
        "type": "gguf",
    },
    "tencent/Hy-MT2-1.8B-GGUF": {
        "repo": "tencent/Hy-MT2-1.8B-GGUF",
        "filename": "Hy-MT2-1.8B-Q8_0.gguf",
        "lmstudio_path": "/Volumes/Falstaff4T/RomeoData2/lmstudio/models/tencent/Hy-MT2-1.8B-GGUF/Hy-MT2-1.8B-Q8_0.gguf",
        "type": "gguf",
    },
    "tencent/Hy-MT2-1.8B-2Bit-GGUF": {
        "repo": "tencent/Hy-MT2-1.8B-2Bit-GGUF",
        "filename": "Hy-MT2-1.8B-2Bit.gguf",
        "lmstudio_path": "/Volumes/Falstaff4T/RomeoData2/lmstudio/models/tencent/Hy-MT2-1.8B-2Bit-GGUF/Hy-MT2-1.8B-2Bit.gguf",
        "type": "gguf",
    },
    "tencent/Hy-MT2-1.8B-1.25Bit-GGUF": {
        "repo": "tencent/Hy-MT2-1.8B-1.25Bit-GGUF",
        "filename": "Hy-MT2-1.8B-1.25Bit.gguf",
        "lmstudio_path": "/Volumes/Falstaff4T/RomeoData2/lmstudio/models/tencent/Hy-MT2-1.8B-1.25Bit-GGUF/Hy-MT2-1.8B-1.25Bit.gguf",
        "type": "gguf",
    },
}

ALIASES = {
    # MLX
    "30b-mlx": "QwQbb/Hy-MT2-30B-A3B-MLX-4bit",
    "1.8b-mlx": "p0we7/Hy-MT2-1.8B-oQ8-fp16",
    "7b-mlx": "tevino/Hy-MT2-7B-oQ8",
    "7b-8bit-mlx": "sahilchachra/hy-mt2-7b-8bit-mlx",
    # GGUF
    "7b-gguf": "tencent/Hy-MT2-7B-GGUF",
    "1.8b-heretic": "mradermacher/Hy-MT2-1.8B-heretic-GGUF",
    "1.8b-gguf": "tencent/Hy-MT2-1.8B-GGUF",
    "1.8b-2bit": "tencent/Hy-MT2-1.8B-2Bit-GGUF",
    "1.8b-1.25bit": "tencent/Hy-MT2-1.8B-1.25Bit-GGUF",
}


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

            # 1. Direct containment match (e.g. "p0we7/hy-mt2-1.8b-oq8-fp16")
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


def resolve_and_download_model(model_name_or_path: str | None, backend: str) -> str:
    """Resolve local path or LMStudio path, downloading via huggingface_hub if needed."""
    if not model_name_or_path:
        model_name_or_path = (
            "p0we7/Hy-MT2-1.8B-oQ8-fp16" if backend == "mlx" else "tencent/Hy-MT2-1.8B-GGUF"
        )

    normalized_path = str(model_name_or_path).replace("\\", "/")
    if any(
        legacy in normalized_path for legacy in ["Hunyuan-MT-7B", "Hunyuan-MT1", "Hy-MT1", "HY-MT1"]
    ):
        raise EngineError("Hy-MT1.x models are no longer supported. Please upgrade to Hy-MT2.")

    # 1. Direct path that exists
    p = Path(model_name_or_path)
    if p.exists():
        return str(p.resolve())

    # 2. Check aliases
    key = ALIASES.get(model_name_or_path.lower(), model_name_or_path)

    # 3. Try to discover model locally on disk
    local_path = find_local_model_path(key, backend)
    if local_path:
        return local_path

    # 4. Check known mapping fallback (if not found in standard discovery, check specified lmstudio_path)
    info = KNOWN_MAPPING.get(key)
    if info:
        lm_path = Path(info["lmstudio_path"])
        if lm_path.exists():
            return str(lm_path.resolve())

        repo = info["repo"]
        if info["type"] == "mlx":
            try:
                from huggingface_hub import snapshot_download

                return snapshot_download(repo_id=repo)
            except Exception as exc:
                raise EngineError(
                    f"Failed to resolve/download MLX model {repo} from Hugging Face"
                ) from exc
        else:
            filename = info["filename"]
            try:
                from huggingface_hub import hf_hub_download

                return hf_hub_download(repo_id=repo, filename=filename)
            except Exception as exc:
                raise EngineError(
                    f"Failed to resolve/download GGUF model {repo}/{filename} from Hugging Face"
                ) from exc

    # 5. Fallback to direct repo ID download
    if "/" in key:
        if backend == "mlx":
            try:
                from huggingface_hub import snapshot_download

                return snapshot_download(repo_id=key)
            except Exception as exc:
                raise EngineError(f"Failed to download MLX model {key} from Hugging Face") from exc
        else:
            raise EngineError(
                f"Model {model_name_or_path} not found locally, and no GGUF filename mapped for repo {key}."
            )

    raise EngineError(f"Model path/identifier not found: {model_name_or_path}")


class LocalMlxEngine(EngineBase):
    """Local MLX-backed engine for HY-MT and TranslateGemma."""

    def __init__(
        self,
        family: str,
        config: EngineConfig,
        model_path: str,
        *,
        max_tokens: int,
    ) -> None:
        super().__init__(config.name, config.chunk_size, config.html_chunk_size)
        self._family = family
        self._max_tokens = max_tokens

        resolved_path = resolve_and_download_model(model_path, "mlx")
        self._model_name = Path(resolved_path).name
        try:
            from mlx_lm import generate, load
        except Exception as exc:  # pragma: no cover
            raise EngineError("mlx-lm is required for MLX engines") from exc
        self._generate = generate
        self._model, self._tokenizer = load(resolved_path)

    def translate(self, request: EngineRequest) -> EngineResult:
        if self._family == "mthy":
            prompt = build_mthy_prompt(
                source_text=request.text,
                target_language=_resolve_mthy_language(request.target_lang),
                voc=request.voc,
            )
            if hasattr(self._tokenizer, "apply_chat_template") and getattr(
                self._tokenizer, "chat_template", None
            ):
                mthy_messages = [{"role": "user", "content": prompt}]
                prompt = self._tokenizer.apply_chat_template(
                    mthy_messages, tokenize=False, add_generation_prompt=True
                )
            text = self._generate(
                self._model,
                self._tokenizer,
                prompt=prompt,
                max_tokens=self._max_tokens,
                verbose=False,
            )
            return EngineResult(text=text, voc=dict(request.voc))
        if self._family == "gemma":
            source_lang = request.source_lang if request.source_lang != "auto" else "en"
            gemma_messages: list[dict[str, Any]] = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "source_lang_code": source_lang,
                            "target_lang_code": request.target_lang,
                            "text": request.text,
                        }
                    ],
                }
            ]
            if not hasattr(self._tokenizer, "apply_chat_template"):
                raise EngineError("Gemma MLX tokenizer missing chat template support")
            prompt = self._tokenizer.apply_chat_template(
                gemma_messages, tokenize=False, add_generation_prompt=True
            )
            text = self._generate(
                self._model,
                self._tokenizer,
                prompt=prompt,
                max_tokens=self._max_tokens,
                verbose=False,
            )
            return EngineResult(text=text.split("<end_of_turn>")[0].strip(), voc=dict(request.voc))
        raise EngineError(f"Unsupported MLX family '{self._family}'")
