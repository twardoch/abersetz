---
this_file: README.md
---
# abersetz

Minimalist file translator that reuses proven machine translation engines while keeping configuration portable and repeatable. The tool walks through a simple locate → chunk → translate → merge pipeline and exposes both a Python API and a `fire`-powered CLI.

## Why abersetz?
- Focuses on translating files, not single strings.
- Reuses stable engines from `translators` and `deep-translator`, plus pluggable LLM-based engines for consistent terminology.
- Persists engine preferences and API secrets with `platformdirs`, supporting either raw values or the environment variable that stores them.
- Shares vocabulary between chunks so long documents stay consistent.
- Keeps a lean codebase: no custom infrastructure, just clear building blocks.

## Key Features
- Recursive file discovery with include/exclude filters.
- Automatic HTML vs. plain-text detection to preserve markup when possible.
- Semantic chunking via `semantic-text-splitter`, with configurable lengths per engine.
- Vocabulary-aware translation pipeline that merges `<vocabulary>` JSON emitted by LLM engines.
- Offline-friendly dry-run mode for testing and demos.
- Optional vocabulary sidecar files when `--save-voc` is set.

## Installation
```bash
pip install abersetz
```

## Quick Start
```bash
# Using the main CLI
abersetz tr ./docs --to-lang pl --engine translators/google --output ./build/pl

# Or using the shorthand command
abtr ./docs --to-lang pl --engine translators/google --output ./build/pl
```

### CLI Options (preview)
- `--from-lang`: source language (defaults to `auto`).
- `--to-lang`: target language (default `en`).
- `--engine`: one of
  - `translators/<provider>` (e.g. `translators/google`)
  - `deep-translator/<provider>` (e.g. `deep-translator/deepl`)
  - `hysf`
  - `ullm/<profile>` where profiles are defined in config.
- `--recurse/--no-recurse`: recurse into subdirectories (defaults to on).
- `--overwrite`: replace input files instead of writing to output dir.
- `--save-voc`: drop merged vocabulary JSON next to each translated file.
- `--chunk-size` / `--html-chunk-size`: override default chunk lengths.
- `--verbose`: enable debug logging via loguru.

## Configuration
`abersetz` stores runtime configuration under the user config path determined by `platformdirs`. The config file keeps:
- Global defaults (engine, languages, chunk sizes).
- Engine-specific settings (API endpoints, retry policies, HTML behaviour).
- Credential entries, each allowing either `{ "env": "ENV_NAME" }` or `{ "value": "actual-secret" }`.

Example snippet (stored in `config.json`):
```json
{
  "defaults": {
    "engine": "translators/google",
    "from_lang": "auto",
    "to_lang": "en",
    "chunk_size": 1200,
    "html_chunk_size": 1800
  },
  "credentials": {
    "siliconflow": {"env": "SILICONFLOW_API_KEY"}
  },
  "engines": {
    "hysf": {
      "chunk_size": 2400,
      "credential": {"name": "siliconflow"},
      "options": {
        "model": "tencent/Hunyuan-MT-7B",
        "base_url": "https://api.siliconflow.com/v1",
        "temperature": 0.3
      }
    },
    "ullm": {
      "chunk_size": 2400,
      "credential": {"name": "siliconflow"},
      "options": {
        "profiles": {
          "default": {
            "base_url": "https://api.siliconflow.com/v1",
            "model": "tencent/Hunyuan-MT-7B",
            "temperature": 0.3,
            "max_input_tokens": 32000,
            "prolog": {}
          }
        }
      }
    }
  }
}
```
Use `abersetz config show` and `abersetz config path` to inspect the file.

## CLI Tools
- `abersetz`: Main CLI with `tr` (translate) and `config` commands
- `abtr`: Direct translation shorthand (equivalent to `abersetz tr`)

## Python API
```python
from abersetz import translate_path, TranslatorOptions

translate_path(
    path="docs",
    options=TranslatorOptions(to_lang="de", engine="translators/google"),
)
```

## Examples
The `examples/` directory holds ready-to-run demos:
- `poem_en.txt`: source text.
- `poem_pl.txt`: translated sample output.
- `vocab.json`: vocabulary generated during translation.
- `walkthrough.md`: step-by-step CLI invocation log.

## Development Workflow
```bash
uv sync
python -m pytest --cov=. --cov-report=term-missing
ruff check src tests
ruff format src tests
```

## Testing Philosophy
- Every helper has direct unit coverage.
- Integration tests exercise the pipeline with a stub engine.
- Network calls are mocked; real APIs are never hit in CI.

## License
MIT
