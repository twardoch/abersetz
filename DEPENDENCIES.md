---
this_file: DEPENDENCIES.md
---
# Dependencies

## Production Dependencies

### Translation Engines
- **translators** (>=5.9): Provides access to multiple free translation APIs (Google, Bing, Baidu, etc.) through a unified interface. Core requirement for free translation capabilities.
- **deep-translator** (>=1.11): Alternative translation library with support for additional providers including DeepL. Provides fallback options and file translation utilities.
- **openai** (>=1.51): Official OpenAI client library, used for custom LLM-based translation engines (hysf, ullm) that connect to Siliconflow and other OpenAI-compatible endpoints.

### CLI and User Interface
- **fire** (>=0.5): Google's Python Fire library for automatic CLI generation from functions. Minimal boilerplate, automatic help generation, and intuitive command structure.
- **rich** (>=13.9): Rich terminal formatting and progress indicators. Provides beautiful console output with tables, progress bars, and colored text.

### Core Utilities
- **loguru** (>=0.7): Simple yet powerful logging with minimal setup. Provides structured logging with automatic rotation, retention, and colored output.
- **platformdirs** (>=4.3): Cross-platform user directories for configuration storage. Ensures config files are stored in appropriate OS-specific locations.
- **tomli-w** (>=1.0): Lightweight TOML serializer used to persist configuration data in the new `config.toml` format without writing custom emitters.
- **tomli** (>=2.0, Python <3.11 only): Backports the standard library TOML parser for Python 3.10 environments, guaranteeing consistent config loading across supported versions.
- **semantic-text-splitter** (>=0.7): Intelligent text chunking that respects semantic boundaries. Critical for maintaining context in translation chunks.
- **tenacity** (>=8.4): Robust retry logic with exponential backoff. Essential for handling transient API failures and rate limits.

## Development Dependencies

### Testing
- **pytest** (>=8.3): Modern testing framework with powerful fixtures and plugins. Industry standard for Python testing.
- **pytest-cov** (>=6.0): Coverage plugin for pytest. Ensures code quality with coverage reports.

### Code Quality
- **ruff** (>=0.9): Fast Python linter and formatter combining multiple tools. Replaces black, flake8, isort, and more.
- **mypy** (>=1.10): Static type checker for Python. Catches type errors before runtime.

## Why These Packages?

1. **Multiple Translation Backends**: Having both `translators` and `deep-translator` provides redundancy and access to different translation providers. Users can choose based on availability, quality, or cost.

2. **LLM Support**: The `openai` client enables advanced LLM-based translation with vocabulary management, providing higher quality for specialized content.

3. **Developer Experience**: `fire` and `rich` create an intuitive CLI with minimal code. `loguru` simplifies debugging without complex logging configuration.

4. **Reliability**: `tenacity` ensures the tool handles network issues gracefully, while `semantic-text-splitter` maintains translation quality by preserving context.

5. **Cross-Platform**: `platformdirs` ensures the tool works correctly on Windows, macOS, and Linux without platform-specific code.

6. **Code Quality**: The development dependencies ensure high code quality through testing (91% coverage) and automatic formatting/linting.
