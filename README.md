---
this_file: README.md
---
# abersetz

Minimalist file translator that reuses proven machine translation engines while keeping configuration portable and repeatable. The tool walks through a simple locate → chunk → translate → merge pipeline and exposes both a Python API and a `fire`-powered CLI.

## Why abersetz?
- Focuses on translating files, not single strings.
- Reuses stable engines from `translators` and `deep-translator`, plus pluggable LLM-based engines for consistent terminology.
- Persists engine preferences and API secrets with `platformdirs`, supporting either raw values or the environment variable that stores them.
- Shares voc between chunks so long documents stay consistent.
- Keeps a lean codebase: no custom infrastructure, just clear building blocks.

## Key Features
- Recursive file discovery with include/xclude filters.
- Automatic HTML vs. plain-text detection to preserve markup when possible.
- Semantic chunking via `semantic-text-splitter`, with configurable lengths per engine.
- voc-aware translation pipeline that merges `<voc>` JSON emitted by LLM engines.
- Offline-friendly dry-run mode for testing and demos.
- Optional voc sidecar files when `--save-voc` is set.
- Built-in `abersetz validate` health check that pings each configured engine, reports latency, and surfaces pricing hints from the research catalog.

## Installation
```bash
pip install abersetz
```

## Quick Start

### First-time Setup
```bash
# Automatically discover and configure available translation services
abersetz setup

# Smoke-test configured engines with a single command
abersetz validate --target-lang es
```

This will scan your environment for API keys, test endpoints, and create an optimized configuration.

### Basic Translation
```bash
# Using the main CLI
abersetz tr pl ./docs --engine tr/google --output ./build/pl

# Or using the shorthand command
abtr pl ./docs --engine tr/google --output ./build/pl
```

### CLI Options (preview)
- `to_lang`: first positional argument selecting the target language.
- `--from-lang`: source language (defaults to `auto`).
- `--engine`: one of
  - `tr/<provider>` (e.g. `tr/google`)
  - `dt/<provider>` (e.g. `dt/deepl`)
  - `hy`
  - `ll/<profile>` where profiles are defined in config.
    - Legacy selectors such as `translators/google` remain accepted and are auto-normalized.
- `--recurse/--no-recurse`: recurse into subdirectories (defaults to on).
- `--write_over`: replace input files instead of writing to output dir.
- `--save-voc`: drop merged voc JSON next to each translated file.
- `--chunk-size` / `--html-chunk-size`: override default chunk lengths.
- `--verbose`: enable debug logging via loguru.
- `abersetz engines` extras:
  - `--family tr|dt|ll|hy`: filter listing to a single engine family.
  - `--configured-only`: show only configured engines.
- `abersetz validate` extras:
  - `--selectors tr/google,ll/default`: limit validation to specific selectors (comma-separated).
  - `--target-lang es`: override the default sample translation language (`es`).
  - `--sample-text "Hello!"`: supply a custom validation snippet.

## Configuration
`abersetz` stores runtime configuration under the user config path determined by `platformdirs`. The config file keeps:
- Global defaults (engine, languages, chunk sizes).
- Engine-specific settings (API endpoints, retry policies, HTML behaviour).
- Credential entries, each allowing either `{ "env": "ENV_NAME" }` or `{ "value": "actual-secret" }`.

Example snippet (stored in `config.toml`):
```toml
[defaults]
engine = "tr/google"
from_lang = "auto"
to_lang = "en"
chunk_size = 1200
html_chunk_size = 1800

[credentials.siliconflow]
name = "siliconflow"
env = "SILICONFLOW_API_KEY"

[engines.hysf]
chunk_size = 2400

[engines.hysf.credential]
name = "siliconflow"

[engines.hysf.options]
model = "tencent/Hunyuan-MT-7B"
base_url = "https://api.siliconflow.com/v1"
temperature = 0.3

[engines.ullm]
chunk_size = 2400

[engines.ullm.credential]
name = "siliconflow"

[engines.ullm.options.profiles.default]
base_url = "https://api.siliconflow.com/v1"
model = "tencent/Hunyuan-MT-7B"
temperature = 0.3
max_input_tokens = 32000

[engines.ullm.options.profiles.default.prolog]
```
Use `abersetz config show` and `abersetz config path` to inspect the file.

## CLI Tools
- `abersetz`: Main CLI exposing `tr` (translate), `validate`, and `config` commands.
- `abtr`: Direct translation shorthand (equivalent to `abersetz tr`).

## Python API
```python
from abersetz import translate_path, TranslatorOptions

translate_path(
    path="docs",
    options=TranslatorOptions(to_lang="de", engine="tr/google"),
)
```

## Examples
The `examples/` directory holds ready-to-run demos:
- `poem_en.txt`: source text.
- `poem_pl.txt`: translated sample output.
- `vocab.json`: voc generated during translation.
- `walkthrough.md`: step-by-step CLI invocation log.
- `validate_report.sh`: captures the validation summary table for quick audits.

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
