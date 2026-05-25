---
this_file: examples/README.md
---
# Abersetz Benchmark

Translation speed and cost can make or break your localization pipeline. This suite benchmarks translation engines across realistic test documents.

## Running the Benchmark

Execute the benchmark using the bundled wrapper script or Python direct invocation:

```bash
# Run a dry-run check of all engines (instant, safe, offline)
uv run python examples/benchmark.py run --dry-run

# Run full translation using specific configured engines
uv run python examples/benchmark.py run --engines "tr/google,dt/google"
```

### Options

- `--engines`: Comma-separated list of selector names (e.g. `tr/google,dt/google,hysf`). Defaults to auto-discovery.
- `--max-chunks`: Limit number of chunks processed per file (useful for rapid rate-safe testing).
- `--dry-run`: Evaluate chunking structures and pipeline speeds without hitting remote translation APIs.
- `--verbose`: Print extra pipeline logs during processing.

## Test Data

The suite uses two documents in `examples/data/`:
1. `poem/poem.en.md` - Small poetic prose, ideal for fast sanity checks.
2. `fontlab/fontlab-7-tldr.en.md` - A dense 73KB markdown guide, ideal for testing document parsing, formatting, and high-volume throughput.

Translated files are written to the respective directories as `<name>.pl--<descriptor>.md`.
Summary metrics are printed in a console table and persisted to `examples/benchmark_results.json`.
