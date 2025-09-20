---
this_file: PLAN.md
---
# Abersetz Translation MVP Plan

## Project Overview
- **Goal**: Deliver a minimal yet reliable file translation toolkit (`abersetz`) that reuses mature translation engines, processes local files in batches, and exposes a Fire-based CLI mirroring a locate → chunk → translate → merge workflow.
- **Scope sentence**: Translate files between languages using reusable engines, storing config in platformdirs, and offering repeatable CLI + library APIs.

## Architecture & Key Decisions
- **Core modules** (all under `src/abersetz`):
  - `config.py`: platformdirs-backed config store for API secrets, engine defaults, and chunk sizing. Persists env var references plus direct values.
  - `engines.py`: thin wrappers for `translators`, `deep_translator`, and custom `hysf` / `ullm` engines built on `openai` + `tenacity`.
  - `pipeline.py`: file discovery, HTML detection, chunking (via `semantic-text-splitter`), translation orchestration, vocabulary hand-off logic.
  - `cli.py`: Fire command exposing translate command with recursion toggle, language args, engine selection, overwrite/save-vocabulary flags.
  - `__init__.py`: public API shortcuts.
- **Data flow**: gather files → derive chunker (plain vs HTML) → run translator engine per chunk (with vocabulary context) → merge & persist outputs while optionally saving vocabulary JSON.
- **Chunking**: use `semantic-text-splitter` `TextSplitter` + `MarkdownSplitter` depending on HTML detection; fallback to simple line chunker if library unavailable at runtime.
- **Vocabulary sharing**: capture `<output>` + optional `<vocabulary>` tags from engines supporting it (custom LLM pathways); merge dictionaries and include as `prolog` for subsequent chunks.
- **Configuration storage**: store YAML/JSON file under platformdirs user config; structure contains global defaults, per-engine overrides, secret references (`env` or `value`). Provide helper to resolve actual key at runtime.

## Dependencies and Justification
- `fire`: CLI scaffolding, minimal custom parsing.
- `rich`: Rich logging / status for CLI feedback.
- `loguru`: consistent structured logging with minimal setup.
- `translators`: provides many free translation engines, matches requirement.
- `deep-translator`: alternate provider set with file translation utility.
- `semantic-text-splitter`: high quality chunking respecting semantic boundaries.
- `platformdirs`: mandated config storage location.
- `openai`: official client for siliconflow + custom endpoints.
- `tenacity`: robust retry helper for API calls.
- `httpx`: optional for verifying configuration endpoints (used by custom engine for HEAD ping if needed).
- `pytest`, `pytest-cov`, `pytest-mock`: testing baseline (dev dependency already present but ensure usage).

## Risks & Mitigations
- **Network failures / rate limits**: wrap API calls with tenacity, allow dry-run translation engine for tests.
- **HTML detection accuracy**: implement heuristic (presence of tags) + allow forced mode; include tests for false positives.
- **Vocabulary parsing errors**: handle missing / malformed JSON gracefully, log warning, continue translation.
- **Chunk merging errors**: ensure deterministic join strategy; include newline handling tests.
- **Missing API keys**: prompt informative errors linking to config commands.

## Phase Breakdown
1. **Foundations & Config**
   - Define config schema dataclasses with validation.
   - Implement platformdirs persistence (read/write) & environment resolution logic.
   - Provide CLI helpers for inspecting stored config.
   - Tests: config read/write, env resolution fallback, default creation.

2. **File Discovery & Chunking**
   - Implement recursive globbing respecting include/exclude patterns (default: text extensions, optional `--recurse`).
   - HTML detection utility returning enum (`html`, `markdown`, `plain`).
   - Chunking orchestrator leveraging semantic-text-splitter with configurable max length.
   - Tests: detection heuristics, chunk sizing boundaries, ensures final concatenation stable.

3. **Engine Integrations**
   - Wrap `translators` + `deep-translator` for synchronous text translation.
   - Build custom `hysf` engine using OpenAI client hitting siliconflow endpoint with tenacity retry.
   - Build `ullm` engine that reads config-specified endpoint/model, handles vocabulary prolog & `<vocabulary>` parsing.
   - Provide fake/local engine for testing pipeline without network.
   - Tests: engine selection, request payload assembly, vocabulary merge, retry decorator behavior (mocked client).

4. **Pipeline Assembly**
   - Connect file iteration, chunk translation, vocabulary propagation, and output writing.
   - Support output directory vs overwrite; ensure directory creation.
   - Implement optional `--save-voc` to emit vocabulary JSON alongside output.
   - Tests: pipeline integration with stub engine, ensures file outputs, vocabulary persistence, error surfaces.

5. **CLI & Examples**
   - Expose Fire CLI command `abersetz translate` with options (`--engine`, `--from-lang`, `--to-lang`, `--recurse`, `--overwrite`, `--save-voc`, chunk overrides).
   - Provide CLI entrypoint in `pyproject` or console script mapping.
   - Create `examples/` containing sample source files, example config template, and README snippet showing CLI invocations.
   - Tests: CLI command executed via Fire (simulate using `CliRunner` or direct call) verifying argument wiring.

6. **Documentation & Verification**
   - Rewrite README with usage, engines, config, testing instructions.
   - Prepend README content into `CLAUDE.md`.
   - Update `TODO.md` and `WORK.md` (ongoing progress logs) as tasks progress.
   - Run full test suite + coverage; document results in `WORK.md`.

## Test Strategy Summary
- Unit tests for config, detection, chunker, vocabulary merge, engine payload generation.
- Integration test using stub engine to translate sample file end-to-end within tmp path.
- CLI smoke tests verifying Fire wiring.
- Keep coverage ≥80%; enforce via pytest-cov.

## Deliverables Checklist
- PLAN.md, TODO.md, README.md, CLAUDE.md updated.
- Source modules + tests with `this_file` headers.
- `examples/` folder with runnable demo (input + expected output + instructions).
- Updated `pyproject.toml` dependencies and console script entry.
- Passing `python -m pytest --cov` documented in WORK.md.

