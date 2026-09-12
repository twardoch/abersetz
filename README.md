# abersetz

Translate entire directories of text and Markdown files using modern AI. Feed it a folder; get back a translated folder. No boilerplate, no broken formatting.

## What it does

Abersetz takes a file or directory tree, detects the text format (plain text or HTML), slices large documents into chunks at natural sentence and paragraph boundaries, feeds each chunk to a translation engine, and stitches the results back together preserving the original layout.

Translation memory carries vocabulary terms forward across chunks so "widget" in paragraph 1 still means "widget" in paragraph 47.

## Engines

Abersetz speaks to several translation backends through a unified selector
grammar: `engine[/subvariant]::provider`.

| Engine code | What it uses | Example selector |
|---|---|---|
| `tr` | `translators` package — scrapes web endpoints | `tr::google`, `tr::bing` |
| `dt` | `deep-translator` — more stable, official APIs | `dt::deepl`, `dt::microsoft` |
| `lm` | LMStudio local models via the official `lmstudio` SDK | `lm::gemma-3-4b` |
| `ll` | Any OpenAI-compatible LLM endpoint | `ll::siliconflow:Qwen/Qwen2.5-7B-Instruct` |
| `ml` | Local MLX model (`mlx_lm`) | `ml/hy-mt2::/models/Hy-MT2-7B` |
| `gg` | Local GGUF model (`llama.cpp`) | `gg/gemma::/models/gemma.gguf` |

The text after `::` is the provider: a translation backend (`tr`/`dt`), a model
id (`lm`), an `endpoint:model` spec (`ll`), or a model folder/file path
(`ml`/`gg`). An optional subvariant before `::` (e.g. `ml/hy-mt2`, `lm/gemma`)
picks the prompt family for local models. The legacy `engine/provider` form
(`tr/google`, `ll/default`) is still accepted.

LLM engines wrap text in XML tags and extract the `<output>` block from the response, which makes them tolerant of chatty models that add extra commentary. Dedicated translation models are the exception: abersetz recognises them by name and sends each one its native prompt instead (see below).

### Dedicated translation models

| Model | Prompt family | Where it runs | Example selectors |
|---|---|---|---|
| Tencent **Hy-MT2** (1.8B / 7B / 30B-A3B) | `hy-mt2` | `ml`, `gg`, `lm`, `ll` | `gg::7b-gguf`, `ml::7b-mlx`, `lm::hy-mt2-7b`, `ll::openrouter:tencent/hy-mt2-7b`, `ll::tencent:hy-mt2-pro` |
| Google **TranslateGemma** (4B / 12B / 27B) | `gemma` | `ml`, `gg`, `lm`, `ll` | `ml::tg-4b-mlx`, `gg::tg-12b-gguf`, `lm::translategemma-4b-it` |
| BSC-LT **SalamandraTA-7b-instruct** | `salamandra` | `gg` (alias); `ml`/`lm`/`ll` with an explicit repo or model id | `gg::salamandra-7b` |
| Google **MADLAD-400-10B-MT** (T5) | `madlad` | `gg` only | `gg::madlad-10b` |

The family is inferred from the model id, path or file name; force it with a
subvariant (`ll/hy-mt2::openai:my-finetune`). What each family changes:

- **Hy-MT2** uses Tencent's official English instruction (with a terminology
  block when a vocabulary is present), no system prompt, and the recommended
  sampler (`temperature 0.7, top_p 0.6, top_k 20, repetition_penalty 1.05`;
  the 30B-A3B mixture-of-experts variant uses `top_p 1.0` and no `top_k`).
  Hosted tiers: OpenRouter (`tencent/hy-mt2-1.8b`, `-7b`, `-30b-a3b`) and
  Tencent Cloud TokenHub (`hy-mt2-pro`, `-plus`, `-lite`; set
  `TENCENTCLOUD_API_KEY`).
- **TranslateGemma** needs its unusual chat template: the user turn carries
  `source_lang_code` and `target_lang_code`. Runtimes that apply the model's
  own template get that structure; LM Studio and OpenAI-compatible servers get
  the rendered text verbatim. Decoding is greedy. Pass `--from-lang`; without
  it English is assumed.
- **SalamandraTA** gets the model-card prompts (plain, glossary-constrained
  when a vocabulary is present, markup-preserving for HTML) with English
  language names and greedy decoding.
