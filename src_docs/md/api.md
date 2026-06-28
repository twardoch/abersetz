---
title: Python API
description: Public Python API for abersetz — translate files and directory trees programmatically.
---

# Python API Reference

## Quick start

```python
from abersetz.pipeline import TranslatorOptions, translate_path
from pathlib import Path

results = translate_path(
    Path("./docs"),
    TranslatorOptions(engine="tr::google", to_lang="es"),
)
for r in results:
    print(f"{r.source} -> {r.destination} ({r.chunks} chunks)")
```

## `translate_path`

Main entry point for translating files or directory trees.

```python
from abersetz.pipeline import translate_path, TranslatorOptions

results = translate_path(
    path,          # str | Path — file or directory
    options,       # TranslatorOptions
    config=None,   # AbersetzConfig | None — custom config, loads from disk if None
    client=None,   # Any | None — custom HTTP client (tests / proxies)
)
# Returns: list[TranslationResult]
```

## `TranslatorOptions`

```python
from abersetz.pipeline import TranslatorOptions

opts = TranslatorOptions(
    engine="tr::google",        # engine selector
    from_lang="auto",           # source language (default: auto-detect)
    to_lang="pl",               # target language
    recurse=True,               # recurse into sub-directories
    write_over=False,           # overwrite source files in-place
    output_dir=None,            # Path | None — explicit output root
    save_voc=False,             # write vocabulary JSON alongside output
    chunk_size=None,            # int | None — override engine default
    html_chunk_size=None,       # int | None — override for HTML
    include=("*.md", "*.txt"),  # file glob patterns to include
    xclude=(),                  # file glob patterns to exclude
    dry_run=False,              # preview without making any API calls
    prolog={},                  # dict[str, str] — static LLM context
    initial_voc={},             # dict[str, str] — seed vocabulary
)
```

## `TranslationResult`

Each call to `translate_path` returns a list of `TranslationResult` objects:

```python
result.source       # Path — input file
result.destination  # Path — output file
result.chunks       # int — number of chunks translated
result.voc          # dict[str, str] — accumulated vocabulary (LLM engines)
result.format       # TextFormat — PLAIN | HTML | MARKDOWN
```

## Low-level: using engines directly

```python
from abersetz.engines import create_engine, EngineRequest
from abersetz.config import load_config

config = load_config()
engine = create_engine("tr::google", config)

request = EngineRequest(
    text="Hello, world!",
    source_lang="en",
    target_lang="es",
    is_html=False,
    voc={},
    prolog={},
    chunk_index=0,
    total_chunks=1,
)

result = engine.translate(request)
print(result.text)   # "¡Hola, mundo!"
```

## Configuration API

```python
from abersetz.config import load_config, save_config, AbersetzConfig, Defaults

# Load from disk (respects per-project abersetz.toml)
config = load_config()

# Modify and save
config.defaults.to_lang = "de"
save_config(config)
```

## Error handling

```python
from abersetz.providers.base import EngineError
from abersetz.pipeline import PipelineError

try:
    results = translate_path("missing.txt", TranslatorOptions(to_lang="es"))
except PipelineError as e:
    print(f"Pipeline failed: {e}")
except EngineError as e:
    print(f"Engine error: {e}")
```

## Auto-generated API docs

::: abersetz.pipeline
    options:
      members:
        - translate_path
        - TranslatorOptions
        - TranslationResult

::: abersetz.engines
    options:
      members:
        - create_engine

::: abersetz.config
    options:
      members:
        - load_config
        - save_config
        - AbersetzConfig
