---
this_file: CHANGELOG.md
---
# Changelog

All notable changes to abersetz will be documented in this file.

## [Unreleased]

### Release Highlights (Draft)
- Short engine selectors everywhere (`tr/*`, `dt/*`, `ll/*`, `hy`) with automatic config migration and backwards-compatible aliases.
- New `abersetz validate` health-check plus setup wizard integration for immediate pass/fail feedback.
- Provider-aware setup wizard with pricing hints, richer CLI tables, and coverage-driven test suites ensuring 91% baseline.

### Maintenance
- 2025-09-21 12:39 UTC — `python -m pytest -xvs` (180 passed, 8 skipped in 91.12s; coverage 98% with uncovered lines limited to CLI 286 and intentionally skipped integrations.)
- 2025-09-21 12:39 UTC — `python -m pytest --cov=. --cov-report=term-missing` (180 passed, 8 skipped in 80.92s; coverage unchanged at 98% with explicit misses on CLI line 286 plus skipped integration scaffolding and guarded setup/pipeline asserts.)
- 2025-09-21 12:39 UTC — `uvx mypy .` (success; zero errors aside from the expected `annotation-unchecked` notice for the advanced API helper.)
- 2025-09-21 12:39 UTC — `uvx bandit -r .` (448 Low-severity findings stemming from deliberate test `assert`s and the config backup guard; no Medium/High issues.)
- 2025-09-21 12:39 UTC — /cleanup removed `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.benchmarks`, and `.coverage` artifacts immediately after verification.
- 2025-09-21 12:45 UTC — `python -m pytest -xvs` (180 passed, 8 skipped in 80.56s; coverage 98% with only skipped integrations and a single CLI guard line outstanding.)
- 2025-09-21 12:45 UTC — `python -m pytest --cov=. --cov-report=term-missing` (180 passed, 8 skipped in 94.41s; coverage unchanged at 98% with explicit misses on CLI line 286, skipped integrations, and guarded regression scaffolding.)
- 2025-09-21 12:45 UTC — `uvx mypy .` (success; zero errors with the expected annotation-unchecked notice only.)
- 2025-09-21 12:45 UTC — `uvx bandit -r .` (448 Low-severity findings from intentional test `assert`s and the config backup guard; Medium/High severities remain zero.)
- 2025-09-21 12:45 UTC — /cleanup removed `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.benchmarks`, and `.coverage` artifacts after the full verification sweep.
- 2025-09-21 12:16 UTC — `python -m pytest -xvs` (177 passed, 8 skipped in 88.81s; coverage plugin reported 98% overall with misses limited to intentionally skipped integration scaffolding and four guarded setup/pipeline lines.)
- 2025-09-21 12:16 UTC — `python -m pytest --cov=. --cov-report=term-missing` (177 passed, 8 skipped in 85.02s; coverage table unchanged at 98% with explicit misses listing the skipped integration suite plus the guarded setup/pipeline assertions.)
- 2025-09-21 12:16 UTC — `uvx mypy .` (3 errors: CLI optional-output assignment handling in `src/abersetz/cli.py` and credential default typing in `external/dump_models.py`; all other modules clean.)
- 2025-09-21 12:16 UTC — `uvx bandit -r .` (438 Low-severity findings stemming from deliberate test `assert`s and the config backup `try/except/pass`; Medium/High severities remain zero.)
- 2025-09-21 12:16 UTC — /cleanup removed `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.benchmarks`, and `.coverage` artifacts immediately after verification.
- 2025-09-21 12:06 UTC — Added `[tool.mypy]` overrides to silence stubless third-party imports and introduced pipeline regression tests for string paths and HTML chunk hints while updating the integration API usage.
- 2025-09-21 12:06 UTC — `python -m pytest -xvs` (177 passed, 8 skipped in 88.93s; coverage 98% with only intentionally skipped integrations outstanding.)
- 2025-09-21 12:06 UTC — `python -m pytest --cov=. --cov-report=term-missing` (177 passed, 8 skipped in 81.35s; coverage unchanged at 98% with misses restricted to skipped integrations and guarded pipeline/setup lines.)
- 2025-09-21 12:06 UTC — `uvx mypy .` (3 errors: CLI output option typing and external dump optional string fallback.)
- 2025-09-21 12:06 UTC — `uvx bandit -r .` (438 Low-severity findings from expected pytest `assert`s and config backup guard; Medium/High severities remain zero.)
- 2025-09-21 12:06 UTC — /cleanup removed `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.benchmarks`, and `.coverage` artifacts post-verification.
- 2025-09-21 11:50 UTC — `python -m pytest -xvs` (175 passed, 8 skipped in 90.23s; overall coverage reported at 98% with only intentionally skipped integration scaffolding outstanding.)
- 2025-09-21 11:50 UTC — `python -m pytest --cov=. --cov-report=term-missing` (175 passed, 8 skipped in 80.11s; coverage totals steady at 98% with misses isolated to skipped integration placeholders and guarded pipeline/setup asserts.)
- 2025-09-21 11:50 UTC — `uvx mypy .` (49 errors; unchanged missing third-party stubs plus known CLI/pipeline union assignments and the intentional integration keyword argument.)
- 2025-09-21 11:50 UTC — `uvx bandit -r .` (430 Low-severity findings stemming from expected pytest `assert`s and the config backup `try/except/pass`; Medium/High severities remain zero.)
- 2025-09-21 11:50 UTC — /cleanup removed `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.benchmarks`, and `.coverage` artifacts post-verification.
- 2025-09-21 11:39 UTC — `python -m pytest tests/test_examples.py -xvs` (22 passed in 1.83s; `examples/advanced_api.py` coverage now 100% with new voc/CLI tests.)
- 2025-09-21 11:39 UTC — `python -m pytest -xvs` (175 passed, 8 skipped in 84.35s; total coverage 98% with only intentionally skipped integration scaffolding outstanding.)
- 2025-09-21 11:39 UTC — `python -m pytest --cov=. --cov-report=term-missing` (175 passed, 8 skipped in 82.11s; coverage summary confirms `examples/advanced_api.py` fully covered, residual misses confined to skipped integration placeholders.)
- 2025-09-21 11:39 UTC — `uvx mypy .` (49 errors; unchanged missing third-party stubs plus known CLI union assignments.)
- 2025-09-21 11:39 UTC — `uvx bandit -r .` (430 Low-severity findings from expected pytest `assert`s and the config backup guard; Medium/High severities remain clear.)
- 2025-09-21 11:39 UTC — /cleanup removed `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.benchmarks`, and `.coverage` artifacts post-verification.
- 2025-09-21 11:28 UTC — `python -m pytest -xvs` (171 passed, 8 skipped in 94.32s; inline coverage holds at 97% with uncovered lines restricted to `examples/advanced_api.py` and intentionally skipped integration scaffolding.)
- 2025-09-21 11:28 UTC — `python -m pytest --cov=. --cov-report=term-missing` (171 passed, 8 skipped in 80.50s; coverage breakdown unchanged with `examples/advanced_api.py` lines 141-343 and `tests/test_integration.py` skip placeholders flagged.)
- 2025-09-21 11:28 UTC — `uvx mypy .` (49 errors; all attributable to missing third-party stubs plus known CLI union assignments, no regressions detected.)
- 2025-09-21 11:28 UTC — `uvx bandit -r .` (419 Low-severity findings from deliberate pytest `assert`s and the config backup `try/except/pass` guard; Medium/High severities remain clear.)
- 2025-09-21 11:28 UTC — /cleanup removed `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.benchmarks`, and `.coverage` artifacts post-report.
- 2025-09-21 09:24 UTC — `python -m pytest -xvs` (171 passed, 8 skipped in 98.65s; coverage inline summary now shows 100% for `chunking.py`, `engine_catalog.py`, and `pipeline.py`).
- 2025-09-21 09:24 UTC — `python -m pytest --cov=. --cov-report=term-missing` (171 passed, 8 skipped in 82.02s; totals steady at 97% with remaining gaps limited to `examples/advanced_api.py` and intentionally skipped integrations).
- 2025-09-21 09:24 UTC — Targeted pytest runs (`tests/test_chunking.py`, `tests/test_engine_catalog.py`, `tests/test_pipeline.py -k "chunk_size"`) all passed, confirming fallback import guards and engine chunk sizing coverage.
- 2025-09-21 09:24 UTC — `uvx mypy .` (49 errors; unchanged missing-stub diagnostics plus existing CLI union assignments).
- 2025-09-21 09:24 UTC — `uvx bandit -r .` (419 Low-severity findings: expected test `assert`s and config backup guard; Medium/High severities remain clear).
- 2025-09-21 09:24 UTC — /cleanup removed `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.benchmarks`, and `.coverage` artifacts post-touchup.
- 2025-09-21 09:14 UTC — `python -m pytest -xvs` (170 passed, 8 skipped in 104.55s; coverage inline summary reported 97% overall with residual misses in `examples/advanced_api.py` and intentionally skipped integration scaffolding).
- 2025-09-21 09:14 UTC — `python -m pytest --cov=. --cov-report=term-missing` (170 passed, 8 skipped in 83.28s; coverage totals unchanged at 97% with `examples/advanced_api.py` flagged for 21 uncovered lines and integration skips enumerated).
- 2025-09-21 09:14 UTC — `uvx mypy .` (49 errors; outstanding items are missing third-party stubs plus known CLI/output union checks, no regressions observed).
- 2025-09-21 09:14 UTC — `uvx bandit -r .` (415 Low-severity findings from expected test `assert`s and the config backup guard; Medium/High severities remain clear).
- 2025-09-21 09:14 UTC — /cleanup removed `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.benchmarks`, and `.coverage` artifacts after the verification sweep.
- 2025-09-21 11:03 UTC — `python -m pytest -xvs` (170 passed, 8 skipped in 108.03s; coverage climbs to 97% overall with `examples/advanced_api.py` at 88% and `setup.py` fully covered).
- 2025-09-21 11:03 UTC — `python -m pytest --cov=. --cov-report=term-missing` (170 passed, 8 skipped in 85.13s; remaining uncovered lines confined to optional CLI banners and skipped integrations).
- 2025-09-21 11:03 UTC — `uvx mypy .` (49 errors; reduced from 58 after report refactor and coverage additions, residual issues are missing stubs plus known CLI signature unions).
- 2025-09-21 11:03 UTC — `uvx bandit -r .` (415 Low-severity findings from expected test asserts and config backup guard; Medium/High severities still clear).
- 2025-09-21 11:03 UTC — Added typed report helpers and new example/setup tests, unlocking 100% coverage for `setup.py` and high-confidence async example workflows.
- 2025-09-21 08:46 UTC — `python -m pytest -xvs` (162 passed, 8 skipped in 80.41s; coverage plugin summary steady at 95% overall with remaining misses in `examples/advanced_api.py` and `setup.py` fallback helper).
- 2025-09-21 08:46 UTC — `python -m pytest --cov=. --cov-report=term-missing` (162 passed, 8 skipped in 80.61s; missing lines unchanged: `examples/advanced_api.py`, `setup.py:221/262/286/471`, integration skips).
- 2025-09-21 08:46 UTC — `uvx mypy .` (58 errors; all missing third-party stubs plus longstanding example/test typing gaps, no new diagnostics).
- 2025-09-21 08:46 UTC — `uvx bandit -r .` (390 Low-severity findings from expected test asserts and config backup guard; Medium/High severities remain clear).
- 2025-09-21 08:46 UTC — /cleanup removed `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.benchmarks`, and `.coverage` artifacts after the QA sweep.
- 2025-09-21 10:38 UTC — `python -m pytest -xvs` (162 passed, 8 skipped in 82.49s; coverage table unchanged at 95% overall after test helper adjustments.)
- 2025-09-21 10:38 UTC — `uvx mypy .` (58 errors remaining; removed attr/truthiness/arg-type warnings, outstanding diagnostics are missing third-party stubs plus legacy example typing.)
- 2025-09-21 10:38 UTC — Targeted pytest runs (`tests/test_engines.py -k deep_translator_engine_retry_on_failure`, `tests/test_offline.py`, `tests/test_cli.py -k cli_engines_lists_configured_providers`) all passed to validate helper tweaks.
- 2025-09-21 10:38 UTC — /cleanup removed `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.benchmarks`, and `.coverage` artifacts post-work sweep.
- 2025-09-21 10:29 UTC — `python -m pytest -xvs` (162 passed, 8 skipped in 81.14s; coverage summary stayed at 95% overall with `setup.py` retaining 4 uncovered lines and integration scaffolding intentionally skipped.)
- 2025-09-21 10:29 UTC — `python -m pytest --cov=. --cov-report=term-missing` (162 passed, 8 skipped in 81.10s; coverage 95% overall with misses in `examples/advanced_api.py`, `setup.py:221/262/286/471`, and inert integration placeholders.)
- 2025-09-21 10:29 UTC — `uvx mypy .` (67 errors across 21 files; all due to missing third-party stubs plus known lenient typing in examples/tests.)
- 2025-09-21 10:29 UTC — `uvx bandit -r .` (390 Low-severity findings from expected test asserts and config backup guard; no Medium/High severities.)
- 2025-09-21 10:29 UTC — /cleanup removed `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.benchmarks`, and `.coverage` artifacts post-suite.
- 2025-09-21 10:20 UTC — `python -m pytest -xvs` (162 passed, 8 skipped in 80.66s; coverage summary reported 95% overall with `examples/advanced_api.py` now at 47% and `setup.py` uncovered lines reduced to four.)
- 2025-09-21 10:20 UTC — `python -m pytest --cov=. --cov-report=term-missing` (162 passed, 8 skipped in 81.84s; coverage held at 95% overall, missing lines restricted to `examples/advanced_api.py`, `setup.py:221/262/286/471`, and intentionally skipped integrations.)
- 2025-09-21 10:20 UTC — `uvx mypy .` (67 errors across 21 files; Chat namespace diagnostics cleared, residual issues stem from missing third-party stubs and legacy example/test typing gaps.)
- 2025-09-21 10:20 UTC — `uvx bandit -r .` (390 Low-severity findings (`B101` test asserts plus config backup guard); no Medium/High severities.)
- 2025-09-21 10:20 UTC — Targeted pytest runs (`tests/test_openai_lite.py -k completions`, `tests/test_setup.py -k select_default_engine`, `tests/test_examples.py -k translation_workflow`) verified new guards.
- 2025-09-21 10:20 UTC — /cleanup removed `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.coverage`, and `.benchmarks` artifacts post-suite.
- 2025-09-21 10:03 UTC — /cleanup removed `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.coverage`, and `.benchmarks` after the verification sweep.
- 2025-09-21 10:02 UTC — `python -m pytest -xvs` (154 passed, 8 skipped in 83.79s; inline coverage summary reported 94% total with misses isolated to `setup.py` fallback, `examples/advanced_api.py`, and intentionally skipped integration scaffolding.)
- 2025-09-21 10:02 UTC — `python -m pytest --cov=. --cov-report=term-missing` (154 passed, 8 skipped in 82.36s; coverage held at 94% overall with the same uncovered lines enumerated in the report.)
- 2025-09-21 10:02 UTC — `uvx mypy .` (71 errors across 21 files; unchanged missing third-party stubs plus attr/type diagnostics in examples, CLI fixtures, and integration tests.)
- 2025-09-21 10:02 UTC — `uvx bandit -r .` (377 Low-severity findings from expected test `assert`s and the config backup guard; Medium/High severities remain absent.)
- 2025-09-21 09:36 UTC — `python -m pytest -xvs` (151 passed, 8 skipped in 86.11s; coverage inline report flagged the remaining misses on `config.py:322`, `setup.py:220/261/285/457-459`, and the intentionally skipped integration scaffolding.)
- 2025-09-21 09:36 UTC — `python -m pytest --cov=. --cov-report=term-missing` (151 passed, 8 skipped in 86.37s; coverage steady at 97% overall with the same uncovered lines.)
- 2025-09-21 09:36 UTC — `uvx mypy .` (77 errors across 21 files; entirely missing third-party stubs plus legacy example/external Optional defaults and `_translators` attribute access in tests.)
- 2025-09-21 09:36 UTC — `uvx bandit -r .` (364 Low-severity findings produced by test `assert`s and the config backup guard; Medium/High severities absent.)
- 2025-09-21 09:36 UTC — /cleanup removed `.pytest_cache`, `.mypy_cache`, `.benchmarks`, `.coverage`, and `.ruff_cache` after documenting results.
- 2025-09-21 09:45 UTC — `python -m pytest tests/test_config.py -k recursive_name -xvs` (validated recursion fix; INFO log emitted once and function returned `None`).
- 2025-09-21 09:46 UTC — `python -m pytest tests/test_engines.py -k "translators_engine" -xvs` (translator stubs exercised text/HTML/retry flows without touching private attributes).
- 2025-09-21 09:47 UTC — `python -m pytest tests/test_examples.py -k "translation_workflow or translate_with_consistency" -xvs` (lazy config default and vocabulary copy behaviour confirmed with stubbed `translate_path`).
- 2025-09-21 09:54 UTC — `python -m pytest -xvs` (154 passed, 8 skipped in 81.16s; recursion fix verified and translator stubs exercised without private attribute access).
- 2025-09-21 09:54 UTC — `python -m pytest --cov=. --cov-report=term-missing` (154 passed, 8 skipped in 81.67s; coverage steady at 97% with residual misses isolated to `setup.py` fallback and skipped integration suite).
- 2025-09-21 09:55 UTC — `uvx mypy .` (71 errors across 21 files; reduced by addressing translator stubs and recursive credential path, remaining diagnostics stem from missing third-party stubs and legacy example tooling).
- 2025-09-21 09:55 UTC — /cleanup removed `.pytest_cache`, `.mypy_cache`, `.benchmarks`, `.coverage`, and `.ruff_cache` after the verification sweep.
- 2025-09-21 09:31 UTC — `python -m pytest -xvs` (151 passed, 8 skipped in 92.98s; coverage inline summary 97% with `setup.py` misses trimmed to 6 lines and `config.py:322` still outstanding.)
- 2025-09-21 09:31 UTC — `python -m pytest --cov=. --cov-report=term-missing` (151 passed, 8 skipped in 87.49s; uncovered lines limited to `config.py:322`, `setup.py:220/261/285/457-459`, and intentionally skipped integration scaffolding.)
- 2025-09-21 09:31 UTC — `uvx mypy .` (77 errors across 21 files; resolved `_BasicApiModule` attribute complaints and `Path.stat` override mismatch, remaining diagnostics are missing third-party stubs plus legacy example/external typing gaps.)
- 2025-09-21 09:31 UTC — `uvx bandit -r .` (364 Low-severity findings from test `assert`s and config backup guard; Medium/High severities absent.)
- 2025-09-21 09:31 UTC — /cleanup removed `.pytest_cache`, `.mypy_cache`, `.benchmarks`, `.coverage` immediately after the verification sweep.
- 2025-09-21 09:19 UTC — `python -m pytest -xvs` (150 passed, 8 skipped in 80.27s; coverage inline summary reported 97% with residual misses on `config.py:322`, `setup.py` verbose/error branches, and intentionally skipped integrations.)
- 2025-09-21 09:19 UTC — `python -m pytest --cov=. --cov-report=term-missing` (150 passed, 8 skipped in 79.98s; coverage steady at 97% with identical uncovered lines plus the `tests/test_integration.py` skip list.)
- 2025-09-21 09:19 UTC — `uvx mypy .` (88 errors across 22 files; missing third-party stubs for pytest/httpx/tenacity/platformdirs/langcodes/loguru/rich/semantic_text_splitter/tomli_w and Optional defaults in examples/external helpers remain outstanding.)
- 2025-09-21 09:19 UTC — `uvx bandit -r .` (361 Low-severity findings produced by test `assert` usage and the config backup guard; no Medium/High severities.)
- 2025-09-21 09:19 UTC — /cleanup removed `.pytest_cache`, `.mypy_cache`, `.benchmarks`, `.coverage` artifacts immediately after documentation updates.
- 2025-09-21 09:11 UTC — `python -m pytest -xvs` (150 passed, 8 skipped; coverage climbed to 97% with `engines.py` now fully covered and `setup.py` gaps limited to verbose/error-reporting branches.)
- 2025-09-21 09:11 UTC — `python -m pytest --cov=. --cov-report=term-missing` (150 passed, 8 skipped; coverage 97% overall with remaining misses on `config.py:322`, selective `setup.py` paths, and intentionally skipped integrations.)
- 2025-09-21 09:11 UTC — `uvx mypy .` (88 errors across 22 files; missing stubs for pytest/httpx/tenacity/platformdirs/langcodes/loguru/rich/semantic_text_splitter/tomli_w plus Optional defaults in examples/external helpers.)
- 2025-09-21 09:11 UTC — `uvx bandit -r .` (361 Low-severity findings; expected test `assert` usage and config backup guard, no Medium/High issues.)
- 2025-09-21 09:11 UTC — Removed `.pytest_cache`, `.mypy_cache`, `.benchmarks`, `.coverage` artifacts; `.ruff_cache` was not created during this run.
- 2025-09-21 09:10 UTC — `python -m pytest tests/test_setup.py -k "list_payload or logs_verbose" -xvs` (2 passed; covered list payload parsing and verbose log capture for `_test_single_endpoint`.)
- 2025-09-21 09:10 UTC — `python -m pytest tests/test_setup.py -k "deepl or prefers_hysf or returns_immediately" -xvs` (3 passed; exercised Deepl mapping, `_validate_config([])` early exit, and hysf default fallback.)
- 2025-09-21 09:09 UTC — `python -m pytest tests/test_engines.py -k "handles_html or rejects_unknown_provider or build_hysf" -xvs` (3 passed; covered Translators HTML path, deep-translator unsupported-provider error, and `_build_hysf_engine` credential guard.)
- 2025-09-21 08:57 UTC — `python -m pytest -xvs` (142 passed, 8 skipped in 89.51s; coverage remains 96% with residual misses on `config.py:322`, `engines.py` fallback branches, and setup validation scaffolding.)
- 2025-09-21 08:57 UTC — `python -m pytest --cov=. --cov-report=term-missing` (142 passed, 8 skipped in 81.25s; coverage 96% overall with remaining gaps identical to the standard run plus intentionally skipped integration suite lines.)
- 2025-09-21 08:57 UTC — `uvx mypy .` (85 errors across 22 files; missing third-party stubs for pytest/httpx/tenacity/platformdirs/langcodes/loguru/rich/semantic_text_splitter/tomli_w and Optional defaults in `examples/advanced_api.py` remain.)
- 2025-09-21 08:57 UTC — `uvx bandit -r .` (347 Low-severity findings; expected test `assert` usage and the config backup best-effort handler, Medium/High severities clear.)
- 2025-09-21 08:57 UTC — Removed `.pytest_cache`, `.mypy_cache`, `.benchmarks`, `.coverage`; `.ruff_cache` was not present this run.
- 2025-09-21 08:46 UTC — `uvx bandit -r .` (347 Low-severity findings; expected test `assert`s and config backup guard, Medium/High severities clear.)
- 2025-09-21 08:46 UTC — `uvx mypy .` (85 errors across 22 files; missing third-party stubs plus Optional defaults in examples/external scripts persist.)
- 2025-09-21 08:46 UTC — `python -m pytest --cov=. --cov-report=term-missing` (142 passed, 8 skipped; coverage 96% with remaining misses on credential recursion fallback, deep-translator unsupported provider branch, and setup validation scaffolding.)
- 2025-09-21 08:45 UTC — `python -m pytest -xvs` (142 passed, 8 skipped; new tests cover credential recursion, large-file warnings, and LLM payload fallbacks.)
- 2025-09-21 08:45 UTC — Removed `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.benchmarks`, `.coverage` after verification.
- 2025-09-21 08:44 UTC — `python -m pytest tests/test_engines.py -k "parse_payload or missing_selector" -xvs` (4 passed; exercised LLM payload fallbacks and missing engine config error.)
- 2025-09-21 08:44 UTC — `python -m pytest tests/test_pipeline.py -k warns_on_large_file -xvs` (1 passed; verified large-file warning branch.)
- 2025-09-21 08:43 UTC — `python -m pytest tests/test_config.py -k "resolve_credential_returns_none or resolve_credential_reuses" -xvs` (2 passed; validated null credential and alias recursion paths.)
- 2025-09-21 08:36 UTC — `uvx bandit -r .` (337 Low-severity findings; expected test `assert`s and config backup guard, Medium/High severities clear.)
- 2025-09-21 08:36 UTC — `uvx mypy .` (83 errors across 22 files; missing third-party stubs plus intentional Optional defaults and OpenAI shim attribute usage.)
- 2025-09-21 08:36 UTC — `python -m pytest --cov=. --cov-report=term-missing` (135 passed, 8 skipped; coverage steady at 96% with misses limited to credential recursion, retry fallbacks, pipeline messaging, setup validation branches, and skipped integrations.)
- 2025-09-21 08:35 UTC — `python -m pytest -xvs` (135 passed, 8 skipped in 81.67s after rerun; coverage plugin confirmed CLI/examples/validation at 100%, total coverage 96%.)
- 2025-09-21 08:35 UTC — Removed `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.benchmarks`, `.coverage` via /cleanup.
- 2025-09-21 08:27 UTC — `uvx bandit -r .` (337 Low-severity findings after new tests; Medium/High severities clear.)
- 2025-09-21 08:26 UTC — `uvx mypy .` (83 errors across 22 files; missing third-party stubs and Optional defaults unchanged.)
- 2025-09-21 08:26 UTC — `python -m pytest --cov=. --cov-report=term-missing` (135 passed, 8 skipped; coverage 96% with `cli.py` and `engine_catalog.py` now 100%, residual misses on credential recursion and integration scaffolding.)
- 2025-09-21 08:25 UTC — `python -m pytest -xvs` (135 passed, 8 skipped; confirmed new CLI/config/catalog tests and maintained 96% coverage.)
- 2025-09-21 08:23 UTC — `python -m pytest tests/test_engine_catalog.py -k normalize_selector -xvs` (6 passed; covered `None`/blank selector guards.)
- 2025-09-21 08:22 UTC — `python -m pytest tests/test_config.py -k engine_config_to_dict -xvs` (1 passed; verified optional field serialization.)
- 2025-09-21 08:21 UTC — `python -m pytest tests/test_cli.py -k deep_translator_string -xvs` (1 passed; exercised deep-translator string provider branch.)
- 2025-09-21 08:16 UTC — `python -m pytest -xvs` (130 passed, 8 skipped; coverage 96% with `cli.py` 99% and remaining misses confined to setup/config fallbacks plus skipped integrations.)
- 2025-09-21 08:16 UTC — `python -m pytest --cov=. --cov-report=term-missing` (130 passed, 8 skipped; coverage steady at 96% with misses on `cli.py:177`, config/env fallbacks, setup validation branches, and intentionally skipped integration scaffolding.)
- 2025-09-21 08:16 UTC — `uvx mypy .` (83 errors across 22 files; missing third-party stubs for pytest/httpx/tenacity/platformdirs/langcodes/loguru/rich plus Optional/default typing gaps in examples and external research scripts.)
- 2025-09-21 08:16 UTC — `uvx bandit -r .` (329 Low-severity findings: expected test `assert` usage and the config backup `try/except/pass` guard; Medium/High severities clear.)
- 2025-09-21 08:16 UTC — Removed `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.benchmarks`, `.coverage` during /cleanup following documentation updates.
- 2025-09-21 08:05 UTC — `python -m pytest -xvs` (130 passed, 8 skipped; coverage 96% with `examples/basic_api.py` and `chunking.py` now fully covered.)
- 2025-09-21 08:06 UTC — `python -m pytest --cov=. --cov-report=term-missing` (130 passed, 8 skipped; coverage steady at 96% with remaining misses unchanged.)
- 2025-09-21 08:06 UTC — `uvx mypy .` (92 errors unchanged; missing third-party stubs plus intentional `Chat.completions` and example protocol lookups.)
- 2025-09-21 08:06 UTC — `uvx bandit -r .` (329 Low-severity findings covering new test `assert`s and the config backup guard; Medium/High severities clear.)
- 2025-09-21 08:04 UTC — `python -m pytest tests/test_examples.py -k cli_dispatch -xvs` (1 passed; CLI dispatch test ensures example selection path works under stubbed translation.)
- 2025-09-21 08:04 UTC — `python -m pytest tests/test_chunking.py -k "blank or fallback" -xvs` (2 passed; fallback slices verified under forced ImportError.)
- 2025-09-21 08:05 UTC — `python -m pytest tests/test_package.py -k getattr -xvs` (1 passed; invalid attribute requests raise `AttributeError` and cache remains stable.)
- 2025-09-21 07:57 UTC — `python -m pytest -xvs` (126 passed, 8 skipped; coverage snapshot 96% with residual misses isolated to integration scaffolding and fallback branches across CLI/config/setup.)
- 2025-09-21 07:58 UTC — `python -m pytest --cov=. --cov-report=term-missing` (126 passed, 8 skipped; coverage steady at 96% with uncovered lines limited to `examples/basic_api.py:150`, package `__init__`, chunking fallbacks, engine retry guards, setup progress paths, and intentionally skipped integrations.)
- 2025-09-21 07:58 UTC — `uvx mypy .` (92 errors unchanged; missing third-party stubs plus intentional `Chat.completions` and dynamic example attributes.)
- 2025-09-21 07:58 UTC — `uvx bandit -r .` (321 Low-severity findings for deliberate test `assert`s and backup guard; Medium/High severities remain clear.)
- 2025-09-21 07:48 UTC — `python -m pytest -xvs` (126 passed, 8 skipped; project coverage 96% with `engines.py` gaps closed.)
- 2025-09-21 07:49 UTC — `python -m pytest --cov=. --cov-report=term-missing` (126 passed, 8 skipped; coverage steady at 96% with remaining misses isolated to integration scaffolding and setup progress branches.)
- 2025-09-21 07:49 UTC — `uvx mypy .` (92 errors unchanged; missing third-party stubs and intentional dynamic attributes in OpenAI shim and tests.)
- 2025-09-21 07:50 UTC — `uvx bandit -r .` (321 Low-severity findings covering deliberate test `assert`s and backup guard; Medium/High severities clear.)
- 2025-09-21 07:50 UTC — Removed `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.benchmarks`, `.coverage` during /cleanup.
- 2025-09-21 07:46 UTC — `python -m pytest tests/test_engines.py -xvs` (15 passed; `src/abersetz/engines.py` coverage lifted to 96% with new error-handling tests.)
- 2025-09-21 07:45 UTC — `python -m pytest tests/test_engines.py -k "profile" -xvs` (4 passed; verified default/variant selection and error handling for `_select_profile`.)
- 2025-09-21 07:44 UTC — `python -m pytest tests/test_engines.py -k "llm" -xvs` (3 passed; confirmed fail-fast behaviour when models or credentials are missing.)
- 2025-09-21 07:36 UTC — `python -m pytest -xvs` (118 passed, 8 skipped; total coverage snapshot 95% with `cli.py` at 99% and remaining misses limited to integration scaffolding.)
- 2025-09-21 07:37 UTC — `python -m pytest --cov=. --cov-report=term-missing` (118 passed, 8 skipped; coverage steady at 95% with gaps in CLI verbose path, config/env fallbacks, setup progress output, and intentionally skipped integration tests.)
- 2025-09-21 07:37 UTC — `uvx mypy .` (92 errors unchanged; all due to missing third-party stubs for pytest/httpx/tenacity/semantic_text_splitter/langcodes/platformdirs/tomli_w/loguru/rich/requests plus deliberate dynamic `Chat.completions` usage and example exports.)
- 2025-09-21 07:38 UTC — `uvx bandit -r .` (316 Low-severity findings covering expected test `assert` usage and the config backup `try/except/pass` guard; Medium/High severities clear.)
- 2025-09-21 07:38 UTC — Removed `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.benchmarks`, `.coverage` during /cleanup.
- 2025-09-21 07:30 UTC — `python -m pytest -xvs` (118 passed, 8 skipped; `cli.py` coverage advanced to 99% and `config.py` to 98%, total coverage 95%.)
- 2025-09-21 07:31 UTC — `python -m pytest --cov=. --cov-report=term-missing` (118 passed, 8 skipped; coverage steady at 95% with newly added CLI/config tests closing previously uncovered lines.)
- 2025-09-21 07:31 UTC — `python -m pytest tests/test_cli.py -k "config_commands or string_branches" -xvs` (2 passed; targeted verification for ConfigCommands round-trip and single-provider branches.)
- 2025-09-21 07:31 UTC — `python -m pytest tests/test_config.py -k recurses -xvs` (1 passed; confirmed recursive credential resolution logs missing env once and returns stored secret.)
- 2025-09-21 07:32 UTC — `uvx mypy .` (92 errors unchanged, all due to missing third-party stubs and intended dynamic attributes.)
- 2025-09-21 07:32 UTC — `uvx bandit -r .` (316 Low-severity findings: deliberate `assert` usage in tests and config backup fallback; Medium/High severities clear.)
- 2025-09-21 07:32 UTC — Removed `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.benchmarks`, `.coverage` during /cleanup.
- 2025-09-21 07:20 UTC — `python -m pytest -xvs` (116 passed, 8 skipped; inline coverage snapshot 95% overall with remaining misses concentrated in CLI/config/engine helper branches and intentionally skipped integrations.)
- 2025-09-21 07:21 UTC — `python -m pytest --cov=. --cov-report=term-missing` (116 passed, 8 skipped; total coverage confirmed at 95% with uncovered lines highlighted in CLI verbose paths, config fallbacks, engine retry logic, setup progress messages, and integration scaffolding.)
- 2025-09-21 07:22 UTC — `uvx mypy .` (92 errors stemming from missing third-party stubs for pytest/httpx/tenacity/semantic_text_splitter/langcodes/platformdirs/tomli_w/loguru/rich/requests plus intentional `Chat.completions` attribute lookups and dynamically exported example helpers.)
- 2025-09-21 07:23 UTC — `uvx bandit -r .` (308 Low-severity findings covering deliberate `assert` usage throughout tests and the guarded config backup fallback; Medium/High severities remain clear.)
- 2025-09-21 07:24 UTC — Removed `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.benchmarks`, `.coverage` during /cleanup following verification sweep.
- 2025-09-21 07:08 UTC — `python -m pytest -xvs` (112 passed, 8 skipped; coverage snapshot 94% with remaining misses isolated to CLI/config/engine helpers and intentionally skipped integration flows).
- 2025-09-21 07:09 UTC — `python -m pytest --cov=. --cov-report=term-missing` (112 passed, 8 skipped; overall coverage 94% with uncovered lines reported for CLI render fallbacks, config defaults, engine catalog/provider aggregation, setup progress output, and integration placeholders).
- 2025-09-21 07:10 UTC — `uvx mypy .` (92 errors expected from missing third-party stubs for pytest/httpx/tenacity/semantic_text_splitter/langcodes/rich/platformdirs/tomli_w/loguru/requests plus intentional mocked `Chat.completions` attributes and dynamically exported example helpers).
- 2025-09-21 07:10 UTC — `uvx bandit -r .` (300 Low-severity findings covering deliberate test asserts and the guarded config backup fallback; Medium/High severities remain clear).
- 2025-09-21 07:16 UTC — Added CLI shell coverage tests (`tests/test_cli.py`) to cover pipeline errors, setup forwarding, and Fire entrypoints; `cli.py` coverage now 96% (full suite: `python -m pytest -xvs`, `python -m pytest --cov=. --cov-report=term-missing`).
- 2025-09-21 04:53 UTC — `python -m pytest -xvs` (109 passed, 8 skipped; coverage plugin snapshot 94% overall with remaining gaps limited to CLI helper branches, engine retry paths, setup prompts, and intentionally skipped integration flows).
- 2025-09-21 04:55 UTC — `python -m pytest --cov=. --cov-report=term-missing` (109 passed, 8 skipped; total coverage steady at 94% with uncovered lines enumerated across CLI/config/engine helpers plus integration placeholders).
- 2025-09-21 04:56 UTC — `uvx mypy .` (expected 40+ errors driven by missing third-party stubs for pytest/httpx/tenacity/semantic_text_splitter/langcodes/rich/platformdirs/tomli_w/loguru and mocked `Chat.completions` attributes in tests/openai shim).
- 2025-09-21 04:57 UTC — `uvx bandit -r .` (292 Low-severity findings: deliberate `assert` usage across tests and the guarded config backup fallback; no Medium/High issues).
- 2025-09-21 05:00 UTC — `python -m pytest -k "render_results or collect_engine_entries or chunk_size_for" -xvs` (5 passed; targeted smoke verifying new coverage-focused tests).
- 2025-09-21 05:01 UTC — `python -m pytest -xvs` (112 passed, 8 skipped; CLI coverage 92%, `engines.py` 92%, and new tests landed at 100% coverage).
- 2025-09-21 05:02 UTC — `python -m pytest --cov=. --cov-report=term-missing` (112 passed, 8 skipped; total coverage steady at 94% with residual misses isolated to CLI/setup helper branches and intentional integration skips).
- 2025-09-21 05:03 UTC — `uvx mypy .` (unchanged 40+ errors stemming from missing third-party stubs and mocked `Chat.completions` helpers).
- 2025-09-21 05:04 UTC — `uvx bandit -r .` (300 Low-severity findings reflecting expanded test asserts and existing backup fallback handling; still no Medium/High issues).
- Added `tests/test_cli.py::test_render_results_lists_destinations`, `tests/test_cli.py::test_collect_engine_entries_accepts_single_provider_string`, and `tests/test_engines.py::test_engine_base_chunk_size_prefers_html_then_plain` to close remaining coverage gaps in `_render_results`, translator provider string handling, and `EngineBase.chunk_size_for`.
- 2025-09-21 06:13 UTC — `python -m pytest -xvs` (96 passed, 8 skipped; coverage plugin summary 93% overall, remaining misses centred on CLI/config/engine helpers and intentionally skipped integrations).
- 2025-09-21 06:15 UTC — `python -m pytest --cov=. --cov-report=term-missing` (96 passed, 8 skipped; total coverage 93% with uncovered lines enumerated across CLI/config/engine modules and integration skips).
- 2025-09-21 06:18 UTC — `uvx mypy .` (70+ errors: missing third-party stubs for pytest/httpx/tenacity/langcodes/rich/platformdirs/tomli_w/loguru plus `Chat.completions` attribute assumptions in `openai_lite.py` and tests).
- 2025-09-21 06:19 UTC — `uvx bandit -r .` (264 Low-severity findings: intentional `assert` usage throughout tests and fallback backup handler in `config.py`).
- 2025-09-21 06:25 UTC — `python -m pytest -xvs` (103 passed, 8 skipped; coverage plugin summary 94% overall with `config.py` 94%, `engine_catalog.py` 93%, `cli.py` 90%).
- 2025-09-21 06:26 UTC — `python -m pytest --cov=. --cov-report=term-missing` (103 passed, 8 skipped; total coverage 94% with residual misses limited to integration skips and a few CLI/config helper branches).
- 2025-09-21 06:26 UTC — Added regression tests for config fallback logging (`tests/test_config.py`), translator provider collection (`tests/test_engine_catalog.py`), and CLI engine filters (`tests/test_cli.py`), lifting coverage across `config.py`, `engine_catalog.py`, and `cli.py`.
- 2025-09-21 06:27 UTC — `uvx mypy .` (unchanged 70+ errors driven by missing third-party stubs and stubbed helper attributes).
- 2025-09-21 06:27 UTC — `uvx bandit -r .` (273 Low-severity findings: expected test asserts plus config backup fallback; no Medium/High issues).
- Added `tests/test_pipeline.py::test_translate_path_errors_on_unreadable_file` to assert permission errors raise `PipelineError` with path context (POSIX-only due to chmod semantics).
- Exercised `_persist_output` write-over and dry-run branches via new pipeline tests, ensuring source files update in-place or remain untouched during dry run while voc sidecars honour flags.
- Expanded `tests/test_examples.py` to mock all documented flows plus CLI usage, boosting `examples/basic_api.py` coverage to 98% without network dependencies.
- 2025-09-21 05:52 UTC — `python -m pytest -xvs` (86 passed, 8 skipped; coverage plugin reported 92% overall with warnings solely from config reset fallbacks.)
- 2025-09-21 05:53 UTC — `python -m pytest --cov=. --cov-report=term-missing` (86 passed, 8 skipped; total coverage held at 92%, misses confined to `examples/basic_api.py`, CLI/config/setup seams, and intentionally skipped integration flows.)
- 2025-09-21 05:54 UTC — `uvx mypy .` (70 errors remaining, primarily missing third-party stubs for pytest/httpx/tenacity/langcodes/rich and strict Optional handling in CLI/examples.)
- 2025-09-21 05:54 UTC — `uvx bandit -r .` (234 Low-severity findings corresponding to deliberate `assert` usage in tests and the guarded backup writer in `config.py`.)
- Ran `python -m pytest -xvs` — 78 passed, 8 skipped, 0 failed; coverage plugin snapshot at 92% overall with remaining misses concentrated in `cli.py`, `config.py`, `engine_catalog.py`, `engines.py`, `pipeline.py`, `setup.py`.
- Ran `python -m pytest --cov=. --cov-report=term-missing` — confirmed 92% total coverage and captured exact uncovered lines for follow-up.
- Ran `uvx mypy .` — surfaced 74 errors driven by missing third-party stubs (pytest, httpx, tenacity, langcodes, rich) plus strict Optional/type issues that need triage.
- Ran `uvx bandit -r .` — reported 204 Low-severity findings (intentional `assert` usage in tests, backup fallback `try/except/pass`).
- Removed transient artifacts `.pytest_cache`, `.mypy_cache`, `.benchmarks`, `.coverage` after test suite completed.
- Added CLI helper tests for pattern/json parsing, empty-state rendering, and ensured single-provider configs populate `_collect_engine_entries` correctly.
- 2025-09-21 05:33 UTC — `python -m pytest -xvs` (83 passed, 8 skipped; coverage plugin 93% overall after rerunning with extended timeout).
- 2025-09-21 05:35 UTC — `python -m pytest --cov=. --cov-report=term-missing` (83 passed, 8 skipped; total coverage steady at 93% with misses isolated to CLI/config/pipeline/setup hot spots and integration fixtures).
- 2025-09-21 05:37 UTC — `uvx mypy .` (72 errors; dominated by missing stubs for pytest/httpx/tenacity/langcodes/rich and attribute/type mismatches in `openai_lite.py`, `cli.py`, `tests/test_engines.py`, `tests/test_setup.py`, and examples).
- 2025-09-21 06:35 UTC — `python -m pytest -xvs` (103 passed, 8 skipped; coverage plugin summary 94% overall with remaining misses concentrated in CLI/config/engine helpers and integration skips).
- 2025-09-21 06:36 UTC — `python -m pytest --cov=. --cov-report=term-missing` (103 passed, 8 skipped; total coverage 94%, uncovered lines documented for CLI helper branches, config defaults, engine fallbacks, setup prompts, and intentionally partial integration tests).
- 2025-09-21 06:37 UTC — `uvx mypy .` (92 errors: dominated by missing third-party stubs for pytest/httpx/tenacity/semantic_text_splitter/langcodes/rich/platformdirs/tomli_w/loguru plus expected `Chat.completions` attribute lookups and stubbed example exports).
- 2025-09-21 06:37 UTC — `uvx bandit -r .` (273 Low-severity findings; expected test `assert` usage and the guarded backup writer fallback in `config.py`; no Medium/High findings).
- 2025-09-21 06:38 UTC — Removed `.pytest_cache`, `.mypy_cache`, `.benchmarks`, `.coverage`, `.ruff_cache` during /cleanup following the verification sweep.
- 2025-09-21 06:44 UTC — `python -m pytest -xvs` (109 passed, 8 skipped; coverage plugin summary 94% overall with `config.py` 97% and `engine_catalog.py` 95% after new fallback/aggregation tests).
- 2025-09-21 06:45 UTC — `python -m pytest --cov=. --cov-report=term-missing` (109 passed, 8 skipped; total coverage steady at 94% with remaining misses confined to CLI helper branches, engine retry paths, setup prompts, and intentionally skipped integrations).
- 2025-09-21 06:45 UTC — `uvx mypy .` (92 errors unchanged; missing third-party stubs plus expected mocked attribute lookups across openai/httpx/tenacity/langcodes/rich/platformdirs/tomli_w/loguru and fixture helper projections).
- 2025-09-21 06:46 UTC — `uvx bandit -r .` (292 Low-severity findings reflecting intentional asserts in tests and config backup fallback; no Medium/High findings).
- Added regression tests for `Defaults.from_dict(None)`, `EngineConfig.from_dict(name, None)`, `Credential.to_dict`/`Credential.from_any`, and `collect_deep_translator_providers(include_paid=True)` raising config coverage to 97% and engine catalog coverage to 95%.
- 2025-09-21 06:46 UTC — Removed `.pytest_cache`, `.mypy_cache`, `.benchmarks`, `.coverage`, `.ruff_cache` during post-verification /cleanup.
- 2025-09-21 05:38 UTC — `uvx bandit -r .` (221 Low issues; primarily deliberate `assert` usage in tests and the guarded backup writer in `config.py`).
- Added `tests/test_pipeline.py::test_translate_path_handles_mixed_formats` to cover TXT+HTML flows with the dummy engine, lifting `pipeline.py` coverage to 96% and guarding output path handling.
- Introduced `examples/basic_api.format_example_doc` with fallback messaging plus `tests/test_examples.py` to prevent `.strip()` on `None` docstrings in example listings.
- Guarded `tests/test_setup.py::test_generate_config_uses_fallbacks` against `None` credentials, clearing the prior mypy union-attr warning (remaining failures come from missing third-party stubs).

