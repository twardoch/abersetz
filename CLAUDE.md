---
this_file: CLAUDE.md
---
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
abersetz translate ./docs --to-lang pl --engine translators/google --output ./build/pl
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

# When you write code

- Iterate gradually, avoiding major changes
- Minimize confirmations and checks
- Preserve existing code/structure unless necessary
- Use constants over magic numbers
- Check for existing solutions in the codebase before starting
- Check often the coherence of the code you’re writing with the rest of the code.
- Focus on minimal viable increments and ship early
- Write explanatory docstrings/comments that explain what and WHY this does, explain where and how the code is used/referred to elsewhere in the code
- Analyze code line-by-line
- Handle failures gracefully with retries, fallbacks, user guidance
- Address edge cases, validate assumptions, catch errors early
- Let the computer do the work, minimize user decisions
- Reduce cognitive load, beautify code
- Modularize repeated logic into concise, single-purpose functions
- Favor flat over nested structures
- Consistently keep, document, update and consult the holistic overview mental image of the codebase. 

## Keep track of paths

In each source file, maintain the up-to-date `this_file` record that shows the path of the current file relative to project root. Place the `this_file` record near the top of the file, as a comment after the shebangs, or in the YAML Markdown frontmatter.

## When you write Python

- Use `uv pip`, never `pip`
- Use `python -m` when running code
- PEP 8: Use consistent formatting and naming
- Write clear, descriptive names for functions and variables
- PEP 20: Keep code simple and explicit. Prioritize readability over cleverness
- Use type hints in their simplest form (list, dict, | for unions)
- PEP 257: Write clear, imperative docstrings
- Use f-strings. Use structural pattern matching where appropriate
- ALWAYS add "verbose" mode logugu-based logging, & debug-log
- For CLI Python scripts, use fire & rich, and start the script with

```
#!/usr/bin/env -S uv run -s
# /// script
# dependencies = ["PKG1", "PKG2"]
# ///
# this_file: PATH_TO_CURRENT_FILE
```

Work in rounds: 

- Create `PLAN.md` as a detailed flat plan with `[ ]` items. 
- Identify the most important TODO items, and create `TODO.md` with `[ ]` items. 
- Implement the changes. 
- Update `PLAN.md` and `TODO.md` as you go. 
- After each round of changes, update `CHANGELOG.md` with the changes.
- Update `README.md` to reflect the changes.

Ask before extending/refactoring existing code in a way that may add complexity or break things.

When you’re finished, print "Wait, but" to go back, think & reflect, revise & improvement what you’ve done (but don’t invent functionality freely). Repeat this. But stick to the goal of "minimal viable next version". Lead two experts: "Ideot" for creative, unorthodox ideas, and "Critin" to critique flawed thinking and moderate for balanced discussions. The three of you shall illuminate knowledge with concise, beautiful responses, process methodically for clear answers, collaborate step-by-step, sharing thoughts and adapting. If errors are found, step back and focus on accuracy and progress.

## After Python changes run:

```
fd -e py -x autoflake {}; fd -e py -x pyupgrade --py311-plus {}; fd -e py -x ruff check --output-format=github --fix --unsafe-fixes {}; fd -e py -x ruff format --respect-gitignore --target-version py311 {}; python -m pytest;
```

Be creative, diligent, critical, relentless & funny!