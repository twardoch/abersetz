---
title: Choosing an Engine
description: Compare abersetz translation engines by cost, quality, speed, and use case.
---

# Choosing an Engine

Abersetz supports six engine families. Each addresses a different point on the cost/quality/privacy triangle.

## Comparison table

| Engine | Code | Cost | Quality | Speed | Privacy | Offline | Requires |
|--------|------|------|---------|-------|---------|---------|---------|
| `translators` (Google) | `tr::google` | Free, rate-limited | Good | Fast | Data sent to Google | No | Nothing |
| `translators` (Bing) | `tr::bing` | Free, rate-limited | Good | Fast | Data sent to Microsoft | No | Nothing |
| `deep-translator` (Google) | `dt::google` | Free, rate-limited | Good | Fast | Data sent to Google | No | Nothing |
| `deep-translator` (DeepL) | `dt::deepl` | Free tier / paid | Excellent | Fast | Data sent to DeepL | No | `DEEPL_API_KEY` |
| `deep-translator` (Microsoft) | `dt::microsoft` | Paid | Very good | Fast | Data sent to Microsoft | No | `MICROSOFT_TRANSLATOR_KEY` |
| `deep-translator` (LibreTranslate) | `dt::libre` | Free (self-host) | Moderate | Moderate | Self-hosted option | Partial | LibreTranslate URL |
| LMStudio | `lm::model-id` | Free (local GPU) | Excellent | Moderate | 100% local | Yes | LMStudio app + model |
| LLM (OpenAI) | `ll::openai:gpt-4o-mini` | Paid (~$0.15/1M tokens in) | Excellent | Fast | Data sent to OpenAI | No | `OPENAI_API_KEY` |
| LLM (SiliconFlow) | `ll::siliconflow:Qwen/Qwen2.5-7B-Instruct` | Very cheap (~$0.05/1M tokens in) | Very good | Fast | Data sent to SiliconFlow | No | `SILICONFLOW_API_KEY` |
| LLM (Anthropic) | `ll::anthropic:claude-haiku-4-5` | Paid (~$0.80/1M tokens in) | Excellent | Fast | Data sent to Anthropic | No | `ANTHROPIC_API_KEY` |
| LLM (Gemini) | `ll::gemini:gemini-2.0-flash` | Free tier / paid | Very good | Fast | Data sent to Google | No | `GEMINI_API_KEY` |
| MLX (Apple Silicon) | `ml/mthy::path` | Free (local GPU) | Good–Very good | Fast on M-series | 100% local | Yes | Apple Silicon Mac + `mlx_lm` |
| GGUF (llama.cpp) | `gg/mthy::path` | Free (local CPU/GPU) | Good–Very good | Moderate | 100% local | Yes | `llama-cpp-python` + GGUF file |

## Rate limits and costs

### `tr` — `translators` package (web scraping)

- **Cost**: Free.
- **Rate limits**: Unofficial; Google/Bing impose undocumented per-IP request caps.  
  Expect throttling after ~100 requests/minute. Abersetz retries 3× with exponential backoff.
- **Chunk size**: Default 1 200 characters. Larger chunks increase throttle risk.
- **Best for**: Casual use, prototyping, non-sensitive content.

### `dt` — `deep-translator` (official APIs)

- **Google**: Free unofficial API, same throttle risk as `tr::google`.
- **DeepL**: Free tier caps at 500 000 characters/month; Pro tier is ~$25/month for 1M chars.
  Rate limit: 5 requests/second. API key env var: `DEEPL_API_KEY`.
- **Microsoft**: Pay-as-you-go, ~$10/1M characters.
  Rate limit: 1 000 requests/min, 100 per 10 seconds. API key env var: `MICROSOFT_TRANSLATOR_KEY`.
- **LibreTranslate**: Self-hosted, effectively unlimited. Public instances are rate-limited per IP.
- **Best for**: High-volume production work where DeepL/Microsoft quality is required.

### `lm` — LMStudio (local model via SDK)

- **Cost**: Free; you pay only for hardware and electricity.
- **Rate limits**: None (your local GPU is the only bottleneck).
- **Latency**: 10–200 ms/token depending on model size and hardware.
- **Best for**: Privacy-sensitive content, offline environments, consistent API without cloud billing.

### `ll` — OpenAI-compatible LLM endpoint

- **Cost**: Depends on provider and model. Examples:
  - OpenAI `gpt-4o-mini`: ~$0.15/1M input tokens, ~$0.60/1M output tokens.
  - SiliconFlow `Qwen2.5-7B-Instruct`: ~$0.05/1M tokens total.
  - Anthropic `claude-haiku-4-5`: ~$0.80/1M input tokens, ~$4/1M output tokens.
  - Gemini `gemini-2.0-flash`: free tier generous; then ~$0.10/1M tokens.
- **Rate limits**: Provider-specific. Abersetz retries 3× with exponential backoff.
  OpenAI default: 3 000 RPM (requests per minute) on Tier 1.
- **Best for**: High translation quality, multilingual nuance, terminology consistency across large docs.

### `ml` — MLX (Apple Silicon local inference)

- **Cost**: Free; requires Apple Silicon Mac (M1 or later) and `pip install abersetz[mlx]`.
- **Rate limits**: None.
- **Models**: Hy-MT2 (Tencent, optimised for CJK↔EU), Gemma translation variants.
- **Best for**: macOS users who want fully offline, high-quality translation at near-API speed.

### `gg` — GGUF (llama.cpp local inference)

- **Cost**: Free; requires `pip install abersetz[gguf]` and a `.gguf` model file.
- **Rate limits**: None.
- **Performance**: CPU inference ~2–10 tokens/s; GPU offload with `--n-gpu-layers` much faster.
- **Best for**: Linux/Windows offline use, or macOS without the MLX stack.

## Decision guide

```
Need it free and fast? → tr::google or dt::google (watch rate limits)
Need DeepL quality at scale? → dt::deepl (500k chars/month free)
Privacy matters / offline? → lm (LMStudio) or ml (MLX on macOS) or gg (GGUF anywhere)
Best quality, don't mind paying? → ll::openai:gpt-4o or ll::anthropic:claude-haiku-4-5
Cheap cloud LLM quality? → ll::siliconflow:Qwen/Qwen2.5-7B-Instruct
CJK translation on Apple Silicon? → ml/mthy::<path-to-Hy-MT2-model>
```

## Example commands

```bash
# Free, fast — scrapes Google Translate
abersetz td pl ./docs --engine tr::google

# DeepL quality (requires DEEPL_API_KEY)
abersetz td de ./docs --engine dt::deepl

# Cheap LLM cloud
abersetz td fr ./docs --engine ll::siliconflow:Qwen/Qwen2.5-7B-Instruct

# Fully offline on Apple Silicon
abersetz td es ./docs --engine ml/mthy::7b-mlx

# Check what engines are configured
abersetz ls

# Dry run before burning credits
abersetz td ja ./docs --engine ll::openai:gpt-4o-mini --dry-run
```
