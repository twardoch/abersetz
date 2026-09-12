---
this_file: src_docs/md/translation-memory.md
title: Translation memory and caching
description: Local FastEmbed inference, TurboQuant search and persistent Rust caching.
---

# Translation memory and caching

Abersetz reuses unique verbatim translations before loading an embedding or
translation model. On misses or conflicts, compatible LLM engines receive bounded
bilingual examples from Uubed. Examples remain request-local and never alter your
saved vocabulary.

## Build a local memory

Install the current Uubed Python package and native wheel, then `abersetz[tm]`
and `uubed[fastembed]`. These integration changes are unreleased: when working
from source, build `uubed-rs` with `./build.sh`, install its wheel, and install
the sibling `uubed-py` and Abersetz checkouts with `uv pip install -e`.

```bash
uubed tm build corpus/ --output localization.sqlite --model gemma \
  --backend fastembed --device cpu --dimensions 256 \
  --search-backend turbovec --bit-width 4

abersetz tr pl 'Make the font bold.' --from-lang=en \
  --tm=localization.sqlite --engine='gg/mthy::1.8b-gguf'
```

FastEmbed runs locally in Rust/ONNX Runtime and downloads pinned weights only on
first inference. Gemma, Jina, MiniLM, Granite, Nomic v2 MoE and Voyage nano are
supported. Voyage lite remains API-only. FastEmbed needs CPU; no GGUF model path
is needed for embedding. The translation engine is selected separately.

## TurboQuant search

Turbovec implements TurboQuant in Rust with 2/3/4-bit search indexes. Uubed keeps
the index inside the SQLite memory, alongside authoritative int8 vectors, text,
translation alternatives and provenance. Language-filtered approximate candidates
are reranked with int8 cosine scores. The extra index adds disk space; it does not
make the whole SQLite database smaller or promise exhaustive recall.

Abersetz automatically uses the stored search backend. Use
`--tm-search-backend=sqlite` for exhaustive search, including when the optional
search runtime is unavailable. `--tm-exact-only` bypasses semantic inference.
Existing files can be copied/indexed without re-embedding:

```bash
uubed tm index original.sqlite --output indexed.sqlite --search-backend turbovec
```

`--tm-top-k=5`, `--tm-minimum=0.5`, and `--tm-context-chars=4000` limit the number,
cosine threshold and serialized JSON character budget of complete example pairs.
Regional target-language codes must match the database exactly. Hy-MT MLX/GGUF,
LM Studio and supported `ll` engines accept examples; other prompt adapters require
exact-only mode. File `--job` and `--tm` remain separate workflows.

## Graph constraints

For adjacency/provenance constraints, install the pinned Turbo-Graph source:

```bash
uv pip install 'git+https://github.com/bigmacfive/turbo-graph@72f10416d4c954d42561f90465190f000e29cca9#subdirectory=turbo-graph-python'
uubed tm index original.sqlite --output graph.sqlite --search-backend turbo-graph
abersetz tr pl 'Make the font bold.' --from-lang=en --tm=graph.sqlite \
  --tm-related-to='["Bold"]' --tm-max-hops=1 \
  --engine='gg/mthy::1.8b-gguf'
```

Seeds are exact English source strings. `--tm-origins='["/stored/corpus/file.tmx"]'`
restricts candidates by their stored TMX origin. These constraints require a graph
index and are combined with language filtering inside native search.

## Persistent Rust cache

`diskcache-rs==0.4.10` caches completed chunk translations and TM example lists.
Repeated requests can skip embedding/search and translator calls, even after a
process restart. Cache hits may still initialize the translation engine to resolve
its settings and chunk sizes. Keys include the request, model/engine settings,
language, vocabulary, prolog, local weight-file identity and selected examples. TM keys additionally include
database file identity, index/model configuration, thresholds and graph constraints.
Custom injected embedders and GGUF TM queries bypass the example cache so Uubed
can validate their model identity.

The default location is the platform user cache directory under
`abersetz/abersetz-results-v1`. Set `ABERSETZ_CACHE_DIR` to choose another root or
`ABERSETZ_CACHE=0` to bypass both caches. The previous `twat-cache` files are left
untouched. Cached values use JSON bytes. Failed provider calls are never stored;
cache I/O failures log a warning and return the computed result. Hosted models
can change behind a stable name: clear this cache when replacing such a model.
