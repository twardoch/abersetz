---
this_file: PLAN.md
---
# Abersetz Evolution Plan (Issue #200)

## Scope (One Sentence)
Deliver a responsive translation CLI that defaults to short engine selectors, validates every configured engine end-to-end, and ships with polished docs, examples, and tests that make abersetz easy to adopt and extend.

## Guiding Principles
- Preserve backward compatibility via aliases while promoting the new short selector format (`tr/google`, `dt/deepl`, `ll/default`, etc.).
- Prefer existing, battle-tested packages (`translators`, `deep-translator`, httpx, rich) over custom reinventions.
- Every new feature gains automated tests, documentation, and examples before calling it done.
- Prioritize fast feedback: run targeted pytest suites and smoke the CLI for every phase.

## Phase 1 – Engine Selector Simplification *(Completed)*
**Summary**: Short selector support landed in `config.py`, `engine_catalog.py`, and CLI surfaces. Legacy names are normalized transparently, tests cover migrations, and generated configs now emit `tr/*` / `dt/*` selectors by default.

## Phase 2 – CLI UX Refresh *(Completed)*
**Summary**: CLI accepts short selectors across commands, `abersetz engines` renders the condensed table with configuration markers, and `lang` lists popular targets using `langcodes`. Snapshot-style Fire runner tests are in place for the engines output.

## Phase 3 – Engine Validation Command *(Completed)*
**Summary**: A new `validation.py` module powers `abersetz validate` and the post-setup health check. The command translates a short sample per selector, displays results in a rich table, and ships with exhaustive unit tests using stub engines.

## Phase 4 – Auto-Configuration & Engine Research Enhancements
**Goals**: Broaden provider awareness and produce smarter defaults using the research in `external/` and recent API trends.
- Automate provider metadata extraction from `external/translators.txt`, `external/deep-translator.txt`, and current API research (Google, Azure, AWS, DeepL, LibreTranslate, OpenRouter, etc.) so discovery stays accurate without manual updates.
- Keep pricing/tier hints fresh by syncing the new metadata into setup output (including highlighting free/community tiers).
- Add structured hints for optional packages the user might need (e.g., install `translators[google]`)
- Allow users to opt into community/self-hosted engines like LibreTranslate with a `--include-community` flag.
- Document every provider addition in `DEPENDENCIES.md` with justification referencing external sources.

## Phase 5 – Documentation, Examples, and Tests
**Goals**: Make abersetz feel “vibrant” with real-world material and guardrails.
- Update `README.md`, `CLAUDE.md`, and `CHANGELOG.md` with the new selector format, validation workflow, and configuration guidance.
- Expand `WORK.md` logging template to capture validation runs and outcomes per session.
- Add at least three runnable examples in `examples/`: (1) Multi-file translation with mixed engines, (2) Validation summary report, (3) Config diff before/after setup.
- Create user-facing walkthrough in `docs/` (or extend README) describing how to pick engines based on cost, drawing on the external research completed above.
- Ensure tests cover: selector normalization, CLI output, validation command, setup integration, and documentation link checks (using `pytest` or `pytest-regressions`).
- 2025-09-21 Action Items *(Completed 2025-09-21)*:
  - Added regression tests for `config_dir` fallback and `resolve_credential` logging (see `tests/test_config.py`).
  - Covered `_filter_available` deduping plus `collect_translator_providers` import failure with new cases in `tests/test_engine_catalog.py`.
  - Extended `tests/test_cli.py` to assert `_collect_engine_entries` respects `family` and `configured_only` filters, including long-form family selectors.

## Maintenance Sprint – Reliability Polish *(Completed 2025-09-21)*
**Objective**: Raise confidence in existing helper utilities by tightening coverage for configuration defaults, enforcing typed report generation, and locking down parallel translation behaviour.

### Task 1 – Cover setup discovery and default fallbacks
- **Problem**: `setup.py` still has uncovered lines (221, 262, 286, 471), leaving the endpoint testing branch, fallback logging, and empty-engine return path unverified.
- **Approach**: Extend `tests/test_setup.py` with focused cases to (a) drive `_test_endpoints` through the base-url path, (b) force `_test_single_endpoint` to hit the unknown JSON branch and verbose failure logging, and (c) assert `_select_default_engine` returns `None` when no engines exist.
- **Tests**: `python -m pytest tests/test_setup.py -k "test_endpoints or test_test_single_endpoint or select_default_engine" -xvs`; full suite for regression.
- **Success Criteria**: Coverage report no longer lists `setup.py` lines 221/262/286/471 as missed while preserving existing behaviour.
- **Status**: Completed 2025-09-21 11:03 UTC — `tests/test_setup.py` cases now cover API-provider endpoint flow, verbose failure logging, and empty engine fallback (setup.py shows 100% coverage).

### Task 2 – Harden `TranslationWorkflow.generate_report` typing
- **Problem**: `examples/advanced_api.py` triggers mypy "object is not indexable" errors and keeps report aggregation loosely typed.
- **Approach**: Introduce lightweight `TypedDict`/dataclass helpers to describe report structure, replace untyped dict juggling with explicit updates, and ensure tests confirm error aggregation and per-language stats.
- **Tests**: `python -m pytest tests/test_examples.py -k "translation_workflow" -xvs`; `uvx mypy examples/advanced_api.py tests/test_examples.py`.
- **Success Criteria**: Mypy no longer flags lines 68-79/307; report output stays identical.
- **Status**: Completed 2025-09-21 11:03 UTC — `TranslationWorkflow.generate_report` now uses typed helpers; `uvx mypy .` dropped the union-attr diagnostic and regression tests confirm identical JSON output.

### Task 3 – Add `ParallelTranslator` behaviour tests
- **Problem**: `examples/advanced_api.py` coverage sits at 47% with async comparison utilities untested, risking regressions in demo code.
- **Approach**: Mock `create_engine` to supply stub engines returning deterministic translations and one raising an exception; assert `compare_translations` surfaces both successes and failures.
- **Tests**: `python -m pytest tests/test_examples.py -k parallel_translator -xvs`; smoke the async helper under coverage.
- **Success Criteria**: Coverage for `examples/advanced_api.py` climbs (target ≥70%), verifying both success and error handling paths for the async translator.
- **Status**: Completed 2025-09-21 11:03 UTC — new async and example-facing tests drive coverage to 88% with deterministic stubs for success/failure flows.

