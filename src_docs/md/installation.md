---
title: Installation
description: How to install abersetz and optional extras.
---

# Installation

## Requirements

- Python 3.12 or higher
- `pip` or `uv`

## Standard install

```bash
pip install abersetz
# or
uv pip install abersetz
```

## Optional extras

Install extras for local model backends:

```bash
# Apple Silicon MLX inference (macOS only)
pip install "abersetz[mlx]"

# GGUF inference via llama.cpp
pip install "abersetz[gguf]"

# LMStudio SDK
pip install "abersetz[lms]"

# All extras
pip install "abersetz[all]"
```

## Development install

```bash
git clone https://github.com/twardoch/abersetz.git
cd abersetz
uv pip install -e ".[dev]"
```

## Verify

```bash
abersetz --help
abersetz ls          # list available engines
```

## API keys

Set environment variables for cloud engines:

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export SILICONFLOW_API_KEY="sk-..."
export DEEPL_API_KEY="..."
export GOOGLE_API_KEY="..."     # Gemini
```

Add to `~/.bashrc` or `~/.zshrc` to persist.

## Docker

```dockerfile
FROM python:3.12-slim
RUN pip install abersetz
WORKDIR /data
ENTRYPOINT ["abersetz"]
```

```bash
docker build -t abersetz .
docker run -v $(pwd):/data abersetz td es /data/docs
```
