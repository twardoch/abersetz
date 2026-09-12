# this_file: src/abersetz/providers/lmstudio.py

from __future__ import annotations

from typing import Any

from tenacity import retry, stop_after_attempt, wait_exponential

from ..config import EngineConfig
from ..retrieval import reference_context
from ..selector import family_for_subvariant
from .base import EngineBase, EngineError, EngineRequest, EngineResult
from .hymt2 import build_hymt2_prompt, hymt2_sampling, is_hymt2_model
from .madlad import is_madlad_model
from .salamandra import (
    SALAMANDRA_MAX_TOKENS,
    SALAMANDRA_TEMPERATURE,
    build_salamandra_prompt,
    is_salamandra_model,
)
from .translategemma import (
    TRANSLATEGEMMA_TEMPERATURE,
    clean_translategemma_output,
    is_translategemma_model,
    render_translategemma_prompt,
)


def lmstudio_family(model_name: str | None, subvariant: str | None = None) -> str:
    """Prompt family for an LM Studio model: ``mthy``, ``gemma`` or ``generic``.

    An explicit selector subvariant (``lm/hy-mt2::…``) wins; otherwise the model
    id is sniffed so ``lm::hy-mt2-7b`` and ``lm::translategemma-4b-it`` just work."""
    forced = family_for_subvariant(subvariant)
    if forced is not None:
        return forced if forced in {"mthy", "gemma", "salamandra", "madlad"} else "generic"
    if is_hymt2_model(model_name):
        return "mthy"
    if is_translategemma_model(model_name):
        return "gemma"
    if is_salamandra_model(model_name):
        return "salamandra"
    if is_madlad_model(model_name):
        return "madlad"
    return "generic"


