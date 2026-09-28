# this_file: tests/test_engine_api.py
"""Stable engine API: create_engine and LlmEngine.max_attempts."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

import abersetz
from abersetz import engine_api
from abersetz.config import AbersetzConfig, Credential, EngineConfig
from abersetz.providers.base import EngineError, EngineRequest
from abersetz.providers.llm.inference import LlmEngine


class FlakyClient:
    """OpenAI-shaped fake: fails ``failures`` times, then answers."""

    def __init__(self, failures: int) -> None:
        self.failures, self.calls = failures, 0
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))

    def create(self, **kwargs):
        self.calls += 1
        if self.calls <= self.failures:
            raise ConnectionError(f"boom {self.calls}")
        message = SimpleNamespace(content="<output>Cześć</output>")
        return SimpleNamespace(choices=[SimpleNamespace(message=message)])


def request() -> EngineRequest:
    return EngineRequest(
        text="Hello",
        source_lang="en",
        target_lang="pl",
        is_html=False,
        voc={},
        prolog={},
        chunk_index=0,
        total_chunks=1,
    )


@pytest.fixture(autouse=True)
def no_backoff(monkeypatch: pytest.MonkeyPatch) -> None:
    """Tenacity sleeps between attempts; tests must not."""
    monkeypatch.setattr("tenacity.nap.time.sleep", lambda seconds: None)


def llm(client: FlakyClient, **kwargs) -> LlmEngine:
    return LlmEngine(EngineConfig(name="ll"), client, model="m", temperature=0.0, **kwargs)


def test_llm_engine_when_max_attempts_1_then_exactly_one_call() -> None:
    client = FlakyClient(failures=5)
    with pytest.raises(ConnectionError, match="boom 1"):
        llm(client, max_attempts=1).translate(request())
    assert client.calls == 1, "max_attempts=1 must not retry"


def test_llm_engine_when_default_then_retries_three_times() -> None:
    client = FlakyClient(failures=2)
    result = llm(client).translate(request())
    assert result.text == "Cześć"
    assert client.calls == 3, "default behaviour is three attempts"

    exhausted = FlakyClient(failures=5)
    with pytest.raises(ConnectionError, match="boom 3"):
        llm(exhausted).translate(request())
    assert exhausted.calls == 3


@pytest.mark.parametrize("bad", [0, -1, 1.5, "2", True])
def test_llm_engine_when_max_attempts_invalid_then_value_error(bad) -> None:
    with pytest.raises(ValueError, match="max_attempts"):
        llm(FlakyClient(0), max_attempts=bad)


def test_legacy_wrapped_alias_is_single_attempt() -> None:
    """vexy-localizzy 1.0.28 code calls ``LlmEngine._invoke.__wrapped__``."""
    client = FlakyClient(failures=5)
    engine = llm(client)
    with pytest.raises(ConnectionError):
        LlmEngine._invoke.__wrapped__(engine, [{"role": "user", "content": "x"}])
    assert client.calls == 1


def profile_config() -> AbersetzConfig:
    """Explicit config so the workstation's abersetz.toml never leaks into tests."""
    return AbersetzConfig(
        credentials={"fake": Credential(name="fake", env="ABERSETZ_TEST_FAKE_KEY")},
        engines={
            "ullm": EngineConfig(
                name="ullm",
                chunk_size=900,
                credential=Credential(name="fake"),
                options={"profiles": {"fake": {"model": "fake-model", "temperature": 0.1}}},
            )
        },
    )


def test_create_engine_when_ll_selector_and_injected_client_then_uses_client(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ABERSETZ_TEST_FAKE_KEY", "sk-test")
    client = FlakyClient(failures=0)
    engine = engine_api.create_engine("ll::fake", config=profile_config(), client=client)
    assert isinstance(engine, LlmEngine)
    assert engine.max_attempts == 3
    assert engine.chunk_size == 900
    assert engine.translate(request()).text == "Cześć"
    assert client.calls == 1


def test_create_engine_when_max_attempts_1_then_single_attempt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ABERSETZ_TEST_FAKE_KEY", "sk-test")
    client = FlakyClient(failures=5)
    engine = engine_api.create_engine(
        "ll::fake", config=profile_config(), client=client, max_attempts=1
    )
    with pytest.raises(ConnectionError):
        engine.translate(request())
    assert client.calls == 1


def test_create_engine_when_max_attempts_for_non_llm_then_engine_error() -> None:
    config = AbersetzConfig(engines={"translators": EngineConfig(name="translators")})
    with pytest.raises(EngineError, match="only for ll engines"):
        engine_api.create_engine("tr::google", config=config, max_attempts=1)


def test_create_engine_when_max_attempts_zero_then_value_error() -> None:
    with pytest.raises(ValueError, match="max_attempts"):
        engine_api.create_engine("ll::fake", config=profile_config(), max_attempts=0)


def test_engine_api_reexports_llm_engine() -> None:
    assert engine_api.LlmEngine is LlmEngine
    assert engine_api.EngineConfig is EngineConfig
    assert {"LlmEngine", "EngineConfig", "AbersetzConfig"} <= set(engine_api.__all__)


def test_package_exports_engine_api_lazily() -> None:
    assert abersetz.create_engine is engine_api.create_engine
    assert abersetz.EngineRequest is EngineRequest
    assert abersetz.EngineError is EngineError
    assert {"create_engine", "EngineRequest", "EngineResult", "EngineError"} <= set(
        abersetz.__all__
    )
