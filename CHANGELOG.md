---
this_file: CHANGELOG.md
---
# Changelog

All notable changes to abersetz will be documented in this file.

## [Unreleased]

### Fixed — test suite runs offline and deterministically
- `tests/conftest.py`: added a session-scoped autouse `_prefect_test_harness`
  fixture wrapping the suite in `prefect.testing.utilities.prefect_test_harness`.
  Previously, executing the Prefect `@flow` in
  `tests/test_htmladapt_twat.py::test_prefect_workflow_integration` started a
  temporary Prefect server that ran Alembic migrations against the developer's
  persistent `~/.prefect/prefect.db`. A DB left over from a different Prefect
  version aborted startup ("Can't locate revision identified by '79e7a60e43d8'"
  → "Application startup failed"), failing that test and corrupting pytest's
  summary output via Prefect's exit-time logging to a closed stream. The harness
  points Prefect at a throwaway temp database with correct migrations and runs
  in-process, so flows execute without a real server and the suite no longer
  depends on (or mutates) the user's Prefect state. The fixture degrades
  gracefully (yields) if Prefect is unavailable.
- Result: `uvx hatch test` is now self-contained and green — 249 passed,
  8 skipped (the 8 skips are pre-existing opt-in integration tests gated behind
  `ABERSETZ_INTEGRATION_TESTS=true`), 0 failures.

### Added — Wave 1 modernisation
- Created `src_docs/` MaterialX documentation tree with `mkdocs.yaml` (MkDocs
  Material config) and `src_docs/md/` Markdown sources:
  `index.md`, `installation.md`, `engines.md` (new "Choosing an engine"
  comparison table with rate limits and costs), `cli.md`, `configuration.md`,
  `api.md`, and `STYLE_GUIDE.md`.
- Added `tests/test_ml_engine.py`: 16 new hermetic smoke tests for the MLX
  local engine — language resolution, prompt building, model path resolution,
  alias table integrity, and non-existence of MarianMT (plan documentation
  clarification: `--engine ml/…` is the MLX backend, not MarianMT).
- Added `src_docs/site/` to `.gitignore` (MkDocs build output).
- Added `.gitignore` notes for `ruvector.db` and `llms.txt` (generated
  artifacts currently tracked; flagged for future `git rm --cached` cleanup).

### Changed
- CI (`push.yml` test matrix) now pins to Python 3.12 only (was 3.10/3.11/3.12).
  Keeps the matrix lean; `pyproject.toml` still allows Python ≥ 3.10 for
  package installs.

### Improved — docstrings and inline comments
- `TranslatorsEngine`: added docstring documenting cost (free), unofficial rate
  limits (~50–100 req/min), retry strategy, and privacy posture.
- `DeepTranslatorEngine`: added docstring with per-provider cost and rate-limit
  details (DeepL 5 req/s, Microsoft 1 000 req/min, etc.).
- `LlmEngine`: added docstring with cost table for common providers and a
  detailed inline comment on `_build_messages` explaining the XML-tag prompt
  structure, vocabulary continuity mechanism, and system-prompt design intent.
- `LocalMlxEngine`: added docstring covering cost, rate limits (none), platform
  requirements, model families (mthy, gemma), and HuggingFace download behaviour.
- `LocalGgufEngine`: added docstring covering platform support, CPU/GPU
  performance expectations, and recommended quantisation levels.
- `LmstudioEngine`: added docstring covering cost, privacy, prerequisites, and
  automatic daemon start-up behaviour.

### Added — Engine selector overhaul (issue 111)
- New selector grammar `engine[/subvariant]::provider` with six 2-letter engine codes (`tr`, `dt`, `lm`, `ll`, `ml`, `gg`) in `src/abersetz/selector.py`; legacy `engine/provider` form still parses. Includes `parse_selector`, `slugify_selector`, and `Selector`.
- New `src/abersetz/job.py`: Pydantic `Job`/`JobEntry` job-JSON format (selector + langs + chunk sizes + params + output suffix), `load_job`, `job_to_dict`.
- New `src/abersetz/listing.py`: `build_catalog` powering the unified `abersetz ls` command (merges old `engines` + `discover`). Fast for engine/provider listing; enumerates models (provider APIs / local disk scan) only when the prefix narrows to a model-bearing engine; caches slow results under the config dir with `--force` override; `--job` emits a job skeleton.
- New CLI translation verbs: `tr <text>` (string → stdout), `tf <file>`, `td <dir>`. Each accepts `--job` to translate with every job entry at once (per-suffix outputs / `selector<TAB>result` lines).
- `pipeline.translate_string()` for in-memory string translation.
- `create_engine` now understands the new `::` grammar directly (model id for `lm`, `endpoint:model` for `ll`, model path for `ml`/`gg`); legacy path unchanged.
- Rewrote `examples/benchmark.py` to consume a job-JSON file + input document + report path (no hard-coded `MODEL_PATHS`); added `examples/benchmark_prep.py` (generates `benchmark_job.json`) and `examples/benchmark_run.sh` (poem → `benchmark_poem.json`, fontlab → `benchmark_fontlab.json`).
- Added `pydantic>=2.0` as an explicit dependency.

