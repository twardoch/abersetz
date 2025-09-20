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

- `abersetz`: Main CLI with subcommands
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
| `--to-lang` | Target language code | `en` |
| `--from-lang` | Source language code | `auto` |
| `--engine` | Translation engine | `translators/google` |
| `--output` | Output directory | `<lang>/<filename>` |
| `--recurse/--no-recurse` | Process subdirectories | `True` |
| `--overwrite` | Replace original files | `False` |
| `--include` | File patterns to include | `*.txt,*.md,*.html` |
| `--exclude` | File patterns to exclude | None |
| `--chunk-size` | Characters per chunk | `1200` |
| `--html-chunk-size` | Characters per HTML chunk | `1800` |
| `--save-voc` | Save vocabulary JSON | `False` |
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

## Shorthand Command

### abtr

Direct translation command equivalent to `abersetz tr`:

```bash
abtr PATH [OPTIONS]
```

All options from `abersetz tr` are available.

## Usage Examples

### Basic Translation

Translate a single file:

```bash
abersetz tr document.txt --to-lang es
```

Translate to French using shorthand:

```bash
abtr document.txt --to-lang fr
```

### Directory Translation

Translate all files in a directory:

```bash
abersetz tr ./docs --to-lang de --output ./docs_de
```

With specific patterns:

```bash
abtr ./project \
  --include "*.md,*.txt" \
  --exclude "*test*,.*" \
  --to-lang ja
```

### Engine Selection

Use different translation engines:

```bash
# Google Translate (free)
abtr file.txt --to-lang pt --engine translators/google

# Bing Translate (free)
abtr file.txt --to-lang pt --engine translators/bing

# DeepL
abtr file.txt --to-lang pt --engine deep-translator/deepl

# SiliconFlow LLM
abtr file.txt --to-lang pt --engine hysf

# Custom LLM profile
abtr file.txt --to-lang pt --engine ullm/gpt4
```

### Advanced Options

Overwrite original files:

```bash
abersetz tr backup.txt --to-lang es --overwrite
```

Save vocabulary for LLM engines:

```bash
abtr technical.md \
  --to-lang de \
  --engine ullm/default \
  --save-voc
```

Dry run to preview:

```bash
abersetz tr large_project/ \
  --to-lang fr \
  --dry-run
```

Custom chunk sizes:

```bash
abtr document.html \
  --to-lang zh-CN \
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

Include/exclude patterns support wildcards:

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
abersetz tr docs/ --to-lang fr --verbose
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
  abersetz tr docs/ --to-lang $lang --output docs_$lang
done
```

### Parallel processing

Use GNU parallel for speed:

```bash
find . -name "*.txt" | parallel -j4 abtr {} --to-lang es
```

### Progress tracking

For large projects, use verbose mode:

```bash
abersetz tr large_project/ --to-lang fr --verbose 2>&1 | tee translation.log
```

### Testing configuration

Always test with dry-run first:

```bash
abersetz tr important_docs/ --to-lang de --dry-run
```

## See Also

- [Configuration Guide](configuration/)
- [Python API Reference](api/)
- [Translation Engines](engines/)