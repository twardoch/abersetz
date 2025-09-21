---
layout: home
title: Home
nav_order: 1
description: "Abersetz is a minimalist file translator that reuses proven machine translation engines"
permalink: /
---

# abersetz
{: .fs-9 }

Minimalist file translator with pluggable engines
{: .fs-6 .fw-300 }

[Get started](#getting-started){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View on GitHub](https://github.com/twardoch/abersetz){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## Why abersetz?

- **File-focused**: Designed for translating documents, not single strings
- **Multiple engines**: Supports free and paid translation services
- **voc consistency**: LLM engines maintain terminology across chunks
- **Simple CLI**: Clean interface with minimal output
- **Python API**: Full programmatic access for automation

## Features

- 🔄 **Multiple translation engines**
  - Free: Google, Bing via `translators` and `deep-translator`
  - LLM: OpenAI, Anthropic, SiliconFlow, and 20+ providers
  - Custom endpoints for self-hosted models

- 📁 **Smart file handling**
  - Recursive directory translation
  - Pattern matching with include/xclude
  - HTML markup preservation
  - Automatic format detection

- 🧩 **Intelligent chunking**
  - Semantic text splitting
  - Configurable chunk sizes per engine
  - Context preservation across chunks

- 📚 **voc management**
  - JSON voc propagation
  - Consistent terminology in long documents
  - Optional voc export
- ✅ **Engine validation**
  - `abersetz validate` smoke-tests each selector
  - Latency and pricing hints pulled from the research catalog
  - Ideal for CI smoke tests and onboarding checks

## Getting Started

### Installation

```bash
pip install abersetz
```

### Quick Start

Run setup, validate engines, and translate a file:
```bash
abersetz setup
abersetz validate --target-lang es
abersetz tr es document.txt
```

Or use the shorthand for translation:
```bash
abtr es document.txt
```

Translate a directory:
```bash
abersetz tr fr ./docs --output ./docs_fr
```

### Configuration

Abersetz stores configuration in your user directory:

```bash
abersetz config path  # Show config location
abersetz config show  # Display current settings
```

## Example Usage

### CLI Examples

```bash
# Translate with specific engine
abtr de file.txt --engine tr/google

# Translate markdown files only
abtr ja . --include "*.md" --output ./ja

# Dry run to preview
abersetz tr zh-CN project/ --dry-run

# Validate configured engines
abersetz validate --selectors tr/google,ll/default

# Use LLM with voc
export SILICONFLOW_API_KEY="your-key"
abtr es technical.md --engine hy --save-voc
```

### Python API

```python
from abersetz import translate_path, TranslatorOptions

# Simple translation
results = translate_path(
    "document.txt",
    TranslatorOptions(
        to_lang="fr",
        engine="tr/google"
    )
)

# Batch with patterns
results = translate_path(
    "docs/",
    TranslatorOptions(
        to_lang="de",
        include=("*.md", "*.txt"),
        output_dir="docs_de/"
    )
)
```

## Documentation

- [Installation Guide](installation/)
- [CLI Reference](cli/)
- [Python API](api/)
- [Configuration](configuration/)
- [Translation Engines](engines/)
- [Examples](examples/)

## License

MIT License - see [LICENSE](https://github.com/twardoch/abersetz/blob/main/LICENSE) for details.