### Fixed
- `tests/conftest.py` no longer hard-fails when the installed `twat_cache` build is broken; the `twat_cache` caching test skips gracefully when caching is unavailable.

### Added
- Added unified CLI entrypoint routing in `pyproject.toml` pointing `abersetz` to `abersetz.__main__:main` so that both `uvx abersetz` and `python -m abersetz` execute the same entry point.
- Added return type annotations and descriptive docstrings to all Fire CLI subcommands (`config`, `config show`, `config path`, `lang`) to enable clean `--help` synopses.
- Added `n_threads` option (CPU threads limit) parameter support to `AbersetzCLI.tr`, `TranslatorOptions`, `create_engine`, and `LocalGgufEngine` for local GGUF CPU threads tuning.
- Added smart language code and name resolution to `DeepTranslatorEngine` using `langcodes` to cleanly map codes/names (like `pl` or `polish`) to provider-supported identifiers (like `pl-PL`) without hardcoding mapping tables.
- Added destination existence checking to `examples/benchmark.py` to skip translation if the output file exists, with a new `--force` flag to override this behavior.
- Added dedicated local translation engine using the official `lmstudio` Python SDK (alias `lms`/`lmstudio`).
- Added optional dependency groups (`mlx`, `gguf`, `lms`, and `all`) with macOS platform markers to `pyproject.toml`.
- Added `examples/benchmark.py` speed benchmarking tool to compare translation engine throughput and accuracy across providers, with auto-discovery for all 7 local Hy-MT2 MLX/GGUF models and local LMStudio servers.
- Added `examples/README.md` explaining benchmark configuration, dry-runs, and option flags.
- Added support for local `Hy-MT2` translation models (MLX and GGUF backends) with automatic resolution of local/LMStudio paths.
- Added automatic model downloading from Hugging Face via `huggingface-hub` if not found locally.
- Added prompt-level terminology intervention support for `Hy-MT2` models.
- Added `huggingface-hub` production dependency.
- Added optional local MLX/GGUF engines for HY-MT and TranslateGemma via `mthy` and `gemma` selectors.
- Added `language-data` dependency to keep `langcodes` language-name lookups working in HYSF prompts.
- Added CLI regression tests covering target-language guardrails, JSON prolog/voc ingestion, and option propagation.
- Added CLI regression tests for include defaults and output directory resolution.
- Added `--include-community` flag to `abersetz setup` for opting into community/self-hosted engines.
- Added `pytest-asyncio` development dependency to support testing of async code.
- Added local model discovery module (`LocalModelFinder` in `src/abersetz/providers/llm/local_discovery.py`) that portable-scans HuggingFace, Ollama, LM Studio, Pinokio, and GPT4All directories for LLM weights.
- Added `discover` subcommand to the main `abersetz` CLI, allowing users to scan and display local system models directly from the command line.
- Added support for passing GGUF/MLX inference parameters (`n_gpu_layers`, `n_ctx`, `max_tokens`) as CLI flags and options in `tr` and propagating them dynamically to the engines.
- Added uppercase option aliases for `tr` (`Overwrite`, `Temperature`, `Vocabulary`) and `validate` (`Selectors`, `Text`) to avoid single-letter option collisions under python-fire (letting `-O`, `-T`, `-V`, and `-S` map cleanly alongside lowercase parameters).
- Updated `__main__.py` to use `cli_fast` to speed up module-level version and help lookups.


