# this_file: src/abersetz/providers/mlx.py

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..config import EngineConfig
from ..retrieval import reference_context
from .base import EngineBase, EngineError, EngineRequest, EngineResult
from .hymt2 import build_hymt2_prompt, hymt2_messages, hymt2_sampling
from .local_models import resolve_and_download_model
from .salamandra import SALAMANDRA_MAX_TOKENS, build_salamandra_prompt
from .translategemma import (
    TRANSLATEGEMMA_MAX_TOKENS,
    clean_translategemma_output,
    translategemma_messages,
)


class LocalMlxEngine(EngineBase):
    """Local translation engine using the ``mlx_lm`` framework (Apple Silicon only).

    Loads a model from disk (or downloads it from Hugging Face on first use) and
    runs inference entirely on the local Apple Silicon GPU via the MLX framework.

    Supported model families:
    * **mthy** — Tencent Hy-MT2 series (1.8B / 7B / 30B-A3B). Prompted with the
      official English instruction and decoded with Tencent's recommended
      sampler (``temperature=0.7, top_p=0.6, top_k=20, repetition_penalty=1.05``
      for the dense sizes). Use ``ml/hy-mt2::<alias|repo|path>``.
    * **gemma** — Google TranslateGemma (4B / 12B / 27B). Uses the model's own
      chat template with ``source_lang_code``/``target_lang_code`` and greedy
      decoding. Use ``ml/gemma::<alias|repo|path>``.
    * **salamandra** — BSC-LT SalamandraTA-7b-instruct converted to MLX; the
      model-card prompts through the ChatML template.
    MADLAD-400 (T5) has no mlx_lm port; use ``gg::madlad-10b``.

    **Cost**: Free — inference runs locally; you pay only hardware and electricity.
    **Rate limits**: None.  Throughput is bounded by GPU memory bandwidth
      (typically 50–300 tokens/second on M-series chips).
    **Privacy**: 100 % local — no data leaves the machine.
    **Offline**: Yes — after the model is downloaded once.
    **Platform**: macOS with Apple Silicon (M1 or later) only.
      Install with ``pip install abersetz[mlx]``.
    **Model download**: First-time use triggers a Hugging Face download (several GB).
      Subsequent runs use the cached snapshot.
    """

    def __init__(
        self,
        family: str,
        config: EngineConfig,
        model_path: str,
        *,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> None:
        super().__init__(config.name, config.chunk_size, config.html_chunk_size)
        if family == "madlad":
            raise EngineError(
                "MADLAD-400 is a T5 encoder-decoder model without an mlx_lm port; "
                "use the GGUF engine: gg::madlad-10b"
            )
        self._family = family
        self._temperature = temperature

        resolved_path = resolve_and_download_model(model_path, "mlx")
        # A Hugging Face snapshot resolves to ``…/snapshots/<sha>``; keep the
        # user's alias/repo as the display name and look at both for sizing.
        self._cache_model_path = resolved_path
        self._model_name = Path(str(model_path).rstrip("/")).name or Path(resolved_path).name
        self._sampling = hymt2_sampling(f"{model_path} {resolved_path}")
        if max_tokens is not None:
            self._max_tokens = max_tokens
        elif family == "mthy":
            self._max_tokens = self._sampling.max_tokens
        elif family == "salamandra":
            self._max_tokens = SALAMANDRA_MAX_TOKENS
        else:
            self._max_tokens = TRANSLATEGEMMA_MAX_TOKENS
        try:
            from mlx_lm import generate, load
        except Exception as exc:  # pragma: no cover
            raise EngineError("mlx-lm is required for MLX engines") from exc
        self._generate = generate
        self._model, self._tokenizer = load(resolved_path)

    @property
    def supports_translation_examples(self) -> bool:
        return self._family == "mthy"

    def _sampler_kwargs(self) -> dict[str, Any]:
        """Extra ``mlx_lm.generate`` kwargs implementing the family's decoding recipe.

        Returns an empty dict (greedy decoding) when ``mlx_lm.sample_utils`` is
        unavailable or when the family wants greedy output anyway."""
        try:
            from mlx_lm.sample_utils import make_logits_processors, make_sampler
        except Exception:
            from loguru import logger

            logger.debug("mlx_lm.sample_utils unavailable; decoding with mlx_lm defaults")
            return {}
        if self._family != "mthy":
            if self._temperature is None:
                return {}
            return {"sampler": make_sampler(temp=self._temperature)}
        s = self._sampling
        temp = self._temperature if self._temperature is not None else s.temperature
        sampler_args: dict[str, Any] = {"temp": temp, "top_p": s.top_p}
        if s.top_k > 0:
            sampler_args["top_k"] = s.top_k
        kwargs: dict[str, Any] = {"sampler": make_sampler(**sampler_args)}
        if s.repetition_penalty != 1.0:
            kwargs["logits_processors"] = make_logits_processors(
                repetition_penalty=s.repetition_penalty
            )
        return kwargs

    def _apply_template(self, messages: list[dict[str, Any]]) -> str | None:
        if not (
            hasattr(self._tokenizer, "apply_chat_template")
            and getattr(self._tokenizer, "chat_template", None)
        ):
            return None
        return self._tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )

    def translate(self, request: EngineRequest) -> EngineResult:
        if self._family == "mthy":
            prompt = build_hymt2_prompt(
                request.text,
                request.target_lang,
                voc=request.voc,
                preamble=reference_context(request),
            )
            templated = self._apply_template(hymt2_messages(prompt))
            text = self._generate(
                self._model,
                self._tokenizer,
                prompt=templated if templated is not None else prompt,
                max_tokens=self._max_tokens,
                verbose=False,
                **self._sampler_kwargs(),
            )
            return EngineResult(text=text.strip(), voc=dict(request.voc))
        if self._family == "gemma":
            messages = translategemma_messages(
                request.source_lang, request.target_lang, request.text
            )
            templated = self._apply_template(messages)
            if templated is None:
                raise EngineError("TranslateGemma MLX tokenizer missing chat template support")
            text = self._generate(
                self._model,
                self._tokenizer,
                prompt=templated,
                max_tokens=self._max_tokens,
                verbose=False,
                **self._sampler_kwargs(),
            )
            return EngineResult(text=clean_translategemma_output(text), voc=dict(request.voc))
        if self._family == "salamandra":
            prompt = build_salamandra_prompt(
                request.text,
                request.source_lang,
                request.target_lang,
                voc=request.voc,
                preserve_markup=request.is_html,
            )
            templated = self._apply_template([{"role": "user", "content": prompt}])
            text = self._generate(
                self._model,
                self._tokenizer,
                prompt=templated if templated is not None else prompt,
                max_tokens=self._max_tokens,
                verbose=False,
                **self._sampler_kwargs(),
            )
            return EngineResult(text=text.split("<|im_end|>")[0].strip(), voc=dict(request.voc))
        raise EngineError(f"Unsupported MLX family '{self._family}'")
