---
title: abersetz
description: Translate entire directory trees using multiple AI and classic translation engines.
---

# abersetz

Translate entire directories of text and Markdown files using modern AI. Feed it a folder; get back a translated folder. No boilerplate, no broken formatting.

## What it does

Abersetz takes a file or directory tree, detects the text format (plain text or HTML), slices large documents into chunks at natural sentence and paragraph boundaries, feeds each chunk to a translation engine, and stitches the results back together preserving the original layout.

Translation memory carries vocabulary terms forward across chunks so "widget" in paragraph 1 still means "widget" in paragraph 47.

## Quick start

```bash
pip install abersetz
```

```bash
# Translate a string to stdout
abersetz tr es "Hello world" --engine tr::google

# Translate a file to Spanish
abersetz tf es file.md --engine tr::google

# Translate a directory tree to Polish using an OpenAI LLM
abersetz td pl ./docs --engine ll::openai:gpt-4o-mini

# Dry run — verify paths without burning API credits
abersetz td de ./docs --dry-run
```

## Engine overview

| Code | Backend | Cost | Offline? |
|------|---------|------|---------|
| `tr` | `translators` package — web scraping | Free (rate-limited) | No |
| `dt` | `deep-translator` — official APIs | Free/paid depends on provider | No |
| `lm` | LMStudio — local model via official SDK | Free (local GPU) | Yes |
| `ll` | Any OpenAI-compatible endpoint | Paid (API key) | No |
| `ml` | Local MLX model (Apple Silicon) | Free (local GPU) | Yes |
| `gg` | Local GGUF model via llama.cpp | Free (local CPU/GPU) | Yes |

See [Choosing an Engine](engines.md) for a detailed comparison.

## Links

- [Installation](installation.md)
- [CLI Reference](cli.md)
- [Configuration](configuration.md)
- [Python API](api.md)
- [GitHub](https://github.com/twardoch/abersetz)
- [PyPI](https://pypi.org/project/abersetz/)
