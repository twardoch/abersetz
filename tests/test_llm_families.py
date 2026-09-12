# this_file: tests/test_llm_families.py
"""Hy-MT2 / TranslateGemma prompt families on the OpenAI-compatible ``ll`` engine (offline)."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from abersetz import config as config_module
from abersetz.engines import create_engine
from abersetz.providers.base import EngineRequest
from abersetz.providers.llm.discovery import BUILTIN_ENDPOINTS, endpoint_api_key, resolve_model
from abersetz.providers.llm.inference import llm_prompt_family


class FakeClient:
    """Records chat-completion calls and answers with a fixed string."""

    def __init__(self, reply: str) -> None:
        self.calls: list[dict[str, object]] = []
        completions = SimpleNamespace(create=self._create)
        self.chat = SimpleNamespace(completions=completions)
        self._reply = reply

    def _create(self, **kwargs: object) -> object:
        self.calls.append(kwargs)
        message = SimpleNamespace(content=self._reply)
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])


def _request(text: str = "Hello", *, source: str = "en", target: str = "pl") -> EngineRequest:
    return EngineRequest(
        text=text,
        source_lang=source,
        target_lang=target,
        is_html=False,
        voc={"hello": "cześć"},
        prolog={},
        chunk_index=0,
        total_chunks=1,
    )


# ---------------------------------------------------------------------------
# endpoint registry
# ---------------------------------------------------------------------------


def test_tencent_endpoint_registered() -> None:
    ep = BUILTIN_ENDPOINTS["tencent"]
    assert ep.base_url == "https://tokenhub-intl.tencentcloudmaas.com/v1"
    assert ep.api_key_env == "TENCENTCLOUD_API_KEY"
    assert ep.known_models == ["hy-mt2-pro", "hy-mt2-plus", "hy-mt2-lite"]


def test_openrouter_lists_hymt2_models() -> None:
    known = BUILTIN_ENDPOINTS["openrouter"].known_models
    for model in ("tencent/hy-mt2-1.8b", "tencent/hy-mt2-7b", "tencent/hy-mt2-30b-a3b"):
        assert model in known, f"{model} missing from OpenRouter known models"


def test_resolve_model_when_bare_tencent_then_pro_tier(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TENCENT_API_ENDPOINT", raising=False)
    endpoint, model = resolve_model("tencent")
    assert endpoint.name == "tencent"
    assert model == "hy-mt2-pro"


def test_endpoint_api_key_when_fallback_env_then_used(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TENCENTCLOUD_API_KEY", raising=False)
    monkeypatch.setenv("TENCENT_API_KEY", "fallback-key")
    assert endpoint_api_key(BUILTIN_ENDPOINTS["tencent"]) == "fallback-key"
    monkeypatch.setenv("TENCENTCLOUD_API_KEY", "primary-key")
    assert endpoint_api_key(BUILTIN_ENDPOINTS["tencent"]) == "primary-key"


@pytest.mark.parametrize(
    ("model", "sub", "expected"),
    [
        ("tencent/hy-mt2-7b", None, "mthy"),
        ("hy-mt2-pro", None, "mthy"),
        ("translategemma-4b-it", None, "gemma"),
        ("gpt-4o-mini", None, "generic"),
        ("gpt-4o-mini", "hy-mt2", "mthy"),
        ("gpt-4o-mini", "tg", "gemma"),
    ],
)
def test_llm_prompt_family(model: str, sub: str | None, expected: str) -> None:
    assert llm_prompt_family(model, sub) == expected


# ---------------------------------------------------------------------------
# engine behaviour
# ---------------------------------------------------------------------------


def test_ll_openrouter_hymt2_when_model_id_then_native_prompt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OPENROUTER_API_KEY", "k")
    client = FakeClient("  Cześć świecie ")
    engine = create_engine(
        "ll::openrouter:tencent/hy-mt2-7b", config_module.load_config(), client=client
    )
    result = engine.translate(_request())

    assert result.text == "Cześć świecie", "reply is taken verbatim, no <output> parsing"
    assert result.voc == {"hello": "cześć"}
    call = client.calls[0]
    assert call["model"] == "tencent/hy-mt2-7b"
    assert call["temperature"] == 0.7
    assert call["top_p"] == 0.6
    assert call["max_tokens"] == 4096
    messages = call["messages"]
    assert [m["role"] for m in messages] == ["user"], "Hy-MT2 has no system prompt"
    content = messages[0]["content"]
    assert content.startswith("Reference the following translations:\nhello translates to cześć")
    assert "Translate the following text into Polish." in content
    assert content.endswith("Hello")


def test_ll_tencent_hymt2_when_tokenhub_then_env_fallback_and_moe_defaults(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("TENCENTCLOUD_API_KEY", raising=False)
    monkeypatch.setenv("TENCENT_API_KEY", "k")
    client = FakeClient("ok")
    engine = create_engine("ll::tencent:hy-mt2-pro", config_module.load_config(), client=client)
    engine.translate(_request(target="de"))
    call = client.calls[0]
    assert call["model"] == "hy-mt2-pro"
    assert call["temperature"] == 0.7
    assert call["top_p"] == 0.6


def test_ll_tencent_when_key_missing_then_engine_error(monkeypatch: pytest.MonkeyPatch) -> None:
    from abersetz.providers.base import EngineError

    monkeypatch.delenv("TENCENTCLOUD_API_KEY", raising=False)
    monkeypatch.delenv("TENCENT_API_KEY", raising=False)
    with pytest.raises(EngineError, match="TENCENTCLOUD_API_KEY"):
        create_engine("ll::tencent:hy-mt2-lite", config_module.load_config())


def test_ll_hymt2_when_subvariant_then_family_forced_and_override_temperature(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "k")
    client = FakeClient("ok")
    engine = create_engine(
        "ll/hy-mt2::openai:my-finetune", config_module.load_config(), client=client, temperature=0.1
    )
    engine.translate(_request())
    call = client.calls[0]
    assert call["temperature"] == 0.1
    assert call["top_p"] == 0.6
    assert call["messages"][0]["role"] == "user"


def test_ll_generic_when_ordinary_model_then_xml_protocol(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "k")
    client = FakeClient("<output>done</output>")
    engine = create_engine("ll::openai:gpt-4o-mini", config_module.load_config(), client=client)
    result = engine.translate(_request())
    assert result.text == "done"
    call = client.calls[0]
    assert "top_p" not in call
    assert call["messages"][0]["role"] == "system"


def test_ll_gemma_when_translategemma_then_rendered_template_and_greedy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "k")
    client = FakeClient("Cześć<end_of_turn>")
    engine = create_engine(
        "ll::http://localhost:8080/v1:translategemma-4b-it",
        config_module.load_config(),
        client=client,
    )
    result = engine.translate(_request(source="auto", target="pl"))
    assert result.text == "Cześć"
    call = client.calls[0]
    assert call["temperature"] == 0.0
    assert call["messages"][0]["content"].startswith(
        "You are a professional English (en) to Polish (pl) translator."
    )
