---
layout: default
title: Configuration
nav_order: 5
---

# Configuration
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---

## Overview

Abersetz stores configuration in a JSON file managed by `platformdirs`, ensuring cross-platform compatibility.

## Configuration Location

Find your configuration file:

```bash
abersetz config path
```

Typical locations:
- **Linux**: `~/.config/abersetz/config.json`
- **macOS**: `~/Library/Application Support/abersetz/config.json`
- **Windows**: `%APPDATA%\abersetz\config.json`

## Configuration Structure

### Complete Example

```json
{
  "defaults": {
    "engine": "translators/google",
    "from_lang": "auto",
    "to_lang": "en",
    "chunk_size": 1200,
    "html_chunk_size": 1800
  },
  "credentials": {
    "openai": {"env": "OPENAI_API_KEY"},
    "anthropic": {"env": "ANTHROPIC_API_KEY"},
    "siliconflow": {"env": "SILICONFLOW_API_KEY"},
    "deepseek": {"env": "DEEPSEEK_API_KEY"}
  },
  "engines": {
    "hysf": {
      "chunk_size": 2400,
      "credential": {"name": "siliconflow"},
      "options": {
        "model": "tencent/Hunyuan-MT-7B",
        "base_url": "https://api.siliconflow.com/v1",
        "temperature": 0.3
      }
    },
    "ullm": {
      "chunk_size": 2400,
      "options": {
        "profiles": {
          "default": {
            "base_url": "https://api.siliconflow.com/v1",
            "model": "tencent/Hunyuan-MT-7B",
            "credential": {"name": "siliconflow"},
            "temperature": 0.3,
            "max_input_tokens": 32000
          }
        }
      }
    }
  }
}
```

## Configuration Sections

### defaults

Global default settings for all translations:

```json
{
  "defaults": {
    "engine": "translators/google",  // Default translation engine
    "from_lang": "auto",             // Source language (auto-detect)
    "to_lang": "en",                 // Target language
    "chunk_size": 1200,              // Characters per text chunk
    "html_chunk_size": 1800          // Characters per HTML chunk
  }
}
```

### credentials

API key storage with environment variable references:

```json
{
  "credentials": {
    "openai": {
      "env": "OPENAI_API_KEY"        // Read from environment
    },
    "custom": {
      "value": "sk-actual-key-here"  // Direct value (not recommended)
    }
  }
}
```

### engines

Custom engine configurations:

```json
{
  "engines": {
    "engine_name": {
      "chunk_size": 2000,
      "credential": {"name": "credential_name"},
      "options": {
        // Engine-specific options
      }
    }
  }
}
```

## Setting Up Credentials

### Environment Variables (Recommended)

Store API keys as environment variables:

```bash
# Add to ~/.bashrc or ~/.zshrc
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export SILICONFLOW_API_KEY="sk-..."
```

Then reference in config:

```json
{
  "credentials": {
    "openai": {"env": "OPENAI_API_KEY"}
  }
}
```

### Direct Values (Not Recommended)

Store directly in config (less secure):

```json
{
  "credentials": {
    "openai": {"value": "sk-actual-key-here"}
  }
}
```

## Engine Configuration

### LLM Engine (ullm)

Configure multiple LLM profiles:

```json
{
  "engines": {
    "ullm": {
      "chunk_size": 2400,
      "options": {
        "profiles": {
          "gpt4": {
            "base_url": "https://api.openai.com/v1",
            "model": "gpt-4-turbo-preview",
            "credential": {"name": "openai"},
            "temperature": 0.3,
            "max_input_tokens": 128000,
            "prolog": {
              "role": "You are an expert translator"
            }
          },
          "claude": {
            "base_url": "https://api.anthropic.com/v1",
            "model": "claude-3-opus-20240229",
            "credential": {"name": "anthropic"},
            "temperature": 0.3,
            "max_input_tokens": 200000
          }
        }
      }
    }
  }
}
```

Usage:
```bash
abtr file.txt --engine ullm/gpt4 --to-lang es
abtr file.txt --engine ullm/claude --to-lang fr
```

### Custom Endpoints

Configure self-hosted models:

```json
{
  "engines": {
    "local_llm": {
      "chunk_size": 1500,
      "options": {
        "base_url": "http://localhost:8080/v1",
        "model": "local-model",
        "temperature": 0.5
      }
    }
  }
}
```

## Managing Configuration

### View Current Config

```bash
abersetz config show
```

Or pretty-print:

```bash
abersetz config show | jq '.'
```

### Edit Configuration

