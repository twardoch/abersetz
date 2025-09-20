---
this_file: CHANGELOG.md
---
# Changelog

All notable changes to abersetz will be documented in this file.

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

### Technical Details
- Python 3.10+ support
- Semantic chunking with configurable sizes per engine
- Offline-friendly dry-run mode for testing
- Optional vocabulary sidecar files with --save-voc flag
- Retry logic with tenacity for robust API calls