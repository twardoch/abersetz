# this_file: tests/test_local_engines.py
"""Hy-MT2 / TranslateGemma behaviour of the ``ml``, ``gg`` and ``lm`` engines (offline)."""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from abersetz import config as config_module
from abersetz.engines import create_engine
from abersetz.providers.base import EngineRequest
from abersetz.providers.lmstudio import lmstudio_family
from abersetz.providers.local_models import family_for_model


def _request(text: str = "Hello", *, source: str = "en", target: str = "pl") -> EngineRequest:
    return EngineRequest(
        text=text,
        source_lang=source,
        target_lang=target,
        is_html=False,
        voc={},
        prolog={},
        chunk_index=0,
        total_chunks=1,
    )


# ---------------------------------------------------------------------------
# family inference
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("7b-mlx", "mthy"),
        ("tg-4b-gguf", "gemma"),
        ("mlx-community/Hy-MT2-7B-8bit", "mthy"),
        ("/models/translategemma-12b-it.Q8_0.gguf", "gemma"),
        ("/models/HY-MT2-7B-Q8_0.gguf", "mthy"),
        ("some/other-model", None),
        (None, None),
    ],
)
def test_family_for_model(name: str | None, expected: str | None) -> None:
    assert family_for_model(name) == expected


@pytest.mark.parametrize(
    ("model", "sub", "expected"),
    [
        ("hy-mt2-7b", None, "mthy"),
        ("translategemma-4b-it", None, "gemma"),
        ("gemma-3-4b", None, "generic"),
        ("gemma-3-4b", "hy-mt2", "mthy"),
        ("whatever", "tg", "gemma"),
        ("whatever", "qwen", "generic"),
    ],
)
def test_lmstudio_family(model: str, sub: str | None, expected: str) -> None:
    assert lmstudio_family(model, sub) == expected


# ---------------------------------------------------------------------------
# MLX
# ---------------------------------------------------------------------------


def _install_fake_mlx(monkeypatch: pytest.MonkeyPatch, captured: dict[str, object]) -> None:
    tokenizer = SimpleNamespace(chat_template="template")

    def fake_apply_chat_template(messages, **_):
        captured["messages"] = messages
        return "templated"

    tokenizer.apply_chat_template = fake_apply_chat_template

    def fake_generate(*_, **kwargs):
        captured["generate"] = kwargs
        return "translated<end_of_turn>"

    monkeypatch.setitem(
        sys.modules,
        "mlx_lm",
        SimpleNamespace(load=lambda _: (object(), tokenizer), generate=fake_generate),
    )
    monkeypatch.setitem(
        sys.modules,
        "mlx_lm.sample_utils",
        SimpleNamespace(
            make_sampler=lambda **kw: ("sampler", kw),
            make_logits_processors=lambda **kw: ("processors", kw),
        ),
    )