### Changed
- Normalized engine selectors to canonical short forms (`tr/*`, `dt/*`, `ll/*`, `hy`) with automatic config migration and CLI output displaying short families only.
- Added `--family`/`--configured-only` filters to `abersetz engines` and surfaced popular language hints in `abersetz lang`.
- Switched persisted configuration from JSON to TOML with automatic migration for existing installs.
- Added TOML parser/serializer dependencies (`tomli` fallback and `tomli-w`) to support the new format.
- Simplified CLI syntax so the target language is the first positional argument (e.g. `abtr de file.md`).
- Dropped legacy JSON configuration support; only `config.toml` is produced and read.
- Enriched setup discovery output with provider pricing hints sourced from the `external/` research bundle and displayed them in the summary table.
- Documented validation command usage with guidance on limiting selectors for offline smoke tests.

### Added
- Selector alias utilities ensuring legacy selectors remain accepted while tests cover normalization and CLI rendering.
- `abersetz lang` command listing supported language codes and their English names.
- `abersetz setup` command for automatic configuration discovery and initialization
  - Scans environment for API keys from 13+ providers
  - Tests discovered endpoints with /models calls
  - Generates optimized config based on available services
  - Interactive table display of discovered services
  - Supports --non-interactive mode for CI/automation
- `abersetz validate` command that exercises every configured selector, renders a rich validation table, and now runs automatically after setup completes so users receive immediate pass/fail feedback.
- `examples/validate_report.sh` helper to capture validation output for quick audits or CI artifacts.
- Comprehensive test suites for the setup wizard and `openai_lite` shim covering success/error flows, interactive output, and fallback heuristics.

