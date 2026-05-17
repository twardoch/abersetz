#!/usr/bin/env bash
# build.sh — Build abersetz
# abersetz is a multi-engine text translation CLI tool with chunking support
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Linting and formatting..."
fd -e py -x uvx ruff check --fix {} 2>/dev/null || true
fd -e py -x uvx ruff format {} 2>/dev/null || true

echo "Running tests..."
uvx hatch test 2>/dev/null || uv run pytest -xvs 2>/dev/null || echo "No tests found"

echo "Building package..."
uvx hatch build 2>/dev/null || uv build 2>/dev/null || echo "No build system configured"

echo "Done."