### Changed
- Removed the `my_memory` translation provider from the `deep-translator` providers list (both engine catalog and provider classes) due to its highly restrictive 500-character text limit that fails typical benchmark translations.
- Rejected the discontinued `tencent/Hunyuan-MT-7B` SiliconFlow model in `engines.py` and raised a configuration update suggestion asking users to migrate to `Qwen/Qwen2.5-7B-Instruct`.
- Removed `tencent-Hunyuan-MT-7B` (`hysf`/`hy` engine family) support as it was discontinued by SiliconFlow.
- Updated the default model and temperature for SiliconFlow-based `ullm` defaults to `Qwen/Qwen2.5-7B-Instruct` and `0.3`.
- Updated default engine priorities in setup to prefer SiliconFlow/ULLM over the removed Hunyuan engine.
- Updated validation sort order to position `lms` before `ll` (ULLM).
- Updated `examples/benchmark.py` and `README.md` to remove `hysf` and incorporate `lms` engine.
- Updated `examples/benchmark.py` to rely on the published `abersetz` package via its `uv` script shebang dependencies block instead of manually modifying `sys.path` to target local source files.
- Rewrote `examples/` directory to keep only `./examples/data/` source files while deleting legacy scripts.
- Rewrote `tests/test_examples.py` to cover the new benchmark runner.
- Updated `get_engine_descriptor` helper in the benchmark runner to resolve short selectors to canonical config keys for correct descriptor output.
- Refactored all translation engines/providers into separate modules inside `src/abersetz/providers/` for a cleaner architecture.
- Removed support for legacy `Hy-MT1.x` models (which now raise an `EngineError` if loaded locally).
- Removed assistant preamble/outro text from `README.md`.
- Removed transient one-off files: `update_*.py` refactoring scripts, `md.txt`, and `translation_report.json`.
- Updated user `config.toml` to align deep-translator and translators provider lists with current codebase catalog (removing obsolete `my_memory` from deep-translator, and ensuring `libre` and `linguee` are correctly configured).

### Fixed
- Fixed `abersetz discover` LM Studio handling to use grouped `lms ls --json` model records when the CLI is available, while preserving filesystem scanning fallback when LM Studio is absent.
- Fixed duplicate client configuration conflict in `LmstudioEngine` by catching and handling the ValueError from `configure_default_client` gracefully.
- Fixed a cache key serialization error in `pipeline.py` by safely extracting string model names instead of passing full loaded model weight objects (which exceeded SQLite capacity and caused indexing errors).
- Fixed a log formatting `IndexError` in the `twat_cache` diskcache logger by removing formatted variables from `logger.exception` calls.
- Fixed CLI log noise by defaulting loguru to `WARNING` level on package import, suppressing early diagnostic `DEBUG` messages (like `redis not available`) from downstream libraries.
- Silenced raw diagnostic print calls (`CACHE_KWARGS` and `[FUNCTOOLS] KEY`) in `twat_cache`'s diskcache and functools engines by converting them to standard `logger.debug` statements.
- Configured local workspace dependencies (`htmladapt`, `twat`, `twat-cache`, `twat-task`) as editable in `pyproject.toml` so that environment updates align instantly with local repository edits.
- Silenced import-time print and warning noise in `cli.py` by redirecting stdout/stderr to `/dev/null` during heavy module imports (such as `pipeline.py` which transitively imports `twat_cache`), ensuring that CLI commands are completely clean of diagnostic print pollution.
- Fixed local MLX model directory resolution to return the parent directory containing the model weights rather than the individual file path, ensuring compatibility with `mlx_lm.load`.
- Fixed python-fire help program name display by specifying `name="abersetz"` and `name="abtr"` inside the `fire.Fire()` calls to ensure clean synopsis outputs.
- Cleaned up import statement sorting and non-top-level import warnings (E402/F823) in engines, pipeline, and discovery modules.
- Fixed exception chaining (B904) in `LmstudioEngine` and `src/abersetz/pipeline.py`.
- Fixed unused loop control variables (B007) in `DeepTranslatorEngine._resolve_lang`.
- Fixed `deep-translator` engine initialization by automatically mapping standard 2-letter language codes to their region-specific equivalents for providers with stricter language requirements (e.g. mapping `en` to `en-GB` and `pl` to `pl-PL` for `MyMemoryTranslator`).
- Fixed PyPI publishing flow in `publish.sh` by cleaning the `dist/` directory before building the release package, preventing local development version files from being uploaded and rejected by PyPI due to local version identifier restrictions.
- Fixed `test_cli_setup_forwards_flags` to support `include_community` keyword argument.
- Silenced useless expression warning B018 in `tests/test_package.py`, and refactored try-except-pass block in `src/abersetz/config.py` using `contextlib.suppress`.


## [1.0.19] - 2025-09-21

