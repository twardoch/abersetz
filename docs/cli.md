---
layout: default
title: CLI Reference
nav_order: 3
---

# CLI Reference
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Overview

Abersetz provides two command-line tools:

- `abersetz`: Main CLI with subcommands (`tr`, `validate`, `config`, `engines`, `version`)
- `abtr`: Direct translation shorthand

## Main Commands

### abersetz tr

Translate files or directories.

```bash
abersetz tr PATH [OPTIONS]
```

#### Arguments

- `PATH`: File or directory to translate (required)

#### Options

| Option | Description | Default |
|--------|-------------|---------|
| `to_lang` (positional) | Target language code | — |
| `--from-lang` | Source language code | `auto` |
| `--engine` | Translation engine | `tr/google` (legacy names auto-normalized) |
| `--output` | Output directory | `<lang>/<filename>` |
| `--recurse/--no-recurse` | Process subdirectories | `True` |
| `--write_over` | Replace original files | `False` |
| `--include` | File patterns to include | `*.txt,*.md,*.html` |
| `--xclude` | File patterns to xclude | None |
| `--chunk-size` | Characters per chunk | `1200` |
| `--html-chunk-size` | Characters per HTML chunk | `1800` |
| `--save-voc` | Save voc JSON | `False` |
| `--dry-run` | Preview without translating | `False` |
| `--verbose` | Enable debug output | `False` |

### abersetz config

Manage configuration settings.

```bash
abersetz config COMMAND
```

#### Subcommands

- `show`: Display current configuration
- `path`: Show configuration file location

### abersetz version

Display version information.

```bash
abersetz version
```

### abersetz engines

List available engine families and providers.

```bash
abersetz engines [--include-paid] [--family tr|dt|ll|hy] [--configured-only]
```

- `--family`: filter to a single engine family (short alias or legacy name).
- `--configured-only`: show only engines currently configured.

### abersetz validate

Exercise each configured engine with a short translation and report status, latency, and pricing hints.

```bash
abersetz validate [--selectors tr/google,ll/default] [--target-lang es] [--sample-text "Hello"]
```

- `--selectors`: comma-separated list of selectors to validate (defaults to every configured selector).
- `--target-lang`: target language for the sample translation (defaults to `es`).
- `--sample-text`: override the default sample prompt (`Hello, world!`).
- `--include-defaults/--no-include-defaults`: toggle whether the default engine from config is forced into the run.

{: .note }
Running validation hits live translation APIs. When you are offline—or when you only need a smoke test—use `--selectors` to limit the run to a handful of engines and add `--no-include-defaults` to skip automatically discovered selectors. For example:

```bash
abersetz validate \
  --selectors tr/google,ll/default \
  --no-include-defaults \
  --sample-text "Ping"
```

This checks only the Google free tier and your primary LLM profile, keeping the run under a few seconds and avoiding throttled providers.

## Shorthand Command

### abtr

Direct translation command equivalent to `abersetz tr`:

```bash
abtr TO_LANG PATH [OPTIONS]
```

All options from `abersetz tr` are available.

## Usage Examples

### Basic Translation

Translate a single file:

```bash
abersetz tr es document.txt
```

Translate to French using shorthand:

```bash
abtr fr document.txt
```

### Directory Translation

Translate all files in a directory:

```bash
abersetz tr de ./docs --output ./docs_de
```

With specific patterns:

```bash
abtr ja ./project \
  --include "*.md,*.txt" \
  --xclude "*test*,.*" \
  --output ./translations/ja
```

### Engine Selection

Use different translation engines:

```bash
# Google Translate (free)
abtr pt file.txt --engine translators/google

# Bing Translate (free)
abtr pt file.txt --engine translators/bing

# DeepL
abtr pt file.txt --engine deep-translator/deepl

# SiliconFlow LLM
abtr pt file.txt --engine hysf

# Custom LLM profile
abtr pt file.txt --engine ullm/gpt4
```

### Validate Engines

Generate a quick health report for every configured engine:

```bash
abersetz validate --target-lang de --selectors tr/google,ll/default
```

### Advanced Options

write_over original files:

```bash
abersetz tr es backup.txt --write_over
```

Save voc for LLM engines:

```bash
abtr de technical.md \
  --engine ullm/default \
  --save-voc
```

Dry run to preview:

```bash
abersetz tr fr large_project/ \
  --dry-run
```

Custom chunk sizes:

```bash
abtr zh-CN document.html \
  --html-chunk-size 3000
```

## Language Codes

Common language codes supported:

| Code | Language |
|------|----------|
| `en` | English |
| `es` | Spanish |
| `fr` | French |
| `de` | German |
| `it` | Italian |
| `pt` | Portuguese |
| `ru` | Russian |
| `ja` | Japanese |
| `ko` | Korean |
| `zh-CN` | Chinese (Simplified) |
| `zh-TW` | Chinese (Traditional) |
| `ar` | Arabic |
| `hi` | Hindi |
| `auto` | Auto-detect (source only) |

## Pattern Matching

Include/xclude patterns support wildcards:

- `*.txt` - All .txt files
- `doc*` - Files starting with "doc"
- `*test*` - Files containing "test"
- `.*` - Hidden files
- `*.{md,txt}` - Multiple extensions

## Environment Variables

Set default behaviors with environment variables:

```bash
# Default target language
export ABERSETZ_TO_LANG=es

# Default engine
export ABERSETZ_ENGINE=translators/bing

# API keys for LLM engines
export OPENAI_API_KEY=sk-...
export SILICONFLOW_API_KEY=sk-...
```

## Output Format

Translation results are printed as file paths:

```
/path/to/output/file1.txt
/path/to/output/file2.txt
```

Use `--verbose` for detailed progress:

```bash
abersetz tr fr docs/ --verbose
```

## Error Handling

Common errors and solutions:

### Missing API key

```
Error: Missing API key for engine
```

Solution: Export the required environment variable:

```bash
export SILICONFLOW_API_KEY="your-key"
```

### No files matched

```
Error: No files matched under /path
```

Solution: Check your include patterns:

```bash
abtr . --include "*.md,*.txt"
```

### Network error

```
Error: Network error - Connection timeout
```

Solution: The tool automatically retries. Check your internet connection.

## Tips and Tricks

### Batch translation

Create a script for multiple languages:

```bash
for lang in es fr de ja; do
  abersetz tr $lang docs/ --output docs_$lang
done
```

### Parallel processing

Use GNU parallel for speed:

```bash
find . -name "*.txt" | parallel -j4 abtr es {}
```

### Progress tracking

For large projects, use verbose mode:

```bash
abersetz tr fr large_project/ --verbose 2>&1 | tee translation.log
```

### Testing configuration

Always test with dry-run first:

```bash
abersetz tr de important_docs/ --dry-run
```

## See Also

- [Configuration Guide](configuration/)
- [Python API Reference](api/)
- [Translation Engines](engines/)