## Maintenance Sprint – Coverage Hardening *(Completed 2025-09-21)*
**Goal**: Close remaining high-signal coverage gaps in CLI/engine helpers to reinforce translation and setup reliability without adding new surface area.

### Task A – Cover CLI result rendering output *(done)*
- Added `test_render_results_lists_destinations` capturing a wide-console `Console` sink to assert both destination paths appear in the render output, raising `src/abersetz/cli.py` line coverage for `_render_results` to 100%.
- Reused existing `TranslationResult` dataclass without introducing dependencies; ensures future CLI `tr` flows list translated files reliably.

### Task B – Cover translators single-string provider configuration *(done)*
- Added `test_collect_engine_entries_accepts_single_provider_string` to verify configs defining only `"provider"` mark the provider as configured and discoverable, exercising lines 134-135 of `src/abersetz/cli.py`.
- Retained existing fixture coverage for list-based providers to guard dedupe logic and avoid regressions in config migrations.

### Task C – Cover HTML-specific chunk sizing logic *(done)*
- Added `test_engine_base_chunk_size_prefers_html_then_plain` to ensure `EngineBase.chunk_size_for` prefers `html_chunk_size` when present and falls back to `chunk_size`/`None`, covering lines 81-83 of `src/abersetz/engines.py`.
- Validates pipeline fallback semantics without any new abstractions.

### Verification
- `python -m pytest -k "render_results or collect_engine_entries or chunk_size_for" -xvs`
- `python -m pytest -xvs`
- `python -m pytest --cov=. --cov-report=term-missing`
- `uvx mypy .`
- `uvx bandit -r .`

## Micro Maintenance – CLI Shell Coverage *(Completed 2025-09-21)*
**Objective**: Close the remaining uncovered CLI wrapper lines so Fire entrypoints, setup passthrough, and pipeline error surfacing stay regression-proof without inflating scope.

- **Task: Guard translation error reporting** *(done — `tests/test_cli.py::test_cli_translate_reports_pipeline_error`)*
  - Patched `translate_path` via `monkeypatch` to raise `PipelineError` and asserted `[red]...[/red]` console output prior to re-raising. Covered `cli.py:373-375`.
  - Verification: `python -m pytest tests/test_cli.py -k pipeline_error -xvs` plus full suite; `cli.py` coverage climbed to 96%.

- **Task: Exercise setup wrapper** *(done — `tests/test_cli.py::test_cli_setup_forwards_flags`)*
  - Mocked `setup_command` to capture arguments ensuring `AbersetzCLI.setup` forwards flags intact, covering `cli.py:435`.
  - Verification: Targeted pytest run plus full suite; no dependencies added.

- **Task: Verify Fire entrypoints** *(done — `tests/test_cli.py::test_cli_main_invokes_fire`, `...::test_cli_abtr_main_invokes_fire_with_tr`)*
  - Patched `fire.Fire` to capture invocations from `main()`/`abtr_main()` verifying callables, covering `cli.py:464` and `cli.py:474`.
  - Verification: Targeted pytest run plus full suite; no new dependencies.

## Maintenance Sprint – Config & CLI Reliability *(Completed 2025-09-21)*
**Objective**: Close uncovered branches in engine catalog and configuration helpers to keep short selector UX deterministic.

- **Task 1: Cover `ConfigCommands.show` and `.path`**
  - Implementation: Extended `tests/test_cli.py::test_cli_config_commands_show_and_path` to seed a temp config directory, call `ConfigCommands().show()`, parse the TOML, and assert `.path()` resolves to the injected location.
  - Verification: `python -m pytest tests/test_cli.py -k "config_commands" -xvs`, full suite, and coverage run (`python -m pytest --cov=. --cov-report=term-missing`).

- **Task 2: Cover single-provider branches in `_collect_engine_entries`**
  - Implementation: Added `tests/test_cli.py::test_collect_engine_entries_string_branches` exercising string-only `providers` and non-dict `profiles`, asserting selectors `tr/bing`, `dt/deepl`, `ll/default`, and `hy` report `configured=True`.
  - Verification: Targeted pytest invocation (`python -m pytest tests/test_cli.py -k "string_branches" -xvs`) plus full suite with coverage.

- **Task 3: Exercise recursive credential resolution**
  - Implementation: Added `tests/test_config.py::test_resolve_credential_recurses_into_stored_secret` to clear env vars, ensure recursion traverses stored credentials, and capture log output for the missing env debug message.
  - Verification: `python -m pytest tests/test_config.py -k recurses -xvs`, full suite, coverage, mypy, and bandit.

## Phase 6 – Release Readiness
**Goals**: Ship confidently with verifiable quality.
- Run `python -m pytest --cov=. --cov-report=term-missing` targeting ≥90% coverage for touched modules.
- Status: coverage sits at 91% as of 2025-09-21; maintain ≥90% when new features land.
- Execute manual smoke tests: `abersetz engines`, `abersetz validate`, `abersetz setup --non-interactive`, and a sample `abersetz tr` flow using faked engines.
- Prepare release notes summarizing selector transition, validation command, and provider updates.
- Tag version bump once manual verification passes and ensure packaging metadata references the new docs.

## Dependencies & External References
- Continue using `translators` and `deep-translator` for traditional MT; reference `external/translators.txt` and `external/deep-translator.txt` for supported provider lists.
- Lean on `httpx`, `tenacity`, `rich`, and `loguru` already in the project—no new heavy dependencies unless unavoidable.
- Monitor provider docs cited in the Perplexity research (Google, Azure, AWS, DeepL, Translate.com, LibreTranslate) when refining setup hints.

## Timeline & Checkpoints
1. **Week 1**: Complete Phases 1–2 (selector normalization, CLI refresh) with tests.
2. **Week 2**: Deliver Phase 3 validation command and integrate with setup, plus accompanying tests.
3. **Week 3**: Finish provider research updates and documentation/examples (Phases 4–5).
4. **Week 4**: Conduct release readiness sweep (Phase 6), run full test matrix, and publish release.

## Exit Criteria
- CLI displays only short selectors and accepts both short and legacy forms.
- `abersetz validate` reliably checks each engine and is invoked during setup.
- Documentation, examples, and tests reflect the new workflow.
- QA checklist (automated + manual) executed with recorded results in `WORK.md`.

