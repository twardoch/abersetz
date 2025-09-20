"""Tests for translation engines."""
# this_file: tests/test_engines.py

from __future__ import annotations

from types import SimpleNamespace

import pytest

import abersetz.config as config_module
from abersetz.engines import EngineRequest, create_engine


class DummyClient:
    """Simple stub mimicking OpenAI chat completions."""

    def __init__(self, payload: str):
        self.payload = payload
        self.calls: list[dict[str, object]] = []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **kwargs: object) -> SimpleNamespace:
        self.calls.append(kwargs)
        message = SimpleNamespace(content=self.payload)
        choice = SimpleNamespace(message=message)
        return SimpleNamespace(choices=[choice])


def test_translators_engine_invokes_library(monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = config_module.load_config()
    engine = create_engine("translators/google", cfg)

    captured: dict[str, object] = {}

    def fake_translate_text(
        text: str, translator: str, from_language: str, to_language: str, **_: object
    ) -> str:
        captured.update(
            {
                "text": text,
                "translator": translator,
                "from_language": from_language,
                "to_language": to_language,
            }
        )
        return "translated"

    monkeypatch.setattr("abersetz.engines.translators.translate_text", fake_translate_text)

    request = EngineRequest(
        text="hello",
        source_lang="en",
        target_lang="pl",
        is_html=False,
        vocabulary={},
        prolog={},
        chunk_index=0,
        total_chunks=1,
    )
    result = engine.translate(request)
    assert result.text == "translated"
    assert captured["translator"] == "google"


def test_hysf_engine_parses_vocabulary(monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = config_module.load_config()
    monkeypatch.setenv("SILICONFLOW_API_KEY", "env-key")
    payload = '<output>cześć</output><vocabulary>{"hi": "cześć"}</vocabulary>'
    client = DummyClient(payload)
    engine = create_engine("hysf", cfg, client=client)

    request = EngineRequest(
        text="hi",
        source_lang="en",
        target_lang="pl",
        is_html=False,
        vocabulary={},
        prolog={"existing": "value"},
        chunk_index=0,
        total_chunks=1,
    )
    result = engine.translate(request)
    assert result.text == "cześć"
    assert result.vocabulary == {"hi": "cześć"}
    assert client.calls  # ensure API invoked


def test_ullm_engine_uses_profile(monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = config_module.load_config()
    profile = cfg.engines["ullm"].options["profiles"]["default"]
    profile["prolog"] = {"Term": "Translation"}
    config_module.save_config(cfg)
    monkeypatch.setenv("SILICONFLOW_API_KEY", "env-key")

    payload = '<output>done</output><vocabulary>{"Term": "Done"}</vocabulary>'
    client = DummyClient(payload)
    engine = create_engine("ullm/default", cfg, client=client)

    request = EngineRequest(
        text="Term",
        source_lang="en",
        target_lang="pl",
        is_html=False,
        vocabulary={"Existing": "Istniejący"},
        prolog={},
        chunk_index=0,
        total_chunks=2,
    )
    result = engine.translate(request)
    assert result.text == "done"
    assert result.vocabulary["Term"] == "Done"
    assert result.vocabulary["Existing"] == "Istniejący"
    assert client.calls[0]["model"] == profile["model"]
