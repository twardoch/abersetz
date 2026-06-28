---
title: Configuration
description: Configure abersetz via TOML file, environment variables, and engine options.
---

# Configuration

Abersetz reads a TOML config file. A per-project `abersetz.toml` in the working directory takes precedence over the user-level config.

## File location

```bash
# Show where the user-level config lives
abersetz config path
```

Defaults:

| Platform | Path |
|----------|------|
| Linux | `~/.config/abersetz/config.toml` |
| macOS | `~/Library/Application Support/abersetz/config.toml` |
| Windows | `%APPDATA%\abersetz\config.toml` |

## Minimal example

```toml
[defaults]
engine = "tr::google"
to_lang = "pl"
```

## Full example

```toml
[defaults]
engine = "tr::google"
from_lang = "auto"
to_lang = "en"
chunk_size = 1200
html_chunk_size = 1800

# --- Credentials (prefer env vars; inline only for dev) ---
[credentials.openai]
env = "OPENAI_API_KEY"

[credentials.anthropic]
env = "ANTHROPIC_API_KEY"

[credentials.siliconflow]
env = "SILICONFLOW_API_KEY"

[credentials.deepl]
env = "DEEPL_API_KEY"

# --- LMStudio ---
[engines.lmstudio]
chunk_size = 2400

[engines.lmstudio.options]
base_url = "localhost:1234"
model = "gemma-3-4b"

# --- OpenAI-compatible LLM with profile ---
[engines.ullm]
chunk_size = 2000

[engines.ullm.options.profiles.openai]
base_url = ""               # empty = official OpenAI endpoint
model = "gpt-4o-mini"
temperature = 0.3

[engines.ullm.options.profiles.siliconflow]
base_url = "https://api.siliconflow.com/v1"
model = "Qwen/Qwen2.5-7B-Instruct"
temperature = 0.3

# --- Local Hy-MT2 via MLX ---
[engines.mthy.options]
backend = "mlx"
mlx_path = "/path/to/Hy-MT2-7B-mlx"
max_tokens = 2048

# --- Local Hy-MT2 via GGUF ---
[engines.mthy.options]
backend = "gguf"
gguf_path = "/path/to/Hy-MT2-7B-Q8_0.gguf"
max_tokens = 2048
n_gpu_layers = -1           # -1 = all layers on GPU
n_ctx = 4096
```

## Configuration sections

### `[defaults]`

| Key | Type | Description |
|-----|------|-------------|
| `engine` | string | Default engine selector |
| `from_lang` | string | Source language (default: `"auto"`) |
| `to_lang` | string | Target language code |
| `chunk_size` | int | Characters per plain-text chunk |
| `html_chunk_size` | int | Characters per HTML chunk |

### `[credentials.<name>]`

```toml
[credentials.openai]
env = "OPENAI_API_KEY"       # read from this env var
# value = "sk-..."           # inline (not recommended)
```

### `[engines.<name>]`

| Key | Type | Description |
|-----|------|-------------|
| `chunk_size` | int | Override global chunk_size for this engine |
| `html_chunk_size` | int | Override for HTML |
| `credential` | string | Credential name (matches `[credentials.<name>]`) |
| `options` | table | Engine-specific options (see below) |

### `[engines.ullm.options.profiles.<name>]`

Named profiles let you switch between LLM providers at runtime:

```bash
abersetz td pl ./docs --engine ll/openai     # uses profile "openai"
abersetz td pl ./docs --engine ll/siliconflow
```

Profile keys:

| Key | Description |
|-----|-------------|
| `base_url` | API base URL (empty string = official OpenAI) |
| `model` | Model ID |
| `temperature` | Sampling temperature (0.0–1.0) |
| `prolog` | Static key→value map injected into every LLM prompt |

## Environment variables

All credentials can be passed as environment variables without a config file:

```bash
OPENAI_API_KEY=sk-...      abersetz td pl ./docs --engine ll::openai:gpt-4o-mini
DEEPL_API_KEY=...          abersetz td de ./docs --engine dt::deepl
SILICONFLOW_API_KEY=sk-... abersetz td fr ./docs --engine ll::siliconflow:Qwen/Qwen2.5-7B-Instruct
```

## Per-project config

Drop `abersetz.toml` in your project root; abersetz will prefer it over the user config:

```bash
echo '[defaults]
engine = "dt::deepl"
to_lang = "de"' > abersetz.toml

abersetz td de ./docs   # picks up local abersetz.toml automatically
```
