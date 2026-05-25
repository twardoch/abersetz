# this_file: src/abersetz/providers/lmstudio.py

from __future__ import annotations

from tenacity import retry, stop_after_attempt, wait_exponential

from ..config import EngineConfig
from .base import EngineBase, EngineError, EngineRequest, EngineResult


class LmstudioEngine(EngineBase):
    """Local inference engine using the official lmstudio SDK."""

    def __init__(self, config: EngineConfig, *, temperature: float | None = None) -> None:
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
        self._model = lms.llm(model_name)
        self._temperature = temperature if temperature is not None else options.get("temperature")
        if self._temperature is not None:
            self._temperature = float(self._temperature)

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

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1), reraise=True)
    def _invoke(self, prompt: str) -> str:
        config = {}
        if self._temperature is not None:
            config["temperature"] = self._temperature
        return str(self._model.respond(prompt, config=config))

    def translate(self, request: EngineRequest) -> EngineResult:
        language_name = self._language_name(request.target_lang)
        prompt = (
            f"Translate the following segment into {language_name}, without additional explanation.\n\n"
            f"{request.text}"
        )
        text = self._invoke(prompt).strip()
        return EngineResult(text=text, voc=dict(request.voc))

    @staticmethod
    def _language_name(code: str) -> str:
        try:
            from langcodes import get as get_language

            return get_language(code).language_name("en") or code
        except Exception:
            return code
