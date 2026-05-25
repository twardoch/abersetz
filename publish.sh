#!/usr/bin/env bash
# this_file: publish.sh
# publish.sh — Build, install, and publish abersetz to PyPI
# abersetz is a multi-engine text translation CLI tool with chunking support
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Cleaning previous builds..."
rm -rf dist

echo "Building and testing..."
bash "$SCRIPT_DIR/build.sh"

echo "Installing..."
bash "$SCRIPT_DIR/install.sh"

echo "Tagging next version..."
uvx gitnextver@latest

echo "Cleaning dev build before release build..."
rm -rf dist

echo "Building release package..."
uvx hatch build

echo "Publishing to PyPI..."
uv publish

echo "Done."
