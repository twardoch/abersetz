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
        voc={},
        prolog={},
        chunk_index=0,
        total_chunks=1,
    )
    result = engine.translate(request)
    assert result.text == "translated"
    assert captured["translator"] == "google"


def test_hysf_engine_parses_voc(monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = config_module.load_config()
    monkeypatch.setenv("SILICONFLOW_API_KEY", "env-key")
    payload = '<output>cześć</output><voc>{"hi": "cześć"}</voc>'
    client = DummyClient(payload)
    engine = create_engine("hysf", cfg, client=client)

    request = EngineRequest(
        text="hi",
        source_lang="en",
        target_lang="pl",
        is_html=False,
        voc={},
        prolog={"existing": "value"},
        chunk_index=0,
        total_chunks=1,
    )
    result = engine.translate(request)
    assert result.text == "cześć"
    assert result.voc == {"hi": "cześć"}
    assert client.calls  # ensure API invoked


def test_ullm_engine_uses_profile(monkeypatch: pytest.MonkeyPatch) -> None:
    cfg = config_module.load_config()
    profile = cfg.engines["ullm"].options["profiles"]["default"]
    profile["prolog"] = {"Term": "Translation"}
    config_module.save_config(cfg)
    monkeypatch.setenv("SILICONFLOW_API_KEY", "env-key")

    payload = '<output>done</output><voc>{"Term": "Done"}</voc>'
    client = DummyClient(payload)
    engine = create_engine("ullm/default", cfg, client=client)

    request = EngineRequest(
        text="Term",
        source_lang="en",
        target_lang="pl",
        is_html=False,
        voc={"Existing": "Istniejący"},
        prolog={},
        chunk_index=0,
        total_chunks=2,
    )
    result = engine.translate(request)
    assert result.text == "done"
    assert result.voc["Term"] == "Done"
    assert result.voc["Existing"] == "Istniejący"
    assert client.calls[0]["model"] == profile["model"]


def test_translators_engine_retry_on_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that TranslatorsEngine retries on network failures."""

    cfg = config_module.load_config()
    engine = create_engine("translators/google", cfg)

    # Mock translators to fail twice then succeed
    call_count = 0

    def fake_translate_with_retry(
        text: str, translator: str, from_language: str, to_language: str, **_: object
    ) -> str:
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("Network error")
        return "Translated after retries"

    monkeypatch.setattr("abersetz.engines.translators.translate_text", fake_translate_with_retry)

    request = EngineRequest(
        text="hello",
        source_lang="en",
        target_lang="pl",
        is_html=False,
        voc={},
        prolog={},
        chunk_index=0,
        total_chunks=1,
    )

    result = engine.translate(request)
    assert result.text == "Translated after retries"
    assert call_count == 3  # Two failures + one success


def test_deep_translator_engine_retry_on_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that DeepTranslatorEngine retries on network failures."""

    cfg = config_module.load_config()

    # Mock GoogleTranslator to fail twice then succeed
    call_count = 0

    class MockTranslator:
        def __init__(self, source: str, target: str):
            self.source = source
            self.target = target

        def translate(self, text: str) -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("Network error")
            return "Translated after retries"

    # Patch the PROVIDERS dictionary directly
    from abersetz.engines import DeepTranslatorEngine

    original_providers = DeepTranslatorEngine.PROVIDERS.copy()
    DeepTranslatorEngine.PROVIDERS = {**original_providers, "google": MockTranslator}

    try:
        # Now create the engine after the mock is in place
        engine = create_engine("deep-translator/google", cfg)

        request = EngineRequest(
            text="hello",
            source_lang="en",
            target_lang="pl",
            is_html=False,
            voc={},
            prolog={},
            chunk_index=0,
            total_chunks=1,
        )

        result = engine.translate(request)
        assert result.text == "Translated after retries"
        assert call_count == 3  # Two failures + one success
    finally:
        # Restore original PROVIDERS
        DeepTranslatorEngine.PROVIDERS = original_providers
