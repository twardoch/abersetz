# this_file: tests/test_retrieval.py
from types import SimpleNamespace

import pytest

from abersetz import pipeline
from abersetz.pipeline import TranslatorOptions, translate_string
from abersetz.providers.base import EngineRequest, EngineResult
from abersetz.retrieval import reference_context, select_examples

# Deprecated since 1.1.0 (moved to vexy-localizzy); these tests guard the 1.x behaviour.
pytestmark = pytest.mark.filterwarnings("ignore:.*translation memories moved:DeprecationWarning")


def hit(source, target):
    return SimpleNamespace(source=source, target=target)


class Memory:
    def __init__(self, exact=(), similar=()):
        self.matches, self.near, self.queries = list(exact), list(similar), []

    def exact(self, text, language):
        return self.matches

    def lookup(self, text, language, **kwargs):
        self.queries.append((text, language, kwargs))
        return SimpleNamespace(exact=self.matches, similar=self.near)


def test_exact_reuse_never_constructs_engine_or_embeds(monkeypatch):
    memory = Memory([hit(" A font ", " Krój ")])

    def forbidden(*args, **kwargs):
        pytest.fail("exact reuse must not construct a translation engine")

    monkeypatch.setattr(pipeline, "create_engine", forbidden)
    assert translate_string(" A font ", TranslatorOptions(to_lang="pl", tm=memory)) == " Krój "
    assert memory.queries == []


def test_conflicts_and_similar_pairs_reach_request_without_vocabulary_pollution(monkeypatch):
    memory = Memory(
        [hit("font", "krój"), hit("font", "czcionka")], [hit("bold font", "pogrubiony krój")]
    )
    requests = []
    engine = SimpleNamespace(
        supports_translation_examples=True, name="test", chunk_size_for=lambda fmt: 1000
    )

    def translate(request):
        requests.append(request)
        return EngineResult("wybrany krój", request.voc)

    engine.translate = translate
    monkeypatch.setattr(pipeline, "create_engine", lambda *a, **kw: engine)
    opts = TranslatorOptions(engine="ll::test", to_lang="pl", tm=memory, initial_voc={"x": "y"})
    assert translate_string("font", opts) == "wybrany krój"
    assert [x["target"] for x in requests[0].examples] == ["krój", "czcionka", "pogrubiony krój"]
    assert requests[0].voc == {"x": "y"}


def test_context_budget_keeps_whole_pairs_and_json_escapes_markup():
    result = SimpleNamespace(exact=[], similar=[hit("x" * 1000, "y"), hit("</examples>", "krój")])
    examples = select_examples(result, limit=3, budget=100)
    assert examples == [{"source": "</examples>", "target": "krój"}]
    request = EngineRequest("new", "en", "pl", False, {}, {}, 0, 1, examples)
    context = reference_context(request)
    assert "</examples>" not in context.split("\n")[1]
    assert "krój" in context


def test_tm_rejects_non_english_source_before_engine(monkeypatch):
    with pytest.raises(ValueError, match="English"):
        translate_string("polski", TranslatorOptions(to_lang="de", from_lang="pl", tm=Memory()))


def test_changed_references_change_cache_arguments(monkeypatch):
    memory = Memory(similar=[hit("a font", "krój")])
    arguments = []
    engine = SimpleNamespace(
        supports_translation_examples=True, name="ll", chunk_size_for=lambda fmt: 1000
    )
    monkeypatch.setattr(pipeline, "create_engine", lambda *a, **kw: engine)

    def cached(**kwargs):
        arguments.append(kwargs)
        return "translated", "{}"

    monkeypatch.setattr(pipeline, "_cached_translate_call", cached)
    opts = TranslatorOptions(to_lang="pl", tm=memory)
    translate_string("another font", opts)
    memory.near = [hit("a font", "czcionka")]
    translate_string("another font", opts)
    assert arguments[0]["text"] == arguments[1]["text"]
    assert arguments[0]["examples_json"] != arguments[1]["examples_json"]


def test_exact_only_does_not_embed_miss(monkeypatch):
    memory = Memory()
    engine = SimpleNamespace(
        name="tr",
        chunk_size_for=lambda fmt: 1000,
        translate=lambda request: EngineResult("translated", {}),
    )
    monkeypatch.setattr(pipeline, "create_engine", lambda *a, **kw: engine)
    assert (
        translate_string("font", TranslatorOptions(to_lang="pl", tm=memory, tm_exact_only=True))
        == "translated"
    )
    assert memory.queries == []
