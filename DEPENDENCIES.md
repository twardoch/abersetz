---
this_file: DEPENDENCIES.md
---
# Dependencies

## Production Dependencies

### Translation Engines
- **translators** (>=5.9): Provides access to multiple free translation APIs (Google, Bing, Baidu, etc.) through a unified interface. Core requirement for free translation capabilities.
- **deep-translator** (>=1.11): Alternative translation library with support for additional providers including DeepL. Provides fallback options and file translation utilities.
- **httpx** (>=0.25): Modern HTTP client with sync/async support. Replaces the heavyweight OpenAI SDK with a lightweight implementation, reducing import time by 7.6 seconds.

### CLI and User Interface
- **fire** (>=0.5): Google's Python Fire library for automatic CLI generation from functions. Minimal boilerplate, automatic help generation, and intuitive command structure.
- **rich** (>=13.9): Rich terminal formatting and progress indicators. Provides beautiful console output with tables, progress bars, and colored text.
- **langcodes** (>=3.4): Mature language metadata with CLDR coverage, powering the `abersetz lang` listing without maintaining custom tables.

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

2. **LLM Support**: The lightweight httpx-based client layer (no heavyweight SDKs) keeps LLM-driven translation profiles available without slowing startup or bloating dependencies.

3. **Developer Experience**: `fire` and `rich` create an intuitive CLI with minimal code. `loguru` simplifies debugging without complex logging configuration.

4. **Reliability**: `tenacity` ensures the tool handles network issues gracefully, while `semantic-text-splitter` maintains translation quality by preserving context.

5. **Cross-Platform**: `platformdirs` ensures the tool works correctly on Windows, macOS, and Linux without platform-specific code.

6. **Code Quality**: The development dependencies ensure high code quality through testing (91% coverage) and automatic formatting/linting.

## Verification Log
- 2025-09-21 11:03 UTC — /work reliability polish sweep (pytest, coverage, mypy, bandit) confirmed no dependency changes; improvements limited to tests and typing helpers.
- 2025-09-21 08:46 UTC — /report QA sweep (pytest, coverage, mypy, bandit) confirmed dependency roster unchanged; no new packages introduced.
- 2025-09-21 10:38 UTC — /work iteration adjusted tests only; dependency roster remains unchanged after QA sweep.
- 2025-09-21 10:29 UTC — /report QA sweep (pytest, coverage, mypy, bandit) confirmed dependency roster unchanged; no new packages introduced.
- 2025-09-21 08:06 UTC — Post-/work QA sweep (pytest, coverage, mypy, bandit) introduced only tests; dependency roster remains unchanged.
- 2025-09-21 07:59 UTC — /report sweep reran full QA (pytest, coverage, mypy, bandit); dependency roster unchanged with no new packages introduced.
- 2025-09-21 05:38 UTC — Reviewed dependency roster during /report; no additions or removals required.
- 2025-09-21 05:50 UTC — Revalidated after quality guardrails sprint; no dependency changes introduced by new tests or helpers.
- 2025-09-21 06:19 UTC — /report sweep confirmed dependency list remains accurate; no additions or removals required for latest verification run.
- 2025-09-21 06:27 UTC — Post-/work regression tests touched only test code; dependency roster unchanged.
- 2025-09-21 06:38 UTC — /report verification: reran full test/coverage/mypy/bandit sweep; dependency lineup unchanged with no new packages introduced.
- 2025-09-21 06:46 UTC — Configuration hardening tests added without altering dependencies; latest verification sweep confirms package set remains stable.