### Highlights
- Short engine selectors are the default across the CLI, configuration, and engine catalog while keeping legacy aliases working transparently.
- New `abersetz validate` command reuses the engine pipeline to smoke-test configured selectors and slots into the setup wizard’s post-install checks.
- Refreshed docs, richer examples, and a 98% coverage regression suite backed by clean mypy and bandit runs.

### Added
- Introduced `src/abersetz/validation.py` and the `abersetz validate` CLI command for quick engine verification with rich table output.
- Extended the setup wizard to persist validation results, surface pricing hints, and auto-map discovered API keys to their short selectors.
- Added validation/reporting utilities such as `examples/validate_report.sh` and `translation_report.json` to demonstrate end-to-end health checks.
- Delivered new regression suites covering engine catalog discovery, setup wizard flows, validation pipelines, CLI Fire entrypoints, and advanced examples.

### Changed
- Normalised selector handling to prefer `tr/*`, `dt/*`, `ll/*`, and `hy` forms with automatic migration of legacy `translators/*` and `deep-translator/*` values.
- Updated `_build_options_from_cli` to accept `Path` objects, enforce target-language requirements, and hydrate JSON `prolog`/`voc` inputs consistently.
- Refined engine catalog rendering, configuration helpers, and setup wizard messaging to highlight credential needs and community/paid tiers.

### Fixed
- Resolved pipeline chunk-size fallbacks so engines supply sizes when configuration defaults collapse to zero, covering both plain text and HTML flows.
- Hardened setup wizard endpoint probing and validation logging to survive missing keys and transient HTTP failures.
- Eliminated the final mypy diagnostics by tightening optional typing around CLI outputs and external provider dumps.

### Documentation
- Refreshed `README.md`, reference docs, and example notebooks to describe short selectors, validation usage, and setup wizard improvements.
- Updated agent notebooks (`CLAUDE.md`, `GEMINI.md`, `LLXPRT.md`, `QWEN.md`) and examples to reflect the new validation workflow and selector syntax.

### Testing & Quality
- Test suite: `python -m pytest -xvs` reports 180 passed / 8 skipped with 98% coverage.
- Static analysis: `uvx mypy .` is clean (annotation-unchecked warning only); `uvx bandit -r .` reports Low-severity issues confined to intentional test `assert`s and backup fallbacks.
- Routine cleanup removes transient caches (`.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.benchmarks`, `.coverage`) after every verification sweep.

## [0.1.0] - 2025-01-20

### Added
- Initial release of abersetz - minimalist file translator
- Core translation pipeline with locate → chunk → translate → merge workflow
- Support for multiple translation engines:
  - translators library (Google, Bing, etc.)
  - deep-translator library (DeepL, Google Translate, etc.)
  - Custom hysf engine using Siliconflow API
  - Custom ullm engine for LLM-based translation with voc management
- Automatic file discovery with recursive globbing and include/xclude filters
- HTML vs plain-text detection for markup preservation
- Semantic chunking using semantic-text-splitter for better context boundaries
- voc-aware translation pipeline with JSON voc propagation
- Configuration management using platformdirs for portable settings
- Environment variable support for API credentials
- Fire-based CLI with rich console output
- Comprehensive test suite with 91% code coverage
- Example files demonstrating usage

### Fixed
- Fixed pyproject.toml configuration for modern uv/hatch compatibility
- Updated dependency group configuration to use standard [dependency-groups]
- Fixed type annotations to use modern Python union syntax (|)

## [0.1.1] - 2025-01-21

### Changed
- Renamed CLI main command from `translate` to `tr` for brevity
- Added `abtr` console script as direct shorthand for `abersetz tr`
- Improved CLI help output by instantiating the Fire class correctly
- Reduced logging and rich output to minimum for cleaner interface
- Simplified CLI output to just show destination files

### Added
- Version command (`abersetz version`) to display tool version
- Language code validation with silent handling of non-standard codes

### Fixed
- Fixed Fire CLI to properly expose available commands in help output
- Updated test suite to match renamed CLI command
- Fixed deep-translator retry test by properly mocking the provider

### Improved
- Better error handling for malformed config files with automatic backup
- Added retry mechanisms with tenacity for all translation engines
- Created comprehensive integration tests with skip markers for CI

### Technical Details
- Python 3.10+ support
- Semantic chunking with configurable sizes per engine
- Offline-friendly dry-run mode for testing
- Optional voc sidecar files with --save-voc flag
- Retry logic with tenacity for robust API calls
