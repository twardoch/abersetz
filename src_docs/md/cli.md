---
title: CLI Reference
description: Full reference for abersetz command-line interface.
---

# CLI Reference

## Commands

### `abersetz tr` — translate a string

```
abersetz tr <to_lang> <text> [options]
```

Translates `text` and writes the result to stdout.

```bash
abersetz tr es "Hello world" --engine tr::google
abersetz tr pl "File not found" --engine dt::deepl
abersetz tr ja "Hello" --engine ll::openai:gpt-4o-mini
```

### `abersetz tf` — translate a file

```
abersetz tf <to_lang> <file> [options]
```

Translates a single file. Output goes to `<dir>/<lang>/<filename>` by default.

```bash
abersetz tf de README.md --engine tr::google
abersetz tf fr docs/guide.md --engine ll::openai:gpt-4o-mini --output /tmp/fr/
abersetz tf pl report.md --engine dt::deepl --dry-run
```

### `abersetz td` — translate a directory tree

```
abersetz td <to_lang> <dir> [options]
```

Recursively translates all supported files in `dir`.

```bash
abersetz td pl ./docs --engine tr::google
abersetz td de ./docs --engine ll::siliconflow:Qwen/Qwen2.5-7B-Instruct
abersetz td es ./docs --engine dt::deepl --output ./docs_es
abersetz td ja ./docs --dry-run
```

### `abersetz ls` — list engines and providers

```
abersetz ls [SELECTOR] [options]
```

Lists available engines, providers and discovered models.

```bash
abersetz ls                  # all engines + providers (fast)
abersetz ls ll::             # query LLM model lists (slow; uses cache)
abersetz ls tr --job         # emit job-JSON skeleton for all translator providers
abersetz ls --force          # bypass discovery cache
abersetz ls --include-paid   # include paid-API providers
```

### `abersetz validate` — ping all configured engines

```
abersetz validate
```

Sends a test phrase through every configured engine and reports pass/fail.

---

## Common options

| Option | Description |
|--------|-------------|
| `--engine TEXT` | Engine selector (e.g. `tr::google`, `ll::openai:gpt-4o-mini`, `ml/mthy::/path`) |
| `--from-lang TEXT` | Source language code (default: `auto`) |
| `--output PATH` | Override output path (`tf`/`td`) |
| `--chunk-size INT` | Max characters per text chunk for LLM engines |
| `--job JSON` | Job-JSON file or string: translate with multiple entries at once |
| `--dry-run` | Show what would be translated without making API calls |
| `--Overwrite` | Replace original files in-place instead of writing to a subdirectory |

---

## Engine selector syntax

```
engine[/subvariant]::provider
```

| Part | Meaning |
|------|---------|
| `engine` | Engine family code: `tr`, `dt`, `lm`, `ll`, `ml`, `gg` |
| `/subvariant` | Optional model family for local engines, e.g. `/mthy`, `/gemma` |
| `::provider` | Backend, model ID, or file path |

Examples:

```
tr::google                                    # translators, Google backend
dt::deepl                                     # deep-translator, DeepL
ll::openai:gpt-4o-mini                        # LLM, OpenAI endpoint, gpt-4o-mini
ll::siliconflow:Qwen/Qwen2.5-7B-Instruct     # LLM, SiliconFlow, Qwen model
ml/mthy::7b-mlx                               # MLX, Hy-MT2 family, 7B model alias
ml/mthy::/abs/path/to/model                   # MLX, Hy-MT2 family, explicit path
gg/mthy::tencent/Hy-MT2-7B-GGUF              # GGUF, Hy-MT2 family, HF repo ID
lm::gemma-3-4b                                # LMStudio with gemma-3-4b loaded
```

The legacy `engine/provider` form (`tr/google`, `ll/default`) is still accepted.

---

## Job JSON

A job file lets you fan one input across multiple engines simultaneously — handy for benchmarking:

```json
{
  "to_lang": "pl",
  "from_lang": "en",
  "entries": [
    {"selector": "tr::google"},
    {"selector": "dt::deepl"},
    {"selector": "ll::siliconflow:Qwen/Qwen2.5-7B-Instruct", "params": {"temperature": 0.3}}
  ]
}
```

Use it with:

```bash
abersetz td pl ./docs --job job.json
```

Or generate a skeleton:

```bash
abersetz ls tr --job > tr_job.json
```

---

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Translation error (engine failed, file not found, etc.) |
| 2 | Configuration error (missing API key, unknown engine) |