### Fixed
- Fixed `abersetz config path` command double output issue by removing redundant console.print call
- Fixed `abersetz config show` to output TOML format instead of JSON
- Fixed `tomli_w.dumps()` call by removing unsupported `sort_keys` parameter
- Added `__main__.py` to enable `python -m abersetz` execution
- Fixed CLI test that was calling tr method with incorrect argument order
- Hardened setup wizard flow so validation failures log actionable warnings while preserving non-interactive execution.

### Performance Optimizations
- **Achieved 17x startup performance improvement**: Import time reduced from 8.5s to 0.43s
  - Replaced heavyweight OpenAI SDK with lightweight httpx-based client (saved 7.6s)
  - Implemented lazy imports for translation engines (translators, deep-translator)
  - Added module-level `__getattr__` in `__init__.py` for deferred loading
  - Created fast CLI entry point for instant --version checks
- **Engine shortcuts added**: Use `tr/*`, `dt/*`, `ll/*` instead of full names
- **Fixed `abersetz engines` output**: Removed duplicate object representations
- **Improved table formatting**: Standardized display with checkmarks and better styling

### Planning
- Comprehensive startup optimization plan created to reduce import time from 8.5s to <1s
  - Identified OpenAI SDK as primary bottleneck (7.6s, 89% of startup time)
  - Designed 7-phase refactoring with lazy imports and OpenAI SDK replacement
  - Planned httpx-based lightweight OpenAI client implementation
  - Documented module-level `__getattr__` patterns for deferred imports
  - Created detailed implementation roadmap with performance targets

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
