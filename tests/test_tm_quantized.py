# this_file: tests/test_tm_quantized.py
"""Real TurboQuant search and Rust caching through the translation pipeline."""

from types import SimpleNamespace

import numpy as np
import pytest
from uubed.memory import build_memory

from abersetz import pipeline
from abersetz.pipeline import TranslatorOptions, translate_string
from abersetz.providers.base import EngineResult


class Encoder:
    dimensions = 32
    space = "abersetz-turbo-test"
    task = "similarity"
    backend = "fastembed"
    model = SimpleNamespace(model_id="google/embeddinggemma-300m")
    max_tokens = 128
    prefix = ""
    calls = 0

    def __init__(self, **kwargs):
        pass

    def embed(self, texts):
        type(self).calls += 1
        vectors = np.zeros((len(texts), self.dimensions), dtype=np.float32)
        for i, text in enumerate(texts):
            vectors[i, 0 if "font" in text else 1] = 1
        return vectors

    def close(self):
        pass


@pytest.mark.parametrize("backend", ["turbovec", "turbo-graph"])
def test_pipeline_when_quantized_tm_then_exact_semantic_cache_and_constraints(
    tmp_path, monkeypatch, backend
):
    if backend == "turbo-graph":
        pytest.importorskip("turbo_graph")
    source = tmp_path / "memory.tmx"
    source.write_text(
        '<tmx><body><tu><tuv xml:lang="en"><seg>A font</seg></tuv>'
        '<tuv xml:lang="pl"><seg>Krój pisma</seg></tuv></tu>'
        '<tu><tuv xml:lang="en"><seg>A cat</seg></tuv>'
        '<tuv xml:lang="de"><seg>Katze</seg></tuv></tu></body></tmx>'
    )
    database = tmp_path / "memory.sqlite"
    build_memory([source], database, Encoder(), search_backend=backend)
    monkeypatch.setattr("uubed.memory.Embedder", Encoder)
    Encoder.calls = 0
    requests = []

    def translate(request):
        requests.append(request)
        return EngineResult("Nowy krój", request.voc)

    engine = SimpleNamespace(
        name="test",
        supports_translation_examples=True,
        chunk_size_for=lambda fmt: 1000,
        translate=translate,
    )
    monkeypatch.setattr(pipeline, "create_engine", lambda *a, **k: engine)
    opts = TranslatorOptions(to_lang="pl", from_lang="en", tm=database)
    assert translate_string("A font", opts) == "Krój pisma"
    assert not requests and Encoder.calls == 0, "exact reuse must not infer"
    assert translate_string("Another font", opts) == "Nowy krój"
    assert requests[0].examples == [{"source": "A font", "target": "Krój pisma"}]
    assert Encoder.calls == 1
    assert translate_string("Another font", opts) == "Nowy krój"
    assert len(requests) == Encoder.calls == 1, "both inference and translation must hit disk cache"
    opts.tm_minimum = 0.8
    translate_string("Another font", opts)
    assert Encoder.calls == 2, "changed search settings must re-run retrieval"
    if backend == "turbo-graph":
        opts.tm_related_to, opts.tm_max_hops = ["A cat"], 0
        translate_string("Another font", opts)
        assert requests[-1].examples == [], "graph/language constraints must reach Uubed"
    opts.tm_search_backend = "sqlite"
    opts.tm_related_to = None
    translate_string("Another font", opts)
    assert Encoder.calls >= 3, "explicit exhaustive SQLite fallback remains usable"