## Maintenance Sprint – Coverage & Docs
- **Expand validation coverage** *(Completed 2025-09-21 — `validation.py` now 100% covered)*: Add focused tests for `_append_selector`, `_extract_providers`, and `_selectors_from_config` branches (include-defaults toggle, ullm fallback) to push `validation.py` ≥95% coverage.
- **CLI validation tests** *(Completed 2025-09-21 — selector parsing verified in `tests/test_cli.py`)*: Extend `tests/test_cli.py` to exercise `AbersetzCLI.validate` and `AbersetzCLI.lang` flows using stub engines to bump `cli.py` coverage above 90% and catch regressions.
- **Documentation refresh** *(Completed 2025-09-21 — validation guidance added to CLI + configuration docs)*: Update `docs/cli.md` (and cross-link in `docs/configuration.md`) with guidance for limiting selectors during validation, showcasing `--selectors`/`--include-defaults` to avoid long offline runs.

## Maintenance Sprint – CLI Reliability Tune-Up
- **Exercise parsing helpers via tests** *(Completed 2025-09-21 — coverage in tests/test_cli.py)*: Add focused unit tests for `_parse_patterns` (None, comma-separated string, tuple inputs) and `_load_json_data` (inline JSON vs. file path) to prevent regressions in selector/pattern handling.
- **Cover console rendering fallbacks** *(Completed 2025-09-21 — see tests/test_cli.py)*: Write tests capturing `_render_engine_entries([])` and `_render_validation_entries([])` to assert the user guidance strings, ensuring CLI behaves gracefully when configurations are empty.
- **Hit provider-aggregation branches** *(Completed 2025-09-21 — tests plus `_collect_engine_entries` fix)*: Construct stub configs feeding single `provider` strings (vs. list) and ullm profiles so `_collect_engine_entries` traverses every branch, and update tests to assert selectors differ when `configured_only` or `family` filters are applied.

## Maintenance Sprint – Configuration & Catalog Hardening *(Completed 2025-09-21)*
- **Task: Guard Defaults/EngineConfig fallbacks** *(Completed 2025-09-21 — tests/test_config.py)*  
  - *Outcome*: Added regression tests for `Defaults.from_dict(None)` and `EngineConfig.from_dict(name, None)`, confirming defaults remain intact when optional sections are stripped. Coverage for `src/abersetz/config.py` climbed from 94% to 97%.  
  - *Verification*: `python -m pytest tests/test_config.py -k "defaults_from_dict or engine_config_from_dict" -xvs` plus full suite; all pass.
- **Task: Strengthen Credential conversion coverage** *(Completed 2025-09-21 — tests/test_config.py)*  
  - *Outcome*: Extended credential tests to assert optional field serialization and to lock in the `TypeError` raised for unsupported payload types. Prevents regressions when validating user supplied credentials.  
  - *Verification*: `python -m pytest tests/test_config.py -k "credential_to_dict or credential_from_any" -xvs` and full-suite run.
- **Task: Cover deep translator provider aggregation** *(Completed 2025-09-21 — tests/test_engine_catalog.py)*  
  - *Outcome*: Ensured `collect_deep_translator_providers(include_paid=True)` returns deterministic, duplicate-free lists with paid providers appended. `engine_catalog.py` coverage rose to 95%.  
  - *Verification*: `python -m pytest tests/test_engine_catalog.py -k "deep_translator_providers" -xvs` and overall suite.

## Maintenance Sprint – Quality Guardrails (Completed 2025-09-21)
- **Task 1: Offline integration coverage for `translate_path`** *(Completed 2025-09-21 — see `tests/test_pipeline.py::test_translate_path_handles_mixed_formats`)*
  - Objective: Raise coverage for the translation pipeline by exercising the happy-path file walk with stub engines, ensuring we catch regressions in include/exclude handling and output directory creation (current gap: `tests/test_integration.py` covers only 24%).
  - Implementation: Added a mixed-format test that drives `translate_path` across TXT and HTML fixtures with the `DummyEngine`, asserting destination locations, normalized selectors, and preserved format metadata.
  - Verification: `python -m pytest tests/test_pipeline.py -k mixed_formats -xvs` then full suite confirmed behaviour; pipeline coverage climbed to 96%.
- **Task 2: Harden Optional[str] handling in `examples/basic_api.py`** *(Completed 2025-09-21 — guarded via `format_example_doc` helper and `tests/test_examples.py`)*
  - Objective: Eliminate runtime `AttributeError` and mypy warnings (`Item "None" has no attribute "strip"`) by guarding optional user inputs before calling `.strip()` or similar operations.
  - Implementation: Introduced `format_example_doc` helper with safe fallback messaging and updated CLI output to rely on it; added protocol-driven loader test ensuring None docs are handled gracefully.
  - Verification: `python -m pytest tests/test_examples.py -xvs` plus full suite; mypy on the module now avoids union-attr complaints (remaining missing-stub errors documented in WORK.md).
- **Task 3: Stabilize setup credential typing** *(Completed 2025-09-21 — see `tests/test_setup.py::test_generate_config_uses_fallbacks`)*
  - Objective: Reduce `uvx mypy .` noise by fixing `tests/test_setup.py:580` (`Credential | None` attribute access) and related optional-handling in setup helpers so None cases are explicitly guarded.
  - Implementation: Added explicit guard before dereferencing the `ullm` credential in the setup test to narrow the type and better document the expectation.
  - Verification: `python -m pytest tests/test_setup.py -k generate_config_uses_fallbacks -xvs`; mypy union-attr warning cleared though missing third-party stubs still block a clean run.

## Maintenance Sprint – Coverage Polish II *(Completed 2025-09-21)*
- **Task 1: Guard examples CLI dispatch**
  - Outcome: Added `test_basic_api_cli_dispatch_runs_requested_example` which executes the module as `__main__` with a stubbed translator; `examples/basic_api.py` now hits 100% coverage and CLI dispatch regressions surface immediately.
  - Verification: `python -m pytest tests/test_examples.py -k cli_dispatch -xvs` then full suite; output confirmed stub execution without the usage banner.
- **Task 2: Validate chunk_text fallback paths**
  - Outcome: Fresh tests cover the empty-input guard and forced `ImportError` fallback, pushing `chunking.py` to 100% coverage and proving graceful degradation without `semantic_text_splitter`.
  - Verification: `python -m pytest tests/test_chunking.py -k "blank or fallback" -xvs` plus full suite; fallback slices matched expectations.
