# this_file: src/abersetz/providers/llm/inference.py
from __future__ import annotations

import json
import re
from collections.abc import Mapping
from typing import Any

from tenacity import Retrying, stop_after_attempt, wait_exponential

from ...config import EngineConfig
from ...retrieval import reference_context
from ...selector import family_for_subvariant
from ..base import EngineBase, EngineError, EngineRequest, EngineResult
from ..hymt2 import build_hymt2_prompt, hymt2_messages, hymt2_sampling, is_hymt2_model
from ..salamandra import (
    SALAMANDRA_MAX_TOKENS,
    build_salamandra_prompt,
    is_salamandra_model,
)
from ..translategemma import (
    clean_translategemma_output,
    is_translategemma_model,
    render_translategemma_prompt,
)

#: Prompt families the engine can speak. ``generic`` is the XML protocol below;
#: ``mthy`` and ``gemma`` send the model's native instruction and take the raw reply.
PROMPT_FAMILIES = ("generic", "mthy", "gemma", "salamandra")

#: Engine-level attempts per chunk when the caller does not choose.
DEFAULT_MAX_ATTEMPTS = 3


def llm_prompt_family(model: str | None, subvariant: str | None = None) -> str:
    """Pick the prompt family: explicit ``ll/hy-mt2::…`` subvariant, else sniff the model id."""
    forced = family_for_subvariant(subvariant)
    if forced == "madlad":
        raise EngineError("MADLAD-400 has no hosted chat API; use gg::madlad-10b")
    if forced in PROMPT_FAMILIES:
        return forced
    if is_hymt2_model(model):
        return "mthy"
    if is_translategemma_model(model):
        return "gemma"
    if is_salamandra_model(model):
        return "salamandra"
    return "generic"