def test_ml_hymt2_when_default_then_official_sampler(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    model_dir = tmp_path / "Hy-MT2-7B-8bit"
    model_dir.mkdir()
    captured: dict[str, object] = {}
    _install_fake_mlx(monkeypatch, captured)

    engine = create_engine(f"ml::{model_dir}", config_module.load_config())
    assert engine._family == "mthy", "family should be inferred from the folder name"
    assert engine._max_tokens == 4096
    result = engine.translate(_request())

    assert result.text == "translated<end_of_turn>"
    gen = captured["generate"]
    assert gen["sampler"] == ("sampler", {"temp": 0.7, "top_p": 0.6, "top_k": 20})
    assert gen["logits_processors"] == ("processors", {"repetition_penalty": 1.05})
    assert captured["messages"] == [
        {"role": "user", "content": captured["messages"][0]["content"]}
    ], "single user turn, no system prompt"


def test_ml_hymt2_when_30b_then_moe_sampler(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    model_dir = tmp_path / "Hy-MT2-30B-A3B-oQ8-MLX"
    model_dir.mkdir()
    captured: dict[str, object] = {}
    _install_fake_mlx(monkeypatch, captured)

    engine = create_engine(f"ml/hy-mt2::{model_dir}", config_module.load_config(), temperature=0.2)
    engine.translate(_request())
    gen = captured["generate"]
    assert gen["sampler"] == ("sampler", {"temp": 0.2, "top_p": 1.0}), "top_k omitted for MoE"
    assert "logits_processors" not in gen, "30B recipe has repetition_penalty 1.0"


def test_ml_gemma_when_translategemma_then_structured_messages_and_greedy(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    model_dir = tmp_path / "translategemma-4b-it-8bit"
    model_dir.mkdir()
    captured: dict[str, object] = {}
    _install_fake_mlx(monkeypatch, captured)

    engine = create_engine(f"ml::{model_dir}", config_module.load_config())
    assert engine._family == "gemma"
    result = engine.translate(_request(source="auto", target="de"))

    assert result.text == "translated", "trailing <end_of_turn> is stripped"
    content = captured["messages"][0]["content"][0]
    assert content == {
        "type": "text",
        "source_lang_code": "en",
        "target_lang_code": "de",
        "text": "Hello",
    }
    assert "sampler" not in captured["generate"], "TranslateGemma decodes greedily"


# ---------------------------------------------------------------------------
# GGUF
# ---------------------------------------------------------------------------


def _install_fake_llama(monkeypatch: pytest.MonkeyPatch, captured: dict[str, object]) -> None:
    class FakeLlama:
        def __init__(self, **kwargs):
            captured["init"] = kwargs

        def create_chat_completion(self, **kwargs):
            captured["call"] = kwargs
            return {"choices": [{"message": {"content": " result "}}]}

    monkeypatch.setitem(sys.modules, "llama_cpp", SimpleNamespace(Llama=FakeLlama))


def test_gg_hymt2_when_default_then_official_params(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    model = tmp_path / "Hy-MT2-1.8B-Q8_0.gguf"
    model.write_text("stub")
    captured: dict[str, object] = {}
    _install_fake_llama(monkeypatch, captured)

    engine = create_engine(f"gg::{model}", config_module.load_config())
    result = engine.translate(_request(target="fr"))

    assert result.text == "result"
    call = captured["call"]
    assert call["temperature"] == 0.7
    assert call["top_p"] == 0.6
    assert call["top_k"] == 20
    assert call["repeat_penalty"] == 1.05
    assert call["max_tokens"] == 4096
    assert call["messages"][0]["role"] == "user"
    assert "Translate the following text into French." in call["messages"][0]["content"]


def test_gg_hymt2_when_30b_then_no_top_k(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    model = tmp_path / "Hy-MT2-30B-A3B.Q4_K_M.gguf"
    model.write_text("stub")
    captured: dict[str, object] = {}
    _install_fake_llama(monkeypatch, captured)

    engine = create_engine(f"gg::{model}", config_module.load_config(), temperature=0.1)
    engine.translate(_request())
    call = captured["call"]
    assert call["temperature"] == 0.1, "explicit override wins"
    assert call["top_p"] == 1.0
    assert "top_k" not in call


def test_gg_gemma_when_translategemma_then_greedy(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    model = tmp_path / "translategemma-4b-it.Q8_0.gguf"
    model.write_text("stub")
    captured: dict[str, object] = {}
    _install_fake_llama(monkeypatch, captured)

    engine = create_engine(f"gg::{model}", config_module.load_config())
    assert engine._family == "gemma"
    engine.translate(_request(source="cs", target="de-DE"))
    call = captured["call"]
    assert call["temperature"] == 0.0
    assert "top_p" not in call
    assert call["messages"][0]["content"][0]["source_lang_code"] == "cs"
    assert call["messages"][0]["content"][0]["target_lang_code"] == "de-DE"


# ---------------------------------------------------------------------------
# LM Studio
# ---------------------------------------------------------------------------


def _install_fake_lms(monkeypatch: pytest.MonkeyPatch, captured: dict[str, object]) -> None:
    class Model:
        def __init__(self, name):
            self.name = name

        def respond(self, prompt, config=None):
            captured["prompt"] = prompt
            captured["config"] = config
            return "lms-out"

    monkeypatch.setitem(
        sys.modules,
        "lmstudio",
        SimpleNamespace(configure_default_client=lambda _: None, llm=lambda n: Model(n)),
    )
    monkeypatch.setattr("shutil.which", lambda _: None)


def test_lm_hymt2_when_model_id_then_prompt_and_sampler(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}
    _install_fake_lms(monkeypatch, captured)

    engine = create_engine("lm::hy-mt2-7b", config_module.load_config())
    engine.translate(_request(target="pl"))

    assert str(captured["prompt"]).startswith("Translate the following text into Polish.")
    assert captured["config"] == {
        "temperature": 0.7,
        "topPSampling": 0.6,
        "repeatPenalty": 1.05,
        "maxTokens": 4096,
        "topKSampling": 20,
    }


def test_lm_hymt2_when_subvariant_then_forced_family(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}
    _install_fake_lms(monkeypatch, captured)

    engine = create_engine(
        "lm/hy-mt2::my-local-model", config_module.load_config(), temperature=0.3
    )
    engine.translate(_request(target="de"))
    assert engine._family == "mthy"
    assert captured["config"]["temperature"] == 0.3


def test_lm_gemma_when_translategemma_then_rendered_template(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}
    _install_fake_lms(monkeypatch, captured)

    engine = create_engine("lm::translategemma-4b-it", config_module.load_config())
    engine.translate(_request(source="en", target="pl"))

    prompt = str(captured["prompt"])
    assert prompt.startswith("You are a professional English (en) to Polish (pl) translator.")
    assert prompt.endswith("Please translate the following English text into Polish:\n\n\nHello")
    assert captured["config"] == {"temperature": 0.0}


def test_lm_generic_when_unknown_model_then_plain_instruction(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}
    _install_fake_lms(monkeypatch, captured)

    engine = create_engine("lm::qwen2.5-7b", config_module.load_config())
    engine.translate(_request(target="pl"))
    assert str(captured["prompt"]).startswith("Translate the following segment into Polish")
    assert captured["config"] == {}


def test_ml_hymt2_when_snapshot_path_then_name_and_sampler_from_alias(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """HF snapshots resolve to ``…/snapshots/<sha>``; the alias must still drive naming/sampling."""
    snapshot = tmp_path / "models--dawncr0w--Hy-MT2-30B-A3B-oQ8-MLX" / "snapshots" / "0123abcd"
    snapshot.mkdir(parents=True)
    captured: dict[str, object] = {}
    _install_fake_mlx(monkeypatch, captured)
    monkeypatch.setattr(
        "abersetz.providers.mlx.resolve_and_download_model", lambda *_: str(snapshot)
    )

    engine = create_engine("ml::30b-mlx", config_module.load_config())
    assert engine._model_name == "30b-mlx"
    engine.translate(_request())
    assert captured["generate"]["sampler"] == ("sampler", {"temp": 0.7, "top_p": 1.0})
