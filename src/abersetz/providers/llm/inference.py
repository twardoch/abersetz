# this_file: src/abersetz/providers/llm/inference.py
from __future__ import annotations

import json
import re
from collections.abc import Mapping
from typing import Any

from tenacity import retry, stop_after_attempt, wait_exponential

from ...config import EngineConfig
from ..base import EngineBase, EngineRequest, EngineResult


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
    **Rate limits**: Provider-specific.  Abersetz retries up to 3 times with
      exponential back-off (1 s, 2 s, 4 s …) before re-raising.
    **Privacy**: Text is sent to the remote API endpoint.
    **Offline**: No — requires internet access.
    **Credential**: Set via the matching env var (``OPENAI_API_KEY``,
      ``SILICONFLOW_API_KEY``, ``ANTHROPIC_API_KEY``, ``GEMINI_API_KEY``, …)
      or configure in ``[credentials]`` in ``abersetz.toml``.
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
    ) -> None:
        super().__init__(config.name, config.chunk_size, config.html_chunk_size)
        self._client = client
        self._model = model
        self._temperature = temperature
        self._static_prolog = dict(static_prolog or {})

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1), reraise=True)
    def _invoke(self, messages: list[dict[str, str]]) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=self._temperature,
        )
        return response.choices[0].message.content or ""

    def translate(self, request: EngineRequest) -> EngineResult:
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
            "chunk": request.chunk_index + 1,   # 1-based for human readability
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
            f"<instructions>{instructions}</instructions>\n"
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