Edit directly:

```bash
# Find location
CONFIG_PATH=$(abersetz config path | tail -1)

# Edit with your preferred editor
nano "$CONFIG_PATH"
# or
vim "$CONFIG_PATH"
```

### Reset Configuration

Remove to reset to defaults:

```bash
rm "$(abersetz config path | tail -1)"
```

### Backup Configuration

```bash
CONFIG_PATH=$(abersetz config path | tail -1)
cp "$CONFIG_PATH" "$CONFIG_PATH.backup"
```

## Python Configuration API

### Load Configuration

```python
from abersetz.config import load_config

config = load_config()
print(config.defaults.engine)
print(config.defaults.to_lang)
```

### Modify Configuration

```python
from abersetz.config import load_config, save_config

config = load_config()

# Change defaults
config.defaults.to_lang = "es"
config.defaults.chunk_size = 1500

# Add credential
from abersetz.config import Credential
config.credentials["myapi"] = Credential(env="MY_API_KEY")

# Save changes
save_config(config)
```

### Add Custom Engine

```python
from abersetz.config import load_config, save_config, EngineConfig, Credential

config = load_config()

config.engines["custom"] = EngineConfig(
    name="custom",
    chunk_size=2000,
    credential=Credential(env="CUSTOM_API_KEY"),
    options={
        "base_url": "https://api.custom.com/v1",
        "model": "translation-v1",
        "temperature": 0.3
    }
)

save_config(config)
```

## Environment Variables

### Abersetz-specific

Override defaults with environment variables:

```bash
export ABERSETZ_ENGINE="translators/bing"
export ABERSETZ_TO_LANG="es"
export ABERSETZ_CHUNK_SIZE="1500"
```

### API Keys

Standard API key variables:

```bash
# OpenAI
export OPENAI_API_KEY="sk-..."

# Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."

# Google
export GOOGLE_API_KEY="..."

# SiliconFlow
export SILICONFLOW_API_KEY="sk-..."

# DeepSeek
export DEEPSEEK_API_KEY="..."

# Mistral
export MISTRAL_API_KEY="..."

# Together AI
export TOGETHERAI_API_KEY="..."
```

## Configuration Templates

### Minimal Config

```json
{
  "defaults": {
    "engine": "translators/google",
    "to_lang": "es"
  }
}
```

### Multi-engine Config

```json
{
  "defaults": {
    "engine": "translators/google"
  },
  "credentials": {
    "openai": {"env": "OPENAI_API_KEY"},
    "anthropic": {"env": "ANTHROPIC_API_KEY"}
  },
  "engines": {
    "gpt": {
      "chunk_size": 3000,
      "credential": {"name": "openai"},
      "options": {
        "model": "gpt-4-turbo-preview",
        "base_url": "https://api.openai.com/v1"
      }
    },
    "claude": {
      "chunk_size": 3000,
      "credential": {"name": "anthropic"},
      "options": {
        "model": "claude-3-opus-20240229",
        "base_url": "https://api.anthropic.com/v1"
      }
    }
  }
}
```

### Enterprise Config

```json
{
  "defaults": {
    "engine": "corporate_llm",
    "to_lang": "en",
    "chunk_size": 2000
  },
  "credentials": {
    "corporate": {
      "env": "CORP_TRANSLATION_KEY"
    }
  },
  "engines": {
    "corporate_llm": {
      "chunk_size": 2500,
      "credential": {"name": "corporate"},
      "options": {
        "base_url": "https://translation.company.com/v1",
        "model": "corp-translator-v2",
        "temperature": 0.2,
        "max_retries": 5,
        "timeout": 30
      }
    }
  }
}
```

## Security Best Practices

1. **Never commit API keys**: Add `config.json` to `.gitignore`

2. **Use environment variables**: Store keys in environment, not config

3. **Rotate keys regularly**: Update API keys periodically

4. **Restrict file permissions**:
   ```bash
   chmod 600 "$(abersetz config path | tail -1)"
   ```

5. **Use separate keys**: Different keys for dev/prod environments

## Troubleshooting

### Config not loading

Check file exists and is valid JSON:

```bash
CONFIG_PATH=$(abersetz config path | tail -1)
cat "$CONFIG_PATH" | jq '.'
```

### API key not found

Verify environment variable is set:

```bash
echo $OPENAI_API_KEY
```

### Permission denied

Fix file permissions:

```bash
chmod 644 "$(abersetz config path | tail -1)"
```

## See Also

- [Translation Engines](engines/)
- [Python API](api/)
- [Examples](examples/)