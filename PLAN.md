---
this_file: PLAN.md
---
# Abersetz Startup Time Optimization Plan

## Phase 0: 

- [ ] Implement @issues/105.txt


## Project Overview
- **Goal**: Drastically reduce abersetz startup time from current 8.5 seconds to under 1 second by implementing comprehensive lazy loading strategies
- **Core Problem**: Heavy imports (especially OpenAI SDK at 7.6s) are loaded at import time even when not needed
- **Strategy**: Implement module-level `__getattr__`, deferred imports, and replace heavyweight dependencies with lighter alternatives

## Current Performance Analysis

### Import Time Bottlenecks (Measured)
- **Total abersetz import**: 8.5 seconds
- **OpenAI package**: 7.6 seconds (89% of total time!)
- **translators package**: 2.4 seconds
- **deep_translator package**: 1.3 seconds
- **langcodes package**: 0.6 seconds
- **semantic_text_splitter**: 0.5 seconds

### Import Dependencies
- `engines.py` imports all translation libraries at module level
- `cli.py` imports engines, pipeline, and config eagerly
- `__init__.py` imports pipeline module immediately
- Engine creation happens even for unused engines

## Architecture Decisions

### Core Strategy: Lazy Everything
1. **Module-level `__getattr__`**: Defer imports until actual attribute access
2. **Engine factory pattern**: Only import engine libraries when creating that specific engine
3. **OpenAI replacement**: Replace heavyweight OpenAI SDK with lighter httpx-based implementation
4. **CLI command isolation**: Only load what's needed for the specific command being run

### Technical Approach
- **PEP 690 compatibility**: Design for future global lazy imports support
- **Backward compatibility**: Maintain exact same public API
- **Error handling**: Preserve helpful error messages for missing dependencies
- **Testing**: Ensure lazy loading doesn't break functionality

## Implementation Phases

### Phase 1: Module-Level Lazy Loading
**Goal**: Implement `__getattr__` patterns to defer heavy imports

**Tasks**:
1. **Lazy `__init__.py`**:
   - Replace direct imports with `__getattr__` implementation
   - Only import when specific attributes are accessed
   - Maintain `__all__` for IDE support

2. **Lazy `engines.py`**:
   - Move all engine library imports inside engine creation functions
   - Implement module-level `__getattr__` for engine classes
   - Create import helpers that fail gracefully with helpful messages

3. **Lazy `cli.py`**:
   - Defer imports of heavy modules until command execution
   - Move language code imports (`langcodes`) to `lang` command only
   - Implement conditional imports based on CLI arguments

**Verification**: Basic `import abersetz` should be under 0.5 seconds

### Phase 2: OpenAI SDK Replacement
**Goal**: Replace 7.6-second OpenAI import with lightweight httpx implementation

**Tasks**:
1. **Research OpenAI API patterns**:
   - Analyze current usage in `LlmEngine` and `HysfEngine`
   - Document required API surface (chat completions only)
   - Study httpx examples from external/302-py-httpx.md

2. **Implement lightweight OpenAI client**:
   - Create `openai_lite.py` with minimal OpenAI-compatible API
   - Use httpx for HTTP client with async support
   - Support both sync and async patterns for compatibility
   - Implement retry logic with tenacity

3. **Replace OpenAI imports**:
   - Update `engines.py` to use new lightweight client
   - Maintain exact same interface for `_make_openai_client`
   - Add configuration option to use original OpenAI SDK if needed

**Verification**: Engine creation should be under 1 second total

### Phase 3: Engine Factory Optimization
**Goal**: Only load engine dependencies when that engine is actually used

**Tasks**:
1. **Deferred engine imports**:
   - Move `translators` import to `TranslatorsEngine.__init__`
   - Move `deep_translator` imports to `DeepTranslatorEngine.__init__`
   - Move `langcodes` import to language name resolution functions

2. **Engine registry pattern**:
   - Create engine registry that maps names to factory functions
   - Factory functions handle their own imports and dependencies
   - Lazy load engine configurations only when needed

3. **Import error handling**:
   - Graceful degradation when optional dependencies missing
   - Helpful error messages pointing to installation commands
   - Runtime detection of available engines

**Verification**: `abersetz --help` should be under 0.3 seconds

### Phase 4: CLI Command Isolation
**Goal**: Different CLI commands only load what they need

**Tasks**:
1. **Command-specific imports**:
   - `setup` command: Only import setup-related modules
   - `config` command: Only import config and tomli_w
   - `lang` command: Only import langcodes when executed
   - `engines` command: Only import engine catalog when needed

2. **Fire optimization**:
   - Implement lazy command class loading
   - Defer heavy imports until command method execution
   - Use dynamic imports based on command line arguments

3. **Version command optimization**:
   - Make `--version` extremely fast (under 0.1s)
   - Only import version information, no other modules

**Verification**: `abersetz --version` under 0.1s, `abersetz setup` under 0.5s

### Phase 5: Advanced Lazy Patterns
**Goal**: Implement sophisticated lazy loading for maximum performance

**Tasks**:
1. **Lazy configuration loading**:
   - Only load config when actually needed by commands
   - Defer platformdirs and file I/O until config access
   - Cache loaded configuration to avoid repeated I/O

2. **Conditional chunking imports**:
   - Only import `semantic_text_splitter` when doing actual translation
   - Implement fallback chunking that doesn't require external dependencies
   - Lazy load format detection utilities

