# abersetz

Translate entire directories of text and Markdown files using modern AI. Feed it a folder; get back a translated folder. No boilerplate, no broken formatting.

## What it does

Abersetz takes a file or directory tree, detects the text format (plain text or HTML), slices large documents into chunks at natural sentence and paragraph boundaries, feeds each chunk to a translation engine, and stitches the results back together preserving the original layout.

Translation memory carries vocabulary terms forward across chunks so "widget" in paragraph 1 still means "widget" in paragraph 47.

## Engines

Abersetz speaks to several translation backends through a unified interface:

| Selector | What it uses |
|---|---|
| `tr/google`, `tr/bing`, … | `translators` package — scrapes web translation endpoints |
| `dt/google`, `dt/deepl`, `dt/microsoft`, … | `deep-translator` — more stable, official APIs |
| `ullm/<profile>` | Any OpenAI-compatible LLM endpoint (OpenAI, Anthropic, SiliconFlow, local Ollama) |
| `hysf` | Tencent Hunyuan via SiliconFlow API |
| `mthy/mlx`, `mthy/gguf` | Tencent Hunyuan-MT running locally (Apple Silicon or CPU via llama.cpp) |
| `gemma/mlx`, `gemma/gguf` | Google TranslateGemma running locally |

LLM engines wrap text in XML tags and extract the `<output>` block from the response, which makes them tolerant of chatty models that add extra commentary.

## Install

```bash
pip install abersetz
# or
uv pip install abersetz
```

## Quick start

```bash
# Translate a single file to Spanish using Google (via translators)
abersetz translate file.md --to-lang es --engine tr/google

# Translate a directory tree to Polish using OpenAI
abersetz translate ./docs --to-lang pl --engine ullm/openai

# Dry run — verify paths and settings without burning API credits
abersetz translate ./docs --to-lang de --dry-run

# Validate that your API keys work
abersetz validate
```

Output files land in a subdirectory named after the target language by default (e.g. `./docs/pl/`). Use `--output-dir` to redirect them, or `--write-over` to replace files in place.

## CLI reference

```
abersetz translate <path> [options]

  --engine TEXT      Engine selector, e.g. tr/google, ullm/openai, mthy/mlx
  --from-lang TEXT   Source language code (default: auto-detect)
  --to-lang TEXT     Target language code (required)
  --output-dir PATH  Where to write translated files
  --write-over       Overwrite source files instead of creating a subdirectory
  --chunk-size INT   Max tokens per chunk for LLM engines
  --save-voc         Write a .voc.json sidecar file with accumulated terminology
  --dry-run          Show what would be translated without calling any API
  --recurse / --no-recurse  Walk subdirectories (default: on)
  --xclude PATTERN   Glob pattern(s) to skip

abersetz validate    Ping all configured engines with a test phrase
abersetz list        Show available engines from config
```

## Configuration

Drop an `abersetz.toml` in your project root or `~/.config/abersetz/config.toml`. Example with OpenAI:

```toml
[defaults]
engine = "ullm/openai"
to_lang = "pl"
chunk_size = 2000

[engines.ullm.options.profiles.openai]
model = "gpt-4o-mini"
base_url = ""  # leave empty for official OpenAI endpoint

[credentials]
openai = "sk-..."  # or set OPENAI_API_KEY env var
```

For local Hunyuan-MT on Apple Silicon:

```toml
[engines.mthy.options]
backend = "mlx"
mlx_path = "/path/to/Tencent-HunyuanMT-mlx"
max_tokens = 2048
```

## Python API

```python
from abersetz.pipeline import TranslatorOptions, translate_path
from pathlib import Path

results = translate_path(
    Path("./docs"),
    TranslatorOptions(engine="tr/google", to_lang="es"),
)
for r in results:
    print(f"{r.source} -> {r.destination} ({r.chunks} chunks)")
```

## How chunking works

Translation APIs reject large inputs. LLMs have context windows. Abersetz handles both:

- **HTML**: sent as one piece so tags stay intact.
- **Plain text / Markdown**: split by the `semantic-text-splitter` library at sentence and paragraph boundaries, respecting the `chunk_size` setting. Falls back to brute-force character slicing if the library is unavailable.

Vocabulary accumulated during earlier chunks is included in the prompt for later ones (for LLM engines), so terminology stays consistent across the whole document.

## License

MIT
