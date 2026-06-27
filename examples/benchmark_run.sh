#!/usr/bin/env bash
# this_file: examples/benchmark_run.sh
#
# Run the full abersetz benchmark on the two sample documents.
# Prepares a job file (if missing), then benchmarks each input and writes a
# per-document JSON report.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
JOB="${HERE}/benchmark_job.json"

# Generate the job file from discovered engine combinations if it is absent.
if [[ ! -f "${JOB}" ]]; then
    echo "Generating ${JOB} ..."
    uv run "${HERE}/benchmark_prep.py" --output "${JOB}"
fi

echo "Benchmarking poem ..."
uv run "${HERE}/benchmark.py" run \
    --job "${JOB}" \
    --input "${HERE}/data/poem/poem.en.md" \
    --report "${HERE}/benchmark_poem.json" \
    "$@"

echo "Benchmarking fontlab ..."
uv run "${HERE}/benchmark.py" run \
    --job "${JOB}" \
    --input "${HERE}/data/fontlab/fontlab.en.md" \
    --report "${HERE}/benchmark_fontlab.json" \
    "$@"

echo "Done. Reports: benchmark_poem.json, benchmark_fontlab.json"
