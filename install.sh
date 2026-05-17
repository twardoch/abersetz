#!/usr/bin/env bash
# install.sh — Install abersetz locally
# abersetz is a multi-engine text translation CLI tool with chunking support
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Installing abersetz..."
uv pip install -e . 2>/dev/null || pip install -e . 2>/dev/null || echo "Install failed"
echo "Done."