class LmstudioEngine(EngineBase):
    """Local inference engine using the official LMStudio Python SDK.

    Connects to a running LMStudio instance (default: ``localhost:1234``) via the
    official ``lmstudio`` SDK.  If the LMStudio daemon is not running and the
    ``lms`` CLI tool is on PATH, abersetz will attempt to start it automatically.

    Model-specific prompting: when the loaded model is a Hy-MT2 checkpoint the
    engine sends Tencent's official instruction with the recommended sampler
    settings; when it is TranslateGemma it renders Google's chat-template text
    and decodes greedily. Anything else gets a plain translation instruction.

    **Cost**: Free — inference runs locally; you pay only hardware and electricity.
    **Rate limits**: None.  Throughput is bounded by your GPU/CPU speed.
    **Privacy**: 100 % local — no data leaves the machine.
    **Offline**: Yes — after the model is loaded in LMStudio.
    **Prerequisite**: LMStudio must be installed and a model must be loaded.
      Install the ``lmstudio`` SDK extra: ``pip install abersetz[lms]``.
    **Selector**: ``lm::<model-id-or-alias>``, ``lm/hy-mt2::<model-id>``,
      ``lm/gemma::<model-id>``, or ``lm`` for the currently loaded model.
    """

    def __init__(
        self,
        config: EngineConfig,
        *,
        temperature: float | None = None,
        family: str | None = None,
    ) -> None:
        super().__init__(config.name, config.chunk_size, config.html_chunk_size)
        try:
            import lmstudio as lms  # type: ignore[import-untyped]
        except ImportError as err:
            raise EngineError(
                "lmstudio SDK is required for LMStudio engine. Install with: pip install lmstudio"
            ) from err

        options = dict(config.options)
        base_url = options.get("base_url") or "localhost:1234"
        self._ensure_lmstudio_daemon(base_url)
        try:
            lms.configure_default_client(base_url)
        except Exception as err:
            if "already created" not in str(err):
                raise
        model_name = options.get("model") or "local-model"
        self._model_name = model_name
        self._family = family or lmstudio_family(model_name)
        if self._family == "madlad":
            raise EngineError(
                "MADLAD-400 is an encoder-decoder (T5) model that LM Studio's chat API cannot "
                "drive; use the GGUF engine instead: gg::madlad-10b"
            )
        self._model = lms.llm(model_name)
        self._sampling = hymt2_sampling(model_name)
        configured = temperature if temperature is not None else options.get("temperature")
        self._temperature = float(configured) if configured is not None else None

    @property
    def supports_translation_examples(self) -> bool:
        """TranslateGemma / SalamandraTA prompts have no slot for reference pairs."""
        return self._family not in {"gemma", "salamandra"}

    def _ensure_lmstudio_daemon(self, base_url: str | None) -> None:
        import json
        import shutil
        import subprocess
        from pathlib import Path

        from loguru import logger

        if base_url:
            host = base_url.split(":")[0] if ":" in base_url else base_url
            if host not in ("localhost", "127.0.0.1", "othello.local"):
                return

        lms_path = shutil.which("lms")
        if not lms_path:
            home_lms = Path.home() / ".lmstudio" / "bin" / "lms"
            if home_lms.exists():
                lms_path = str(home_lms)

        if not lms_path:
            logger.debug("lms CLI tool not found in PATH or ~/.lmstudio/bin/lms")
            return

        try:
            res = subprocess.run(
                [lms_path, "server", "status", "--json"],
                capture_output=True,
                text=True,
                check=False,
                timeout=5.0,
            )
            if res.returncode == 0:
                status = json.loads(res.stdout.strip())
                if status.get("running"):
                    logger.debug("LM Studio server is already running.")
                    return
        except Exception as e:
            logger.debug(f"Failed to check LM Studio status: {e}")

        logger.info("Waking up LM Studio service...")
        try:
            res = subprocess.run(
                [lms_path, "daemon", "up", "--json"],
                capture_output=True,
                text=True,
                check=False,
                timeout=15.0,
            )
            if res.returncode == 0:
                logger.info("LM Studio service started successfully.")
            else:
                logger.warning(f"LM Studio daemon up failed: {res.stderr}")
        except Exception as e:
            logger.warning(f"Failed to start LM Studio daemon: {e}")

    def _prediction_config(self) -> dict[str, Any]:
        """LM Studio prediction config (camelCase keys, as the SDK's dict form expects)."""
        config: dict[str, Any] = {}
        if self._family == "mthy":
            s = self._sampling
            config.update(
                {
                    "temperature": s.temperature,
                    "topPSampling": s.top_p,
                    "repeatPenalty": s.repetition_penalty,
                    "maxTokens": s.max_tokens,
                }
            )
            if s.top_k > 0:
                config["topKSampling"] = s.top_k
        elif self._family == "gemma":
            config["temperature"] = TRANSLATEGEMMA_TEMPERATURE
        elif self._family == "salamandra":
            config.update(
                {"temperature": SALAMANDRA_TEMPERATURE, "maxTokens": SALAMANDRA_MAX_TOKENS}
            )
        if self._temperature is not None:
            config["temperature"] = self._temperature
        return config

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1), reraise=True)
    def _invoke(self, prompt: str) -> str:
        return str(self._model.respond(prompt, config=self._prediction_config()))

    def _build_prompt(self, request: EngineRequest) -> str:
        if self._family == "mthy":
            return build_hymt2_prompt(
                request.text,
                request.target_lang,
                voc=request.voc,
                preamble=reference_context(request),
            )
        if self._family == "gemma":
            return render_translategemma_prompt(
                request.source_lang, request.target_lang, request.text
            )
        if self._family == "salamandra":
            return build_salamandra_prompt(
                request.text,
                request.source_lang,
                request.target_lang,
                voc=request.voc,
                preserve_markup=request.is_html,
            )
        language_name = self._language_name(request.target_lang)
        return (
            reference_context(request)
            + f"Translate the following segment into {language_name}, without additional explanation.\n\n"
            f"{request.text}"
        )

    def translate(self, request: EngineRequest) -> EngineResult:
        text = self._invoke(self._build_prompt(request)).strip()
        if self._family == "gemma":
            text = clean_translategemma_output(text)
        return EngineResult(text=text, voc=dict(request.voc))

    @staticmethod
    def _language_name(code: str) -> str:
        try:
            from langcodes import get as get_language

            return get_language(code).language_name("en") or code
        except Exception:
            return code
