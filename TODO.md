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
- [ ] Add input file validation to check existence and readability before translation
- [ ] Add graceful handling of edge cases (empty files, very large files >10MB)
- [ ] Add offline smoke test to verify installation without network access