- **MADLAD-400** is prompted with `<2de> text`. llama-cpp-python's chat API
  cannot drive T5 models, so abersetz runs the encode/decode loop itself; the
  encoder window is 512 tokens, so chunks default to 300 characters.

`abersetz ls gg::` and `abersetz ls ml::` list the curated aliases
(`7b-gguf`, `30b-mlx`, `tg-27b-4bit-mlx`, `madlad-10b`, …). Any Hugging Face
repo id also works, with `repo:QUANT` to pick a GGUF quantisation:
`gg::tencent/Hy-MT2-7B-GGUF:Q4_K_M`.

## Install

```bash
pip install abersetz
# or
uv pip install abersetz
```

## Quick start

```bash
# Translate a string straight to stdout
abersetz tr es "Hello world" --engine tr::google

# Translate a single file to Spanish using Google (via translators)
abersetz tf es file.md --engine tr::google

# Translate a directory tree to Polish using an OpenAI-compatible LLM
abersetz td pl ./docs --engine ll::openai:gpt-4o-mini

# Dry run — verify paths and settings without burning API credits
abersetz td de ./docs --dry-run

# List engines, providers and models (or a subset)
abersetz ls            # engines + provider names (fast)
abersetz ls ll::       # query LLM model lists (slow; cached)
abersetz ls tr --job   # emit a job-JSON skeleton for all translators providers
```

Output files land in a subdirectory named after the target language by default (e.g. `./docs/pl/`). Use `--output` to redirect them, or `--Overwrite` to replace files in place.

## CLI reference

```
abersetz tr <to_lang> <text>   Translate a string to stdout
abersetz tf <to_lang> <file>   Translate a single file
abersetz td <to_lang> <dir>    Translate a directory tree

  --engine TEXT      Engine selector, e.g. tr::google, ll::openai:gpt-4o, ml/hy-mt2::/models/x
  --from-lang TEXT   Source language code (default: auto-detect)
  --output PATH      Where to write translated files (tf/td)
  --chunk-size INT   Max tokens per chunk for LLM engines
  --job JSON         A job-JSON file/string: translate with every entry at once
  --dry-run          Show what would be translated without calling any API (tf/td)

abersetz ls [SELECTOR]   List engines / providers / models (combines old engines+discover)
  --job              Emit an abersetz job-JSON skeleton instead of a table
  --force            Bypass the discovery cache for slow model lookups
  --include-paid     Include providers needing a paid API key

abersetz validate    Ping all configured engines with a test phrase
```

### Job JSON

A job pairs selectors with languages, chunk sizes, engine params and an output
suffix, so one input can be fanned across many engines (used by the benchmark):

```json
{
  "to_lang": "pl",
  "from_lang": "en",
  "entries": [
    {"selector": "tr::google"},
    {"selector": "ll::siliconflow:Qwen/Qwen2.5-7B-Instruct", "params": {"temperature": 0.3}}
  ]
}
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

## Uubed translation memory

Use `--tm=/path/to/localization.sqlite` with `tr`, `tf`, or `td` for English-source
localization. A unique verbatim match is returned without loading the translation
or embedding model. On a miss/conflict, `ll`, `lm`, and Hy-MT MLX/GGUF engines receive
near bilingual examples in their prompt. Examples remain request-local and are
included in the translation cache key.

Install the `tm` extra plus the Uubed inference backend needed by your index.
For local development, see `../uubed-project/README.md`; the corresponding package
changes have not been published. Build the database using `uubed tm build`.

```bash
abersetz tr pl 'Make the font bold' --from-lang=en --tm=localization.sqlite \
  --tm-model-path=/path/to/embedding-model.gguf --engine='gg/mthy::1.8b-gguf'
```

`--tm-top-k=5`, `--tm-minimum=0.5`, and `--tm-context-chars=4000` bound the example
count, cosine threshold and serialized JSON character budget. Complete pairs are
retained; context is not truncated inside a source/target string. Token usage
still depends on the translation model's tokenizer. Regional language codes must
match the index exactly. `--tm-exact-only` uses verbatim reuse with any engine and
disables semantic context. TranslateGemma and conventional translator adapters
currently require this mode. File `--job` cannot be combined with `--tm` yet.

## Releases and local data

`./publish.sh --dry-run` verifies the next release without pushing or uploading.
`./publish.sh` commits, tags and publishes it. See [RELEASING.md](RELEASING.md)
for credentials, same-tag retries, dependency order and private-data exclusions.