class LlmEngine(EngineBase):
    """Engine adapter for any OpenAI-compatible LLM endpoint.

    Sends each chunk wrapped in XML tags so the model can respond with a
    structured ``<output>…</output>`` block that is easy to extract even when
    the model adds surrounding commentary.

    **Cost**: Depends entirely on the chosen provider and model.  Indicative
      prices (mid-2025):
      * OpenAI ``gpt-4o-mini``:    ~$0.15 / 1M input tokens, ~$0.60 / 1M output.
      * SiliconFlow ``Qwen2.5-7B``: ~$0.05 / 1M tokens total.
      * Anthropic ``claude-haiku``: ~$0.80 / 1M input, ~$4 / 1M output.
      * Gemini ``gemini-2.0-flash``: generous free tier, then ~$0.10 / 1M.
    **Rate limits**: Provider-specific.  Abersetz makes up to ``max_attempts``
      (default 3) attempts with exponential back-off (1 s, 2 s, 4 s …) before
      re-raising. ``max_attempts=1`` makes exactly one engine-level call; callers
      that own their retry policy use it. The built-in HTTP client
      (:mod:`abersetz.openai_lite`) separately retries 429/5xx/transport errors;
      inject your own client to control that layer too.
    **Privacy**: Text is sent to the remote API endpoint.
    **Offline**: No — requires internet access.
    **Credential**: Set via the matching env var (``OPENAI_API_KEY``,
      ``SILICONFLOW_API_KEY``, ``ANTHROPIC_API_KEY``, ``GEMINI_API_KEY``,
      ``TENCENTCLOUD_API_KEY``, …) or configure in ``[credentials]`` in
      ``abersetz.toml``.

    **Dedicated translation models**: when the model id is a Hy-MT2 checkpoint
    (``ll::openrouter:tencent/hy-mt2-7b``, ``ll::tencent:hy-mt2-pro``) the engine
    switches to Tencent's official instruction, no system prompt, and the
    recommended ``temperature``/``top_p``; TranslateGemma ids get Google's
    rendered chat-template text with greedy decoding. Both return the reply as-is
    instead of parsing ``<output>`` tags.
    """

    OUTPUT_RE = re.compile(r"<output>(?P<body>.*?)</output>", re.DOTALL | re.IGNORECASE)
    VOCAB_RE = re.compile(r"<voc>(?P<body>.*?)</voc>", re.DOTALL | re.IGNORECASE)

    def __init__(
        self,
        config: EngineConfig,
        client: Any,
        *,
        model: str,
        temperature: float,
        static_prolog: Mapping[str, str] | None = None,
        prompt_family: str = "generic",
        max_attempts: int = DEFAULT_MAX_ATTEMPTS,
    ) -> None:
        super().__init__(config.name, config.chunk_size, config.html_chunk_size)
        self.max_attempts = max_attempts
        self._client = client
        self._model = model
        self._temperature = temperature
        self._static_prolog = dict(static_prolog or {})
        if prompt_family not in PROMPT_FAMILIES:
            raise ValueError(f"Unknown prompt family '{prompt_family}'")
        self._prompt_family = prompt_family
        self._sampling = hymt2_sampling(model)

    @property
    def supports_translation_examples(self) -> bool:
        """TranslateGemma / SalamandraTA prompts have no slot for reference pairs."""
        return self._prompt_family not in {"gemma", "salamandra"}

    def _request_kwargs(self) -> dict[str, Any]:
        """Extra chat-completion parameters for dedicated translation models."""
        if self._prompt_family == "mthy":
            return {"top_p": self._sampling.top_p, "max_tokens": self._sampling.max_tokens}
        if self._prompt_family == "salamandra":
            return {"max_tokens": SALAMANDRA_MAX_TOKENS}
        return {}

    @property
    def max_attempts(self) -> int:
        """Engine-level attempts per chunk, including the first; always ``>= 1``."""
        return self._max_attempts

    @max_attempts.setter
    def max_attempts(self, value: int) -> None:
        if type(value) is not int or value < 1:
            raise ValueError(f"max_attempts must be an integer >= 1, got {value!r}")
        self._max_attempts = value

    def _invoke(self, messages: list[dict[str, str]]) -> str:
        """Call the model, retrying up to ``max_attempts`` times with exponential back-off."""
        retrying = Retrying(
            stop=stop_after_attempt(self._max_attempts),
            wait=wait_exponential(multiplier=1),
            reraise=True,
        )
        return retrying(self._invoke_once, messages)

    def _invoke_once(self, messages: list[dict[str, str]]) -> str:
        """One chat-completion request, no retries."""
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=self._temperature,
            **self._request_kwargs(),
        )
        return response.choices[0].message.content or ""

    def translate(self, request: EngineRequest) -> EngineResult:
        if self._prompt_family == "mthy":
            prompt = build_hymt2_prompt(
                request.text,
                request.target_lang,
                voc=request.voc,
                preamble=reference_context(request),
            )
            return EngineResult(
                text=self._invoke(hymt2_messages(prompt)).strip(), voc=dict(request.voc)
            )
        if self._prompt_family == "gemma":
            prompt = render_translategemma_prompt(
                request.source_lang, request.target_lang, request.text
            )
            raw = self._invoke([{"role": "user", "content": prompt}])
            return EngineResult(text=clean_translategemma_output(raw), voc=dict(request.voc))
        if self._prompt_family == "salamandra":
            prompt = build_salamandra_prompt(
                request.text,
                request.source_lang,
                request.target_lang,
                voc=request.voc,
                preserve_markup=request.is_html,
            )
            raw = self._invoke([{"role": "user", "content": prompt}])
            return EngineResult(text=raw.strip(), voc=dict(request.voc))
        voc = dict(self._static_prolog)
        voc.update(request.prolog)
        merged = dict(request.voc)
        messages = self._build_messages(request, voc, merged)
        raw = self._invoke(messages)
        text, new_vocab = self._parse_payload(raw)
        merged.update(new_vocab)
        return EngineResult(text=text, voc=merged)

    def _build_messages(
        self,
        request: EngineRequest,
        voc: Mapping[str, str],
        merged: Mapping[str, str],
    ) -> list[dict[str, str]]:
        """Build the chat-completion message list for a single chunk.

        The prompt is structured with XML tags for three reasons:
        1. **Reliable extraction** — ``<output>…</output>`` lets ``_parse_payload``
           extract translated text with a simple regex even when the model adds
           explanatory commentary around its answer.
        2. **Vocabulary continuity** — ``<prolog>`` carries the running vocabulary
           dictionary forward across chunks so the model honours consistent term
           choices made in earlier chunks.  ``<voc>`` in the response lets the
           model propose new terminology entries that get merged into the next
           chunk's prolog.
        3. **Context for streaming multi-chunk docs** — ``<meta>`` tells the model
           which chunk of how many it is seeing, and whether the content is HTML,
           which helps it avoid escaping or restructuring markup unnecessarily.

        The system prompt requests "deterministic translations strictly in XML tags"
        to suppress the model from adding greetings, disclaimers, or surrounding
        prose — chatty models raise ``_parse_payload`` to fall back to raw output,
        but clean XML is faster and more accurate.
        """
        vocab_payload: dict[str, str] = dict(voc)
        if merged:
            # Inject the accumulated cross-chunk vocabulary so the model can
            # respect earlier terminology choices within the same document.
            vocab_payload.setdefault("__current__", json.dumps(merged, ensure_ascii=False))
        prolog = json.dumps(vocab_payload, ensure_ascii=False) if vocab_payload else "{}"
        meta = {
            "chunk": request.chunk_index + 1,  # 1-based for human readability
            "total": request.total_chunks,
            "is_html": str(request.is_html).lower(),
        }
        # The instruction is kept short and inside the user message (not in the
        # system prompt) so it stays visible even with very long prolog payloads
        # that could otherwise push system-prompt content out of the context window.
        instructions = (
            "Translate the <segment> into the target language. Respond with "
            '<output>...</output> and optionally <voc>{"new": "value"}</voc>.'
        )
        user_content = (
            reference_context(request) + f"<instructions>{instructions}</instructions>\n"
            f"<meta>{json.dumps(meta, ensure_ascii=False)}</meta>\n"
            f"<prolog>{prolog}</prolog>\n"
            f"<target>{request.target_lang}</target>\n"
            f"<source>{request.source_lang}</source>\n"
            f"<segment>{request.text}</segment>"
        )
        return [
            {
                "role": "system",
                # Short system prompt: keeps token usage low and avoids the
                # "helpful assistant" persona that tends to add extra commentary.
                "content": "You produce deterministic translations strictly in XML tags.",
            },
            {"role": "user", "content": user_content},
        ]

    def _parse_payload(self, payload: str) -> tuple[str, dict[str, str]]:
        text_match = self.OUTPUT_RE.search(payload)
        text = text_match.group("body").strip() if text_match else payload.strip()
        vocab_match = self.VOCAB_RE.search(payload)
        if not vocab_match:
            return text, {}
        try:
            vocab = json.loads(vocab_match.group("body"))
        except json.JSONDecodeError:
            vocab = {}
        if isinstance(vocab, dict):
            return text, {str(k): str(v) for k, v in vocab.items()}
        return text, {}


# Compatibility for vexy-localizzy <= the abersetz 1.0.28 pin, which bypassed the
# former Tenacity decorator via ``LlmEngine._invoke.__wrapped__``. Use
# ``LlmEngine(..., max_attempts=1)`` instead; this alias goes away in 2.0.
LlmEngine._invoke.__wrapped__ = LlmEngine._invoke_once  # type: ignore[attr-defined]
