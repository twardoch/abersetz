# Todo List — Task 111: Engine Selector Overhaul

Detailed requirements: [issues/111.md](issues/111.md). Full design in [TASKS.md](TASKS.md).

**One-sentence scope:** Replace the engine selector grammar with `engine[/subvariant]::provider`, expose a single `ls` discovery command, add a reusable job-JSON format, and split translation into `tr`/`tf`/`td` CLI verbs — used consistently everywhere.

## Phase 1 — Selector grammar (`selector.py`)
- [x] Define the 2-letter engine codes: `tr`, `dt`, `lm`, `ll`, `ml`, `gg`.
- [x] `parse_selector(str) -> Selector(engine, subvariant, provider, raw)`:
  - [x] New syntax: split on `::`; left = `engine[/subvariant]`, right = provider.
  - [x] Legacy syntax (no `::`): `engine[/provider]` mapped onto new model (back-compat).
  - [x] Map legacy aliases (`translators`, `deep-translator`, `lms`, `lmstudio`, `ullm`, `mthy`, `gemma`) onto the new codes.
- [x] `format_selector(Selector) -> str` canonical `engine[/subvariant]::provider`.
- [x] `slugify_selector(Selector) -> str` for output-suffix naming.
- [x] Keep `normalize_selector` / `resolve_engine_reference` working (delegate to new parser) so existing call sites and tests don't break.
- [x] Unit tests for every form in [tests/test_selector.py](tests/test_selector.py).

## Phase 2 — Engine factory routing
- [x] Rewrite `create_engine` to consume a parsed `Selector`.
- [x] `tr` → `TranslatorsEngine(provider)`; `dt` → `DeepTranslatorEngine(provider)`.
- [x] `lm` → `LmstudioEngine`, provider = model id.
- [x] `ll` → `LlmEngine`, provider = `endpoint:model` (reuse `resolve_model`).
- [x] `ml` → `LocalMlxEngine`, subvariant = family (`hy-mt2`→mthy / `gemma`), provider = path/alias.
- [x] `gg` → `LocalGgufEngine`, subvariant = family, provider = path/alias.
- [x] Map legacy `mthy/mlx`,`gemma/gguf` etc. onto `ml`/`gg` + family.
- [x] Tests in [tests/test_engines.py](tests/test_engines.py) (offline-safe).

## Phase 3 — Job JSON format (`job.py`)
- [x] Pydantic models: `JobEntry(selector, from_lang, to_lang, chunk_size, html_chunk_size, params, suffix)` and `Job(input, output_dir, entries[])`.
- [x] `suffix` defaults to `slugify_selector`.
- [x] `load_job(path|str) -> Job`, `job_to_dict`.
- [x] Build `TranslatorOptions` from a `JobEntry` (done inline in CLI/benchmark rather than a separate helper).
- [x] Tests in [tests/test_job.py](tests/test_job.py).

## Phase 4 — `ls` command (merges `engines` + `discover`)
- [x] `abersetz ls [selector_prefix]` lists engines / providers / models.
- [x] Fast for engine/provider listing (no API calls); only query provider model APIs / scan local disk when that engine subset is requested.
- [x] Wildcard support (`ll::*`, `tr::goog*`).
- [x] Cache slow results (API model lists, local scans) under config dir; `--force` bypasses cache.
- [x] `--job` emits an abersetz job-JSON skeleton for the matched combos.
- [x] Tests in [tests/test_ls.py](tests/test_ls.py).

## Phase 5 — Translation CLI verbs
- [x] `tr <text>` translates a string to stdout.
- [x] `tf <file>` single-file translation.
- [x] `td <dir>` directory-tree translation.
- [x] Each accepts `--job <json>` plus the existing inline options.
- [x] Keep old `translate`/`tr` behavior available where reasonable; update README.
- [x] Tests in [tests/test_cli.py](tests/test_cli.py).

## Phase 6 — Examples & benchmark
- [x] `examples/benchmark_prep.py`: runs `abersetz ls --job` over all combos → `examples/benchmark_job.json`.
- [x] Rewrite `examples/benchmark.py` to consume `benchmark_job.json` + input doc + output naming + JSON report path. **No `MODEL_PATHS` literal in benchmark.py.**
- [x] `examples/benchmark_run.sh`: poem → `benchmark_poem.json`, fontlab → `benchmark_fontlab.json`.
- [x] Update [tests/test_examples.py](tests/test_examples.py).

## Phase 7 — Wrap-up
- [x] `fd -e py -x uvx ruff ...` + `uvx hatch test` all green.
- [x] Update README.md, CHANGELOG.md, WORK.md, DEPENDENCIES.md.
