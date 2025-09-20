---
this_file: TODO.md
---
## Completed MVP Tasks
- [x] Scaffold config module with platformdirs persistence and tests.
- [x] Implement file discovery, HTML detection, and chunking helpers with coverage.
- [x] Integrate translation engines (translators, deep-translator, hysf, ullm) behind a common interface.
- [x] Assemble translation pipeline handling vocabulary propagation, outputs, and ``--save-voc``.
- [x] Wire Fire-based CLI entrypoint and console script exposing translate workflow.
- [x] Populate ``examples/`` with sample inputs, outputs, and walkthrough README snippet.
- [x] Refresh README, CLAUDE, and supporting docs to match new functionality.
- [x] Run full pytest + coverage, record results in WORK.md and finalize cleanup.

## Quality Improvements
- [x] Improve error handling for malformed config files and missing API keys
- [x] Add retry mechanism for translators/deep-translator engines
- [x] Create integration tests for real translation engines (with skip markers for CI)

## Small-Scale Quality Enhancements
- [x] Add input validation for language codes to prevent invalid language errors
- [x] Add progress indicator for multi-file translations using rich.progress
- [x] Add a `--version` flag to CLI that shows abersetz version
- [x] Reduce logging and rich output to minimum for cleaner interface

## Reliability & Robustness Improvements
- [x] Add input file validation to check existence and readability before translation
- [x] Add graceful handling of edge cases (empty files, very large files >10MB)
- [x] Add offline smoke test to verify installation without network access

## Smart Configuration Setup
- [ ] Implement `abersetz setup` command for automatic configuration discovery
- [ ] Scan environment variables for API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, SILICONFLOW_API_KEY, etc.)
- [ ] Test discovered endpoints with lightweight /models calls
- [ ] Auto-detect available translation engines based on found credentials
- [ ] Create interactive setup with rich console showing discovered services
- [ ] Generate optimized config with proper engine priorities and chunk sizes
- [ ] Test each configured engine with minimal translation to verify functionality
- [ ] Allow non-interactive mode for CI/automation with --non-interactive flag
- [ ] Add provider discovery based on patterns from external/dump_models.py
