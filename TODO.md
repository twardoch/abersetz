---
this_file: TODO.md
---
## Startup Time Optimization - Lazy Import Refactoring

### Phase 0:

- [x] Implement @issues/105.txt
  - [x] Fix abersetz engines command to remove duplicate object reprs
  - [x] Standardize table format with checkmarks and better styling
  - [x] Implement engine name shortcuts (tr/*, dt/*, ll/*)

### Phase 1: Module-Level Lazy Loading
- [x] Implement lazy `__init__.py` with `__getattr__` pattern
- [x] Replace direct imports with deferred attribute access
- [x] Maintain `__all__` for IDE support and discoverability
- [x] Move heavy imports in `engines.py` inside engine creation functions
- [ ] Implement module-level `__getattr__` for engine classes
- [ ] Create graceful import helpers with helpful error messages
- [ ] Defer imports in `cli.py` until command execution
- [ ] Move langcodes import to `lang` command only
- [ ] Implement conditional imports based on CLI arguments
- [ ] Verify: Basic `import abersetz` under 0.5 seconds

### Phase 2: OpenAI SDK Replacement
- [x] Analyze current OpenAI usage in `LlmEngine` and `HysfEngine`
- [x] Document required API surface (chat completions only)
- [x] Study httpx examples from external/302-py-httpx.md
- [x] Create `openai_lite.py` with minimal OpenAI-compatible API
- [x] Use httpx for HTTP client with async support
- [x] Support both sync and async patterns for compatibility
- [x] Implement retry logic with tenacity
- [x] Update `engines.py` to use new lightweight client
- [x] Maintain exact same interface for `_make_openai_client`
- [ ] Add configuration option to use original OpenAI SDK if needed
- [x] Verify: Engine creation under 1 second total

### Phase 3: Engine Factory Optimization
- [x] Move `translators` import to `TranslatorsEngine.__init__`
- [x] Move `deep_translator` imports to `DeepTranslatorEngine.__init__`
- [x] Move `langcodes` import to language name resolution functions
- [ ] Create engine registry mapping names to factory functions
- [ ] Factory functions handle their own imports and dependencies
- [ ] Lazy load engine configurations only when needed
- [ ] Graceful degradation when optional dependencies missing
- [ ] Helpful error messages pointing to installation commands
- [ ] Runtime detection of available engines
- [ ] Verify: `abersetz --help` under 0.3 seconds

### Phase 4: CLI Command Isolation
- [ ] `setup` command: Only import setup-related modules
- [ ] `config` command: Only import config and tomli_w
- [ ] `lang` command: Only import langcodes when executed
- [ ] `engines` command: Only import engine catalog when needed
- [ ] Implement lazy command class loading
- [ ] Defer heavy imports until command method execution
- [ ] Use dynamic imports based on command line arguments
- [ ] Make `--version` extremely fast (under 0.1s)
- [ ] Only import version information, no other modules
- [ ] Verify: `abersetz --version` under 0.1s, `abersetz setup` under 0.5s

### Phase 5: Advanced Lazy Patterns
- [ ] Only load config when actually needed by commands
- [ ] Defer platformdirs and file I/O until config access
- [ ] Cache loaded configuration to avoid repeated I/O
- [ ] Only import `semantic_text_splitter` when doing actual translation
- [ ] Implement fallback chunking that doesn't require external dependencies
- [ ] Lazy load format detection utilities
- [ ] Analyze import dependency graph
- [ ] Minimize transitive imports through careful ordering
- [ ] Use `importlib.import_module` for dynamic loading
- [ ] Verify: All commands under target times, full functionality preserved

### Phase 6: OpenAI Lite Implementation Details
- [ ] Implement httpx.AsyncClient for async operations
- [ ] Add connection pooling and timeout configuration
- [ ] Implement retry logic with exponential backoff
- [ ] Support streaming responses for chat completions
- [ ] Create drop-in replacement API compatible with current usage
- [ ] Test both sync and async code paths
- [ ] Add comprehensive error handling and logging
- [ ] Performance test against original OpenAI SDK
- [ ] Document API differences and migration notes

### Phase 7: Performance Validation
- [ ] Create startup time measurement script
- [ ] Test all CLI commands for performance regression
- [ ] Validate functionality with existing test suite
- [ ] Test missing optional dependencies scenarios
- [ ] Verify error messages are still helpful
- [ ] Test lazy loading under various Python versions
- [ ] Update DEPENDENCIES.md with new optional dependencies
- [ ] Document lazy loading patterns for maintainers
- [ ] Add troubleshooting guide for import issues

### Performance Targets
- [x] `import abersetz`: < 0.5 seconds (achieved: 0.495s from 8.5s)
- [ ] `abersetz --version`: < 0.1 seconds
- [ ] `abersetz --help`: < 0.3 seconds
- [ ] `abersetz setup`: < 0.5 seconds
- [ ] `abersetz tr --dry-run`: < 1.0 seconds

### Quality Assurance
- [ ] Zero regression: All existing functionality preserved
- [ ] Same API: No breaking changes to public interface
- [ ] Better errors: Improved error messages for missing dependencies
- [ ] Optional deps: Graceful degradation when engines not available
- [ ] Comprehensive test coverage for lazy loading patterns
- [ ] Cross-platform compatibility validation
- [ ] Memory usage analysis and optimization

## Completed MVP Tasks
- [x] Scaffold config module with platformdirs persistence and tests.
- [x] Implement file discovery, HTML detection, and chunking helpers with coverage.
- [x] Integrate translation engines (translators, deep-translator, hysf, ullm) behind a common interface.
- [x] Assemble translation pipeline handling voc propagation, outputs, and ``--save-voc``.
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
- [x] Implement `abersetz setup` command for automatic configuration discovery
- [x] Scan environment variables for API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY, SILICONFLOW_API_KEY, etc.)
- [x] Test discovered endpoints with lightweight /models calls
- [x] Auto-detect available translation engines based on found credentials
- [x] Create interactive setup with rich console showing discovered services
- [x] Generate optimized config with proper engine priorities and chunk sizes
- [x] Allow non-interactive mode for CI/automation with --non-interactive flag
- [x] Add provider discovery based on patterns from external/dump_models.py