- **Task 3: Assert __getattr__ rejects unknown exports**
  - Outcome: Regression test guarantees typos raise `AttributeError` while repeated access returns the cached pipeline export, preventing silent import failures.
  - Verification: `python -m pytest tests/test_package.py -k getattr -xvs` followed by full suite.

## Maintenance Sprint – Coverage Polish III *(Completed 2025-09-21)*
- **Task 1: Exercise deep-translator string provider branch**
  - Outcome: Added `test_collect_engine_entries_handles_deep_translator_string_providers` to assert `dt/libre` is emitted and marked configured when `providers` is configured as a string, bringing `_collect_engine_entries` to 100% coverage.
  - Verification: `python -m pytest tests/test_cli.py -k deep_translator_string -xvs`, followed by the full suite.
- **Task 2: Round out EngineConfig serialization**
  - Outcome: Added `test_engine_config_to_dict_includes_optional_fields` ensuring `chunk_size`, `html_chunk_size`, and nested credentials survive serialization, covering the previously missed optional-field branches.
  - Verification: `python -m pytest tests/test_config.py -k engine_config_to_dict -xvs`, plus the full suite.
- **Task 3: Normalize selectors for null/blank inputs**
  - Outcome: Extended `tests/test_engine_catalog.py` with guards for `None`, whitespace-only strings, and empty-base selectors so normalization behaviour stays regression-proof.
  - Verification: `python -m pytest tests/test_engine_catalog.py -k normalize_selector -xvs`, then the full suite.

## Maintenance Sprint – Reliability Boost (Completed 2025-09-21)
- **Task: Enforce pipeline read-permission safeguards** *(tests/test_pipeline.py::test_translate_path_errors_on_unreadable_file)*
  - Outcome: Simulated a zero-permission file on POSIX systems and confirmed `translate_path` raises `PipelineError` with the offending path in the message. Test gated on Windows to avoid chmod inconsistencies. Verified with `python -m pytest tests/test_pipeline.py -k unreadable -xvs`.

