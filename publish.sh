#!/usr/bin/env bash
# publish.sh — Build, install, and publish abersetz to PyPI
# abersetz is a multi-engine text translation CLI tool with chunking support
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Building..."
bash "$SCRIPT_DIR/build.sh"

echo "Installing..."
bash "$SCRIPT_DIR/install.sh"

echo "Tagging next version..."
uvx gitnextver@latest

echo "Publishing to PyPI..."
uvx hatch build
uv publish

echo "Done."
