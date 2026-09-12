#!/usr/bin/env bash
# this_file: test.sh
set -euo pipefail
cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")"
test_python=$(uvx hatch run hatch-test.py3.12:python -c 'import sys; print(sys.executable)')
uubed_source=../uubed-project/uubed-all/uubed-py
native_source=../uubed-project/uubed-all/uubed-rs
if [[ -f "$uubed_source/pyproject.toml" && -f "$native_source/Cargo.toml" ]]; then
    wheels=$(mktemp -d)
    trap 'rm -rf "$wheels"' EXIT
    (cd "$native_source" && uvx maturin build --release --out "$wheels" --interpreter python3.12)
    uv pip install --python "$test_python" --reinstall-package uubed-rs -e "$uubed_source" "$wheels"/*.whl 'turbovec==1.0.0'
else
    uv pip install --python "$test_python" 'uubed[tm]>=1.0.6' 'turbovec==1.0.0'
fi
uvx hatch test -py 3.12
