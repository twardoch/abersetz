---
this_file: CHANGELOG.md
---
# Changelog

All notable changes to abersetz will be documented in this file.

## [Unreleased]

### Changed
- Switched persisted configuration from JSON to TOML with automatic migration for existing installs.
- Added TOML parser/serializer dependencies (`tomli` fallback and `tomli-w`) to support the new format.
- Simplified CLI syntax so the target language is the first positional argument (e.g. `abtr de file.md`).
- Dropped legacy JSON configuration support; only `config.toml` is produced and read.

### Added
- `abersetz lang` command listing supported language codes and their English names.

### Fixed
- Fixed `abersetz config path` command double output issue by removing redundant console.print call
- Fixed `abersetz config show` to output TOML format instead of JSON
- Fixed `tomli_w.dumps()` call by removing unsupported `sort_keys` parameter
- Added `__main__.py` to enable `python -m abersetz` execution
- Fixed CLI test that was calling tr method with incorrect argument order

## [0.1.0] - 2025-01-20

### Added
- Initial release of abersetz - minimalist file translator
- Core translation pipeline with locate → chunk → translate → merge workflow
- Support for multiple translation engines:
  - translators library (Google, Bing, etc.)
  - deep-translator library (DeepL, Google Translate, etc.)
  - Custom hysf engine using Siliconflow API
  - Custom ullm engine for LLM-based translation with vocabulary management
- Automatic file discovery with recursive globbing and include/exclude filters
- HTML vs plain-text detection for markup preservation
- Semantic chunking using semantic-text-splitter for better context boundaries
- Vocabulary-aware translation pipeline with JSON vocabulary propagation
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
- Optional vocabulary sidecar files with --save-voc flag
- Retry logic with tenacity for robust API calls