- **Task: Exercise `_persist_output` write-over & voc paths** *(tests/test_pipeline.py::test_translate_path_write_over_updates_source`, `..._dry_run_skips_io`)*
  - Outcome: Validated write-over updates the original file and emits a `.voc.json` when requested, while dry runs skip filesystem writes entirely. Ensures coverage of `_persist_output` branches. Verified with targeted pytest invocations and full-suite run.

- **Task: Mock example flows for coverage** *(tests/test_examples.py suite)*
  - Outcome: Replaced real translations with stub results across example functions and CLI usage path, boosting `examples/basic_api.py` coverage to 98% and guaranteeing documentation examples remain executable without network access. Verified via `python -m pytest tests/test_examples.py -xvs` and coverage summary.

## Maintenance Sprint – Engine Factory Reliability *(Completed 2025-09-21)*
- **Task 1: Harden `_build_llm_engine` error handling**
  - Outcome: Added regression tests asserting `EngineError` for missing model definitions and credentials, proving factories fail fast rather than constructing misconfigured engines. Covered via `tests/test_engines.py::test_build_llm_engine_without_model_raises_engine_error` and `..._without_credential_raises_engine_error`.
  - Verification: `python -m pytest tests/test_engines.py -k "llm_engine_without" -xvs` plus full suite.

- **Task 2: Verify `_select_profile` and profile resolution**
  - Outcome: Extended engine tests to exercise default profile selection, no-profile fallback, and error handling for unknown variants, lifting coverage across lines 356-363.
  - Verification: `python -m pytest tests/test_engines.py -k select_profile -xvs` and project-wide test sweep.

- **Task 3: Cover OpenAI client construction and unsupported selectors**
- Outcome: Added tests for `_make_openai_client` base URL logic and `create_engine` unsupported-engine guard, ensuring new selectors cannot bypass validation and clients honor configured endpoints.
  - Verification: `python -m pytest tests/test_engines.py -k "openai_client or custom" -xvs` followed by full suite.

## Maintenance Sprint – Reliability Guard IV *(Completed 2025-09-21)*
**Outcome**: Closed critical coverage gaps in credential resolution, pipeline warnings, and LLM payload parsing without expanding surface area.

- **Task 1: Cover `resolve_credential` null and chained secrets**
  - Added `tests/test_config.py::test_resolve_credential_returns_none_for_null_reference` and `...::test_resolve_credential_reuses_stored_alias_object`, ensuring credential-less payloads shortcut to `None` and stored alias recursion hits the terminal fallback branch (line 322).
  - Verified via `python -m pytest tests/test_config.py -k "resolve_credential_returns_none or resolve_credential_reuses" -xvs` plus the full suite.

- **Task 2: Warn on oversized input in pipeline**
  - Introduced `tests/test_pipeline.py::test_translate_path_warns_on_large_file`, monkeypatching `Path.stat` to emulate an 11MB document and asserting the loguru warning while `translate_path` still succeeds.
  - Confirmed with `python -m pytest tests/test_pipeline.py -k warns_on_large_file -xvs` and the full suite; `src/abersetz/pipeline.py` now reports 100% coverage.

- **Task 3: Exercise LLM payload parsing fallbacks**
  - Extended `tests/test_engines.py` with `_make_llm_engine` helper and new cases covering payloads without `<voc>`, malformed JSON, non-dict payloads, plus a missing configuration guard for `create_engine("tr/google")` when `translators` config is absent, lifting `src/abersetz/engines.py` to 98% coverage.
  - Verified using `python -m pytest tests/test_engines.py -k "parse_payload or missing_selector" -xvs` alongside the full test run.

## Maintenance Sprint – Coverage Guard V *(Completed 2025-09-21)*
**Objective**: Eliminate the remaining uncovered defensive branches in `setup.py` and `engines.py` so setup-time diagnostics and engine factories behave predictably even under misconfiguration.

**Current Gaps & Risks**
- `src/abersetz/engines.py` still leaves HTML translation path (line 103), deep-translator provider rejection (line 158), and `_build_hysf_engine` credential guard (line 346) untested. Without regression tests these guards could regress silently, breaking HTML translations or masking credential issues.
- `src/abersetz/setup.py` misses coverage for provider discovery enrichments (line 189), endpoint probing fallbacks for dict/list payloads (lines 258-261), verbose progress logging (lines 282-285), and default engine fallback logic (lines 451-459). These paths ensure accurate hints when users run `abersetz setup`.
- Previous research (pytest-httpx / respx) confirmed we can emulate HTTPX responses without network calls; Loguru capture requires routing via `logger.add(caplog.handler)` per upstream guidance.

**Constraints**
- No new runtime dependencies; reuse pytest monkeypatching and lightweight stubs instead of introducing `pytest-httpx` or `respx`.
- Tests must remain offline-friendly and deterministic across CI.
- Keep functions ≤20 lines and files ≤200 lines; prefer adding to existing test modules (`tests/test_setup.py`, `tests/test_engines.py`).

### Task 1 – Probe `_test_single_endpoint` data handling & verbose logging
- **Implementation**
  1. Monkeypatch `httpx.Client` with a synchronous stub returning crafted responses so `_test_single_endpoint` sees (a) `{ "data": [...] }` and (b) list payloads without network access.
  2. Instantiate `SetupWizard(non_interactive=True, verbose=True)` with a `DiscoveredProvider` carrying a base URL to trigger the HTTP path.
  3. Assert the provider toggles `is_available`, `model_count`, and captures both success and failure branches; use a temporary Loguru handler tied to `caplog` to exercise verbose log lines.
- **Tests**
  - Add `test_test_single_endpoint_populates_model_count_from_dict_and_list` covering the dict/list parsing branch.
  - Add `test_test_single_endpoint_logs_verbose_status` validating the debug message content when `verbose` is enabled.
- **Edge Cases**
  - Ensure 200 responses without `data` default model_count to 1.
  - Simulate a non-200 response to confirm the existing error pathway remains untouched.

### Task 2 – Harden provider discovery & validation defaults
- **Implementation**
  1. Use `monkeypatch.setenv("DEEPL_API_KEY", "token")` and instantiate `SetupWizard` to run `_discover_providers`, verifying the Deepl credential adds `deep-translator/deepl` via `normalize_selector` (covers line 189).
  2. Create a wizard instance and call `_validate_config([])` to hit the early return guard (line 148) without emitting tables; ensure the method exits cleanly and leaves `validation_results` empty.
  3. Extend an integration-style test that runs `_generate_config` with discovered Deepl/OpenAI providers so default engine selection falls through to the correct branch (lines 451-459).
- **Tests**
  - Add `test_discover_providers_includes_deepl_engine_mapping`.
  - Add `test_validate_config_returns_immediately_when_no_results`.
  - Extend or add `test_generate_config_sets_default_engine_priority` to assert fallback ordering.
- **Edge Cases**
  - Clean up environment variables post-test to avoid cross-test interference.
  - Mock console printing via Fire-safe `Console` or rely on non-interactive mode to avoid actual terminal output.

### Task 3 – Cover remaining engine error paths
- **Implementation**
  1. Monkeypatch `sys.modules["translators"]` with a stub exposing `translate_html` / `translate_text` to verify `TranslatorsEngine` routes HTML requests correctly (line 103).
  2. Monkeypatch `sys.modules["deep_translator"]` with minimal provider classes and assert `DeepTranslatorEngine("invalid", config)` raises `EngineError` (line 158).
  3. Build a minimal `AbersetzConfig` without credentials and assert `_build_hysf_engine` surfaces the `Missing credential` error (line 346).
- **Tests**
  - Add `test_translators_engine_translates_html_with_stub` ensuring HTML path used and reuse existing stubbed request fixtures.
  - Add `test_deep_translator_engine_rejects_unknown_provider` raising `EngineError`.
  - Add `test_build_hysf_engine_without_credential_raises_error` to lock in the credential guard.
- **Edge Cases**
  - Restore original modules in `sys.modules` after each test to prevent bleed-over.
  - Keep stubs minimal to avoid accidentally depending on real packages.

### Testing & Verification
- Follow RED ➜ GREEN ➜ REFACTOR per task: write failing tests first, implement minimal fixtures/stubs, rerun targeted tests, then `python -m pytest -xvs` and the coverage suite to confirm 96% stays or improves.
- Run `uvx mypy .` and `uvx bandit -r .` post-implementation to ensure diagnostics remain unchanged.
- *Completed 2025-09-21 via targeted pytest runs recorded in `WORK.md`; full suite now reports 97% coverage with engines/setup guardrails locked in.*

### Dependencies
- No new dependencies required; rely on `pytest`, `monkeypatch`, `caplog`, and custom stubs per research recommendations.

### Future Considerations
- Investigate the recursive fallback at `config.py:322`, which currently risks runaway recursion when stored credentials lack explicit values; a follow-up may refactor this logic once current guardrails are covered.

## Maintenance Sprint – Type & Setup Reliability *(Completed 2025-09-21)*
**Goal**: Reduce mypy noise in test helpers and lock in setup defaults by adding focused tests without expanding runtime surface area.

### Task 1 – Tighten example protocol typing *(done)*
- **Problem**: `tests/test_examples.py` casts the loaded module to `_BasicApiModule`, but the protocol only declares `format_example_doc`, causing mypy to flag every example function access (88 total errors cite these attributes).
- **Approach**:
  1. Expand `_BasicApiModule` to describe the example callables actually exercised (`example_simple`, `example_batch`, `example_dry_run`, `example_html`, `example_with_config`, `example_llm_with_voc`, and `cli`).
  2. Replace ad-hoc `object` stubs in the config helper with lightweight dataclasses carrying typed attributes so mypy no longer reports `object` attribute access.
  3. Keep runtime behaviour identical; only adjust typing helpers and shared fixtures.
- **Verification**: `uvx mypy tests/test_examples.py` now reports only missing third-party stubs; `python -m pytest tests/test_examples.py -xvs` passes with existing coverage snapshot.

### Task 2 – Match Path.stat monkeypatch signature *(done)*
- **Problem**: The large-file warning test monkeypatches `Path.stat` with `fake_stat(*args, **kwargs)`, leading mypy to complain about an unexpected `**dict[str, object]` argument (error at `tests/test_pipeline.py:203`).
- **Approach**:
  1. Implement a small helper returning an `os.stat_result` via `os.stat_result((mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime))` or use `types.SimpleNamespace` with typed attributes.
  2. Define `fake_stat(self: Path, *, follow_symlinks: bool = True) -> os.stat_result` to mirror the real signature.
  3. Restore the original `Path.stat` after the test to avoid cross-test effects.
- **Verification**: `python -m pytest tests/test_pipeline.py -k "warns_on_large_file" -xvs`; `uvx mypy tests/test_pipeline.py` now only flags missing stubs.

### Task 3 – Cover setup default engine fallback *(done)*
- **Problem**: `src/abersetz/setup.py` lines 453-459 (fallback to `ullm/default` or first engine) remain uncovered, leaving default selection unverified when only ullm/self-hosted engines exist.
- **Approach**:
  1. Build a `SetupWizard` instance with fabricated `DiscoveredProvider` entries representing only `ullm` (available) plus a custom engine to exercise each branch.
  2. Invoke `_generate_config()` to assert defaults prefer `ullm/default` when present and fall back to the first engine when no preferred family is available.
  3. If helper is private, add test to `tests/test_setup.py` constructing the wizard directly in non-interactive mode.
- **Verification**: `python -m pytest tests/test_setup.py -k defaults_to_ullm -xvs`; `setup.py` uncovered lines reduced to the verbose failure path plus fallback guard.

## Maintenance Sprint – Quality Hardening (Planned 2025-09-21)

## Maintenance Sprint – Mypy Noise Reduction (Planned 2025-09-21)
**Goal**: Reduce stubborn mypy diagnostics by tightening test-only helpers without touching production code paths.

### Task 1 – Restore DeepTranslator providers without Mapping.copy
- **Problem**: `tests/test_engines.py` calls `.copy()` on the providers mapping returned by `DeepTranslatorEngine._get_providers()`, which mypy flags because the return type is `Mapping[str, type]`.
- **Approach**: Snapshot providers with `dict(DeepTranslatorEngine._get_providers())`, reassign using shallow copies inside the test, and ensure the `finally` block restores the mapping with the same concrete type.
- **Verification**: `python -m pytest tests/test_engines.py -k deep_translator_engine_retries_on_network_failures -xvs`; `uvx mypy tests/test_engines.py` should drop the `attr-defined` error.
- **Status**: Completed 2025-09-21 10:38 UTC; switched to `dict(...)` snapshot in `tests/test_engines.py` and reran targeted pytest plus full suite.

### Task 2 – Make offline smoke test assertions explicit
- **Problem**: `tests/test_offline.py::test_import_works_offline` asserts module-level callables directly, which mypy warns about (`Function ... could always be true`).
- **Approach**: Replace raw truthiness checks with `is not None` and `callable(...)` assertions so type checkers see deliberate checks instead of truthy objects.
- **Verification**: `python -m pytest tests/test_offline.py -xvs`; `uvx mypy tests/test_offline.py` should eliminate the truthiness diagnostics.
- **Status**: Completed 2025-09-21 10:38 UTC; assertions now use `isinstance`/`callable`, targeted pytest run succeeded.

### Task 3 – Pass typed arguments into CLI engines helper
- **Problem**: `tests/test_cli.py` invokes `AbersetzCLI().engines(**kwargs)`, which mypy interprets as supplying a `dict[str, object]` positional argument, raising an `arg-type` warning.
- **Approach**: Update the local `render` helper to accept explicit parameters and call `AbersetzCLI().engines(False, family=family, configured_only=configured_only)` (or equivalent) so the signature matches the annotated method.
- **Verification**: `python -m pytest tests/test_cli.py -k engines_lists_providers_with_filters -xvs`; `uvx mypy tests/test_cli.py` should drop the argument-type complaints.
- **Status**: Completed 2025-09-21 10:38 UTC; helper now threads positional `include_paid` and reruns targeted pytest successfully.
**Goal**: Tighten typing assurance and coverage around existing helpers without expanding runtime surface area.

### Task 1 – Stabilize OpenAI chat namespace typing
- **Problem**: mypy reports `Chat` lacks a `completions` attribute, leaving `OpenAI` compatibility unchecked and keeping four diagnostics open in `openai_lite.py` and associated tests.
- **Approach**: Declare `completions` on `Chat` with an explicit optional `ChatCompletions` type and assign it during `OpenAI` initialization; add a focused unit test confirming the attribute is populated.
- **Tests**: `python -m pytest tests/test_openai_lite.py -k completions`, `uvx mypy src/abersetz/openai_lite.py tests/test_openai_lite.py`.
- **Dependencies**: none beyond existing stdlib and project tooling.
- **Status**: Completed 2025-09-21; see `tests/test_openai_lite.py::test_chat_declares_completions_attribute` and mypy summary (67 errors remaining).

### Task 2 – Cover setup default engine fallback
- **Problem**: `_generate_config` lines 457-459 remain untested, so default engine selection could regress when only non-priority engines are present.
- **Approach**: Extract the priority selection into a helper so we can drive the fallback branch with synthetic engine maps, then add regression tests covering translators, ullm, and unknown-engine scenarios.
- **Tests**: `python -m pytest tests/test_setup.py -k default_engine`, full suite for sanity.
- **Dependencies**: reuse pytest + existing fixtures.
- **Status**: Completed 2025-09-21; helper `_select_default_engine` exercised with new regression tests.

### Task 3 – Exercise `TranslationWorkflow.generate_report`
- **Problem**: `examples/advanced_api.py` sits at 28% coverage and lacks assertions around report aggregation and error tracking.
- **Approach**: Stub `translate_path` to feed deterministic `TranslationResult` objects, verify `translate_project` accumulates results/errors, and ensure `generate_report` returns the expected summary without touching the filesystem.
- **Tests**: `python -m pytest tests/test_examples.py -k translation_workflow`, targeted coverage check.
- **Dependencies**: no new packages; rely on pytest monkeypatch and Path utilities.
- **Status**: Completed 2025-09-21; report helper now creates parent directories before writing.

## Maintenance Sprint – Coverage & Typing Polish *(Completed 2025-09-21)*
**Outcome**: Eliminated the recursive credential loop, decoupled translator tests from private state, and hardened advanced examples so mypy defaults behave predictably.

## Maintenance Sprint – Reliability Touchups *(Completed 2025-09-21 09:24 UTC)*
**Objective**: Closed lingering coverage gaps around optional dependency fallbacks and confirmed pipeline chunk sizing honours engine preferences.

### Task 1 – Prove chunker fallback maintains global imports
- **Problem**: `tests/test_chunking.py` left line 39 uncovered, meaning the fallback import hook never re-entered the happy path; this hid regressions where the hook could block other imports.
- **Approach**: Extended the fallback test to import a safe stdlib module after the simulated failure, asserting the hook defers to the original importer.
- **Verification**: `python -m pytest tests/test_chunking.py -xvs` passed (5 tests) and full suite confirmed 100% coverage for `chunking.py`.

### Task 2 – Verify translator provider stub preserves stdlib imports
- **Problem**: `tests/test_engine_catalog.py` missed line 77, so we never demonstrated that the translators import shim leaves other imports untouched.
- **Approach**: Updated the failure-path test to import a harmless module post-shim and assert normal behaviour, preventing regressions where the shim over-mocks builtins.
- **Verification**: `python -m pytest tests/test_engine_catalog.py -xvs` passed (13 tests) with full suite coverage now 100% for `engine_catalog.py`.

### Task 3 – Assert pipeline honours engine chunk sizing
- **Problem**: `tests/test_pipeline.py` line 27 remained uncovered, leaving the `chunk_size_for` helper unverified when options omit chunk hints.
- **Approach**: Introduced a focused pipeline test where `TranslatorOptions` left chunk sizes unset but the engine advertises a custom chunk size, then asserted the resulting translation records that size.
- **Verification**: `python -m pytest tests/test_pipeline.py -k "chunk_size" -xvs` passed; full suite shows `pipeline.py` at 100% coverage.

### Task 1 – Exercise `resolve_credential` recursion without secrets *(done)*
- Added `tests/test_config.py::test_resolve_credential_with_recursive_name_logs_once`, capturing the INFO-level guidance and verifying the helper returns `None` without infinite recursion when only a named credential exists.
- Updated `src/abersetz/config.py` to skip re-resolving identical credential objects, preventing the stack overflow observed when `SILICONFLOW_API_KEY` is unset.

### Task 2 – Refactor translator tests to avoid private attributes *(done)*
- Stubbed `sys.modules["translators"]` with lightweight fakes before engine creation so the translator tests no longer touch `engine._translators`, removing the mypy attribute errors.
- Preserved behavioural assertions for text, HTML, and retry flows by recording inputs on the stub functions.

### Task 3 – Remove Optional default pitfalls in `examples/advanced_api` *(done)*
- Replaced implicit Optional defaults with explicit guards in `TranslationWorkflow` and `vocManager.translate_with_consistency`, copying the base vocabulary to avoid mutating caller data.
- Added regression coverage in `tests/test_examples.py` to prove lazy config loading happens once and that vocabulary merging honors supplied seeds without side effects.

## Maintenance Sprint – Advanced Examples Hardening *(Planned)*
**Objective**: Lift `examples/advanced_api.py` coverage above 95% and harden its CLI ergonomics without expanding functionality.

### Task 1 – Cover vocabulary loading and merging *(Completed 2025-09-21 11:37 UTC)*
- **Problem**: Lines 141-150 in `examples/advanced_api.py` remained uncovered, so regressions in `vocManager.load_voc` / `merge_vocabularies` would go unnoticed.
- **Approach**: Added `tests/test_examples.py::test_voc_manager_load_and_merge`, which writes temporary voc JSON files, loads them via `load_voc`, merges with a missing key, and asserts the merged mapping preserves latest overrides.
- **Tests**: `python -m pytest tests/test_examples.py -xvs`; `python -m pytest -xvs`.
- **Dependencies**: No new packages; reused stdlib `json` and existing fixtures.
- **Result**: `examples/advanced_api.py` coverage now 100%.

### Task 2 – Verify incremental checkpoint reuse *(Completed 2025-09-21 11:37 UTC)*
- **Problem**: `IncrementalTranslator.load_checkpoint` and `save_checkpoint` branches (lines 292-299) lacked coverage, leaving checkpoint persistence fragile.
- **Approach**: Added `tests/test_examples.py::test_example_incremental_translation_reuses_checkpoint`, seeding the checkpoint file, capturing patched `translate_path`, and asserting the checkpoint rewrites with both completed and newly processed files.
- **Tests**: `python -m pytest tests/test_examples.py -xvs`; `python -m pytest -xvs`.
- **Dependencies**: No new packages required.
- **Result**: Checkpoint branches now exercised; output asserts "Already completed" messaging.

### Task 3 – Exercise advanced CLI entrypoint usage banner *(Completed 2025-09-21 11:37 UTC)*
- **Problem**: The `__main__` guard (lines 327-343) was untested, so usage guidance or dispatch regressions would slip through.
- **Approach**: Added `tests/test_examples.py::test_advanced_api_cli_dispatch_runs_requested_example` and `tests/test_examples.py::test_advanced_api_cli_usage_banner`, monkeypatching `abersetz.translate_path` / `load_config` to keep execution lightweight while running the script via `runpy` for both dispatch and usage flows.
- **Tests**: `python -m pytest tests/test_examples.py -xvs`; `python -m pytest -xvs`; `python -m pytest --cov=. --cov-report=term-missing`.
- **Dependencies**: Reused `runpy`, `monkeypatch`, and existing stubs.
- **Result**: Advanced CLI entrypoint now covered and prints expected usage banner; suite coverage climbs to 98% overall.

## Maintenance Sprint – Type Hygiene & Chunking *(Completed 2025-09-21 12:07 UTC)*
**Objective**: Reduce type-checker noise and lock down pipeline chunk selection edge cases without expanding surface area.

### Task 1 – Silence third-party stub noise in mypy
- **Problem**: `uvx mypy .` still reports 49 errors, overwhelmingly `import-not-found` diagnostics for libraries without published stubs (pytest, httpx, tenacity, rich, loguru, platformdirs, semantic-text-splitter, translators, tomli_w, langcodes).
- **Approach**: Added per-module `ignore_missing_imports = true` overrides in `pyproject.toml` so mypy skips these external packages while continuing to type-check first-party code. Documented the rationale in `CHANGELOG.md` and `WORK.md`.
- **Tests**: `uvx mypy .` (now reduced to 3 real errors), `python -m pytest -xvs`.
- **Result**: Type-check noise shrank from 49 to 3 diagnostics (CLI optional output handling plus external dump fallback).

### Task 2 – Align integration API usage and cover string paths
- **Problem**: `tests/test_integration.py::test_translate_file_api` still calls `translate_path(..., output=...)`, triggering a mypy call-arg failure and leaving the string-path code path untested.
- **Approach**: Updated the integration test to pass `TranslatorOptions(output_dir=...)` and added new unit coverage in `tests/test_pipeline.py` to exercise string inputs/outputs, asserting translated files land in the expected directory.
- **Tests**: `python -m pytest tests/test_pipeline.py -k "string_source" -xvs`, full suite.
- **Result**: Integration test now matches the public API and regression coverage proves string paths resolve to the expected output directory.

### Task 3 – Verify HTML chunk-size fallback
- **Problem**: No test exercises `_select_chunk_size` when HTML content relies on engine-provided chunk sizes while config defaults collapse to zero, so regressions could silently change behaviour.
- **Approach**: Introduced a dedicated pipeline test that writes a small HTML file, forces defaults to `0`, and asserts `TranslationResult.chunk_size` equals the engine's HTML chunk hint.
- **Tests**: `python -m pytest tests/test_pipeline.py -k "html_uses_engine_chunk_hint" -xvs`, full suite.
- **Result**: Pipeline HTML flows now have regression coverage proving engine chunk hints override zeroed defaults.

## Maintenance Sprint – Residual Type & Coverage Polish *(Completed 2025-09-21 12:40 UTC)*
**Objective**: Eliminate the final mypy diagnostics and cover the remaining pipeline chunk-size branches so runtime behaviour stays predictable under mixed formats.

### Task 1 – Resolve optional output typing gaps
- **Problem**: `uvx mypy .` still reports three errors because `_build_options_from_cli` expects `str | None` while Fire passes `Path` objects, and `external/dump_models.py` narrows `api_key_env` to `None` after being inferred as `str`.
- **Approach**: Accept `Path | str | None` in the CLI option parser, normalise to `Path | None`, and update the dump script to type the intermediate `api_key_env` variable as optional while keeping behaviour identical. Add CLI regression tests to prove both string and `Path` outputs flow into `TranslatorOptions.output_dir` without breaking Fire bindings.
- **Tests**: `python -m pytest tests/test_cli.py -k "output_dir" -xvs`; `uvx mypy .`.
- **Success Criteria**: Mypy exits cleanly with zero errors; CLI tests confirm `output` arguments round-trip whether provided as strings or paths.
- **Result**: `uvx mypy .` now reports zero errors, and `tests/test_cli.py::test_cli_translate_accepts_path_output` passes while confirming Path-based outputs resolve correctly.

### Task 2 – Exercise DummyEngine chunk-size fallback
- **Problem**: Coverage reports indicate line 28 in `tests/test_pipeline.py` (the base `DummyEngine.chunk_size_for` branch) never executes, leaving the plain-text fallback unverified.
- **Approach**: Add a focused pipeline test that runs with defaults forcing `chunk_size=0` and uses the stock `DummyEngine`, asserting the returned result records the engine-provided chunk size and that the engine tracked the invocation.
- **Tests**: `python -m pytest tests/test_pipeline.py -k "dummy_engine_chunk" -xvs`; `python -m pytest -xvs`.
- **Success Criteria**: Coverage for `DummyEngine.chunk_size_for` reaches 100%, and the new test demonstrates the pipeline asks the engine for chunk sizing when defaults collapse.
- **Result**: `tests/test_pipeline.py::test_translate_path_uses_dummy_chunk_size_when_defaults_zero` passes, recording a `TextFormat.PLAIN` call and asserting the chunk size equals the engine value.

### Task 3 – Cover HtmlEngine plain-text fallback branch
- **Problem**: Line 166 in `tests/test_pipeline.py` (the `HtmlEngine.chunk_size_for` non-HTML branch) remains unexecuted, so mixed-format runs could regress without detection.
- **Approach**: Introduce a regression test that feeds both HTML and plain-text files through an `HtmlEngine` variant, verifying the method records HTML and plain invocations and that the pipeline uses the expected chunk sizes for each format.
- **Tests**: `python -m pytest tests/test_pipeline.py -k "html_engine_mixed" -xvs`; `python -m pytest -xvs`.
- **Success Criteria**: Coverage marks the `HtmlEngine` fallback branch as executed, and the regression test asserts the pipeline honours HTML-specific sizes while falling back to the plain-text chunk size for other files.
- **Result**: `tests/test_pipeline.py::test_translate_path_with_html_engine_handles_mixed_formats` passes, documenting both HTML and plain invocations and validating the expected chunk sizes.

## Maintenance Sprint – CLI Option Guardrails *(Planned)*
**Objective**: Backfill regression coverage for CLI option validation and propagation so user-facing flags behave predictably without introducing new functionality.

### Task 1 – Cover target-language requirement guard
- **Problem**: `_build_options_from_cli` raises `ValueError("Target language is required")` when `to_lang` is missing, yet no test exercises the branch, leaving the guard unverified.
- **Approach**: Add a focused unit test that invokes `_build_options_from_cli` with `to_lang=None` and asserts the exact `ValueError`, documenting Fire’s behaviour when users omit the positional language argument.
- **Tests**: `python -m pytest tests/test_cli.py -k "target_language_required" -xvs`.
- **Packages**: No new dependencies; pytest and existing CLI helpers cover the scenario.

### Task 2 – Validate prolog and voc ingestion
- **Problem**: `AbersetzCLI.tr` relies on `_load_json_data` to hydrate `prolog` and `voc`, but there is no CLI-level regression ensuring inline JSON and file-backed payloads reach `TranslatorOptions` as dictionaries.
- **Approach**: Extend `tests/test_cli.py` with a case that supplies both inline and file-based JSON via `prolog`/`voc`, intercepts the resulting `TranslatorOptions`, and asserts the dictionaries match the input payloads.
- **Tests**: `python -m pytest tests/test_cli.py -k "prolog_voc" -xvs`.
- **Packages**: No external libraries required beyond stdlib `json` and existing pytest fixtures.

### Task 3 – Ensure optional flags propagate to translator options
- **Problem**: Flags such as `save_voc`, `write_over`, `chunk_size`, and `html_chunk_size` depend on `_build_options_from_cli`, yet current tests only cover include/exclude parsing and Path outputs, leaving these toggles unverified end-to-end.
- **Approach**: Add a regression test invoking `AbersetzCLI.tr` with the optional flags, capture the `TranslatorOptions`, and assert each flag propagates exactly as provided.
- **Tests**: `python -m pytest tests/test_cli.py -k "optional_flags_propagate" -xvs`.
- **Packages**: No additional dependencies; reuse existing CLI test scaffolding.