3. **Import order optimization**:
   - Analyze import dependency graph
   - Minimize transitive imports through careful ordering
   - Use `importlib.import_module` for dynamic loading

**Verification**: All commands under target times, full functionality preserved

### Phase 6: OpenAI Lite Implementation Details
**Goal**: Create production-ready OpenAI SDK replacement

**Implementation Strategy**:
- **Based on httpx patterns from external/302-py-httpx.md**:
  - Use httpx.AsyncClient for async operations
  - Implement connection pooling and timeouts
  - Add retry logic with exponential backoff
  - Support streaming responses

- **API Compatibility**:
  ```python
  # Current usage pattern in engines.py
  from openai import OpenAI
  client = OpenAI(api_key=token, base_url=base_url)
  response = client.chat.completions.create(model=model, messages=messages)

  # New lightweight implementation
  from .openai_lite import OpenAI  # Drop-in replacement
  # Same interface, much faster import
  ```

- **Core Implementation**:
  ```python
  # openai_lite.py - minimal OpenAI SDK replacement
  import httpx
  from tenacity import retry, stop_after_attempt, wait_exponential

  class OpenAI:
      def __init__(self, api_key: str, base_url: str | None = None):
          self.api_key = api_key
          self.base_url = base_url or "https://api.openai.com/v1"
          self.chat = ChatCompletions(self)

  class ChatCompletions:
      @retry(stop=stop_after_attempt(3), wait=wait_exponential())
      def create(self, model: str, messages: list, **kwargs):
          # httpx implementation here
  ```

### Phase 7: Performance Validation
**Goal**: Ensure optimization targets are met and functionality preserved

**Tasks**:
1. **Benchmark Suite**:
   - Create startup time measurement script
   - Test all CLI commands for performance regression
   - Validate functionality with existing test suite

2. **Edge Case Testing**:
   - Test missing optional dependencies
   - Verify error messages are still helpful
   - Test lazy loading under various Python versions

3. **Documentation Updates**:
   - Update DEPENDENCIES.md with new optional dependencies
   - Document lazy loading patterns for maintainers
   - Add troubleshooting guide for import issues

## Package Dependencies Strategy

### New Lightweight Dependencies
- **httpx**: Replace OpenAI SDK for HTTP client functionality
- **No new required dependencies**: All optimizations use existing packages more efficiently

### Existing Dependencies Optimization
- **Make heavy deps optional**: translators, deep-translator become optional with graceful degradation
- **Lazy loading**: All dependencies loaded only when needed
- **Import isolation**: Separate import paths for different functionality

## Performance Targets

### Import Time Goals
- `import abersetz`: < 0.5 seconds (current: 8.5s)
- `abersetz --version`: < 0.1 seconds
- `abersetz --help`: < 0.3 seconds
- `abersetz setup`: < 0.5 seconds
- `abersetz tr --dry-run`: < 1.0 seconds

### Functionality Goals
- **Zero regression**: All existing functionality preserved
- **Same API**: No breaking changes to public interface
- **Better errors**: Improved error messages for missing dependencies
- **Optional deps**: Graceful degradation when engines not available

## Risk Mitigation

### Technical Risks
- **Import timing issues**: Some modules may have hidden dependencies on import order
  - *Mitigation*: Comprehensive testing with isolated import testing
- **Lazy loading complexity**: Debugging becomes harder with deferred imports
  - *Mitigation*: Clear error messages and logging for import failures
- **Compatibility breaks**: Changes might affect edge cases
  - *Mitigation*: Extensive testing with existing test suite

### Performance Risks
- **First-use penalty**: Commands might be slower on first execution
  - *Mitigation*: Acceptable trade-off for much faster CLI startup
- **Memory usage**: Lazy loading might change memory patterns
  - *Mitigation*: Monitor and optimize if needed

## Testing Strategy

### Automated Testing
1. **Import time benchmarks**: Automated performance regression tests
2. **Lazy loading tests**: Verify modules load correctly when accessed
3. **Error handling tests**: Ensure graceful failures with missing deps
4. **Functionality tests**: All existing tests must pass

### Manual Validation
1. **CLI responsiveness**: Manual testing of common command workflows
2. **Error message quality**: Verify error messages are still helpful
3. **Cross-platform testing**: Test on different Python versions and platforms

## Success Metrics

### Primary Goals
- **8x improvement**: Import time from 8.5s to < 1s overall
- **15x improvement**: Basic commands like `--version` under 0.1s
- **Zero regression**: All tests pass, all functionality preserved

### Secondary Goals
- **Better UX**: CLI feels more responsive for all operations
- **Lower resource usage**: Reduced memory footprint for simple operations
- **Maintainability**: Code remains clear and debuggable despite lazy loading

## Future Considerations

### PEP 690 Readiness
- Design patterns compatible with future global lazy imports
- Avoid import-time side effects that break under lazy loading
- Document lazy loading patterns for future Python versions

### Further Optimizations
- **Rust extensions**: Consider rust-based alternatives for hot paths
- **Import caching**: Cache import results across CLI invocations
- **Async CLI**: Explore async CLI patterns for better concurrency

---

This plan transforms abersetz from a slow-starting tool into a lightning-fast CLI that only loads what it needs, when it needs it. The 8.5-second startup becomes a sub-second experience while preserving all functionality.