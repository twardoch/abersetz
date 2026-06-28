---
title: Style Guide
description: Code and documentation conventions for abersetz contributors.
---

# Style Guide

## Python code

### Formatting and linting

All Python files are formatted with **ruff** (`line-length = 100`, `quote-style = "double"`) and linted with `ruff check` (`E`, `F`, `B`, `I`, `UP`, `SIM` rules). Run before committing:

```bash
uvx ruff format src tests
uvx ruff check --fix src tests
```

### Type hints

Use type hints everywhere. Prefer the built-in generics (`list`, `dict`, `tuple`) over `typing.*`. Use `|` unions, not `Optional[X]`:

```python
# Good
def translate(self, request: EngineRequest) -> EngineResult: ...
def chunk_size_for(self, fmt: TextFormat) -> int | None: ...

# Bad
from typing import Optional, List
def translate(self, request: EngineRequest) -> Optional[EngineResult]: ...
```

### Docstrings

Use one-line docstrings for simple functions, multi-line Google style for anything with parameters:

```python
def create_engine(selector: str, config: AbersetzConfig) -> Engine:
    """Build the requested engine from a selector string.

    Args:
        selector: Engine selector, e.g. ``tr::google`` or ``ll::openai:gpt-4o-mini``.
        config: Loaded abersetz configuration.

    Returns:
        Concrete engine implementing the ``Engine`` protocol.

    Raises:
        EngineError: If the selector is unknown or the credential is missing.
    """
```

Engine adapter docstrings must include:

- What API or library the engine wraps
- Whether it requires an API key (and which env var)
- Approximate cost per million characters/tokens
- Known rate limits
- Whether it works offline

### `this_file` record

Every Python file must carry a `this_file` comment near the top (after shebang/imports guard):

```python
# this_file: src/abersetz/providers/translators.py
```

### Error handling

Raise `EngineError` (from `providers.base`) for all engine-level failures. Never swallow exceptions silently unless explicitly noted in a comment explaining why.

## Tests

### Naming

```
test_<function>_when_<condition>_then_<result>
```

### Markers

- `@pytest.mark.integration` — requires network or external service; skipped in CI unless `--run-integration` is passed.
- No marker — must be hermetic (mocked / offline).

### Coverage

Target ≥ 80 % line coverage. Check with:

```bash
uvx hatch test -- --cov=src/abersetz --cov-report=term-missing
```

## Documentation

### Markdown files

- Titles: sentence case, not title case.
- Code blocks: always tagged with language (` ```bash `, ` ```python `, ` ```toml `).
- Tables: pipes aligned by ruff-style formatting is fine; readability over alignment.

### src_docs layout

```
src_docs/
  mkdocs.yaml      # MkDocs Material configuration
  md/              # Markdown source files
    index.md
    installation.md
    engines.md
    cli.md
    configuration.md
    api.md
    STYLE_GUIDE.md
  site/            # Build output (gitignored)
```

To build:

```bash
pip install mkdocs-material mkdocstrings[python]
mkdocs build --config-file src_docs/mkdocs.yaml
```

To serve locally:

```bash
mkdocs serve --config-file src_docs/mkdocs.yaml
```

## Git

- Commit messages: imperative mood, ≤72 chars subject, blank line, body if needed.
- Do not commit generated files: `llms.txt`, `ruvector.db`, `src_docs/site/`, `dist/`.
- Tag format: `v<major>.<minor>.<patch>` (managed by `hatch-vcs`).

## Release checklist

1. All tests pass: `uvx hatch test`
2. Ruff clean: `uvx ruff check src tests && uvx ruff format --check src tests`
3. CHANGELOG.md updated.
4. `git tag v<version>` and `git push --tags`.
5. `./build.sh && ./publish.sh`.
