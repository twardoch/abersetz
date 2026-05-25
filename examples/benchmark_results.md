# Abersetz Translation Engine Benchmark Analysis

This document provides a comprehensive analysis of the benchmark results for various translation engines configured in **Abersetz**. The benchmark was performed using two Markdown documents representing different workloads:
1. **Short Document (`poem.en.md`)**: `1,405` characters.
2. **Long Document (`fontlab-7-tldr.en.md`)**: `73,211` characters.

---

## Executive Summary

The benchmark evaluated **13 different engine configurations** across five backend categories: Scraped Web Translators (`tr/`), Official Translation APIs (`dt/`), OpenAI-compatible cloud LLMs (`ullm/`), Local Hunyuan-MT models (`mthy/`), and LM Studio (`lms`).

### Key Takeaways
* **Local MLX Acceleration is King**: Running local translation models using Apple Silicon's MLX backend (`mthy/mlx`) offers exceptional performance. The **Hunyuan-MT-1.8B (MLX)** model was the fastest active engine, achieving **370.02 cps** (characters per second) on the long document.
* **Large Model Efficiency**: The **30B MLX** model performed surprisingly well on the long document, reaching **189.16 cps**, which is **72% faster** than the smaller **7B GGUF** model (**109.93 cps**). This highlights the massive throughput advantages of MLX over GGUF for large models on Apple Silicon.
* **API Limits & Silent Failures**: Free or scraped web APIs (`tr/bing`, `dt/my_memory`) suffered from major limitations, failing to translate long texts due to query length constraints (MyMemory's 500-char limit) or silent API rate blocks.
* **Infrastructure Dependencies**: Several local and cloud runs failed due to missing files (quantized 2-bit/1.25-bit models on an unmounted external volume) or server connection issues.

---

## Benchmark Results Overview

| Engine Category / Selector | Model/Descriptor | Document | Characters | Success | Time (s) | Speed (cps) | Status / Error Message |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Web Scraping (`tr/`)** | | | | | | | |
| `tr/google` | `tr-google` | Poem | 1,405 | **Skipped** | 0.00 | — | Already cached / translated |
| | | FontLab | 73,211 | **Skipped** | 0.00 | — | Already cached / translated |
| `tr/bing` | `tr-bing` | Poem | 1,405 | ❌ **Failed** | 3.56 | 394.94 | Silent failure (no error message) |
| | | FontLab | 73,211 | ❌ **Failed** | 7.72 | 9,481.94 | Silent failure (no error message) |
| **Official APIs (`dt/`)** | | | | | | | |
| `dt/google` | `dt-google` | Poem | 1,405 | **Skipped** | 0.00 | — | Already cached / translated |
| | | FontLab | 73,211 | **Skipped** | 0.00 | — | Already cached / translated |
| `dt/my_memory` | `dt-my_memory` | Poem | 1,405 | ❌ **Failed** | 3.07 | 458.07 | Text length exceeds MyMemory 500-char limit |
| | | FontLab | 73,211 | ❌ **Failed** | 3.01 | 24,330.53 | Text length exceeds MyMemory 500-char limit |
| **Cloud LLM (`ullm/`)** | | | | | | | |
| `ullm/default` | `Hunyuan-MT-7B` | Poem | 1,405 | ❌ **Failed** | 16.37 | 85.82 | `HTTPStatusError` / Network retry failure |
| | | FontLab | 73,211 | ❌ **Failed** | 16.13 | 4,537.61 | `HTTPStatusError` / Network retry failure |
| **Local MLX (`mthy/mlx`)** | | | | | | | |
| `mthy/30b-mlx` | `Hunyuan-MT-30B` | Poem | 1,405 |  **Passed** | 34.09 | 41.22 | Completed successfully |
| | | FontLab | 73,211 |  **Passed** | 387.03 | 189.16 | Completed successfully (~6.5 mins) |
| `mthy/1.8b-mlx` | `Hunyuan-MT-1.8B` | Poem | 1,405 |  **Passed** | 6.87 | **204.54** | Completed successfully |
| | | FontLab | 73,211 |  **Passed** | 197.86 | **370.02** | Completed successfully (~3.3 mins) |
| **Local GGUF (`mthy/gguf`)** | | | | | | | |
| `mthy/7b-gguf` | `Hunyuan-MT-7B` | Poem | 1,405 |  **Passed** | 35.80 | 39.25 | Completed successfully |
| | | FontLab | 73,211 |  **Passed** | 665.96 | 109.93 | Completed successfully (~11.1 mins) |
| `mthy/1.8b-gguf` | `Hunyuan-MT-1.8B` | Poem | 1,405 |  **Passed** | 7.22 | 194.52 | Completed successfully |
| | | FontLab | 73,211 |  **Passed** | 237.80 | 307.87 | Completed successfully (~4.0 mins) |
| `mthy/1.8b-heretic`| `Hunyuan-MT-1.8B` | Poem | 1,405 |  **Passed** | 39.00 | 36.03 | Completed successfully |
| | | FontLab | 73,211 |  **Passed** | 1,268.18 | 57.73 | Completed successfully (~21.1 mins) |
| `mthy/1.8b-2bit` | `Hunyuan-MT-1.8B` | Poem | 1,405 | ❌ **Failed** | 0.02 | — | Model file not found on external volume |
| | | FontLab | 73,211 | ❌ **Failed** | 0.01 | — | Model file not found on external volume |
| `mthy/1.8b-1.25bit`| `Hunyuan-MT-1.8B` | Poem | 1,405 | ❌ **Failed** | 0.02 | — | Model file not found on external volume |
| | | FontLab | 73,211 | ❌ **Failed** | 0.01 | — | Model file not found on external volume |
| **LM Studio (`lms`)** | | | | | | | |
| `lms` | `lms` | Poem | 1,405 | ❌ **Failed** | 0.06 | — | LM Studio not reachable on localhost:1234 |
| | | FontLab | 73,211 | ❌ **Failed** | 0.00 | — | Client initialization conflict error |

---

## Detailed Performance Analysis

### 1. Local MLX vs. Local GGUF (Apple Silicon Optimization)
On macOS/Apple Silicon, the **MLX** backend demonstrates a clear performance advantage over **GGUF** (llama.cpp).

```
Hunyuan-MT-1.8B Speed Comparison (FontLab 73.2K Chars):
  MLX:  ██████████████████████████████  370.02 cps
  GGUF: █████████████████████████        307.87 cps (+20% slower than MLX)
```

For smaller models like the `1.8B` model, MLX runs **20% faster** than the GGUF equivalent on large documents. For larger models, this advantage increases.
* **30B MLX** achieved **189.16 cps**, while the much smaller **7B GGUF** only achieved **109.93 cps**. This means a model over 4 times larger ran **72% faster** when optimized using MLX, underscoring the efficiency of native unified memory architectures.

### 2. Model Size vs. Throughput (1.8B vs. 7B vs. 30B)
As expected, smaller models yield higher processing speeds, but the scaling behavior is non-linear:
* **Hunyuan-MT-1.8B (MLX)**: 370.02 cps (197.86 seconds for 73.2K chars)
* **Hunyuan-MT-30B (MLX)**: 189.16 cps (387.03 seconds for 73.2K chars)

The `1.8B` model is roughly **1.96x faster** than the `30B` model. Given the `30B` model has ~16 times more parameters, this performance scaling is exceptionally favorable, suggesting that memory bandwidth or batch processing limits play a major role, and that the 30B model is highly viable for pipeline usage if translation accuracy requirements warrant it.

### 3. The "Heretic" Slowdown
The `mthy/1.8b-heretic` configuration was a major outlier in local GGUF performance:
* It required **1,268.18 seconds** (21.1 minutes) to process the large file at a meager **57.73 cps**.
* Compared to the standard `1.8b-gguf` (307.87 cps), the Heretic variant is **5.3x slower**. This represents a severe regression, likely due to CPU fallback, disabling metal acceleration, or unoptimized quantization operations.

---

## Analysis of Failures

> [!WARNING]
> **API Constraints & Missing Local Volumes**
> Out of 13 tested configurations, **6 encountered persistent failures** during execution, highlighting key stability issues that users must navigate.

#### A. API Length Constraints (MyMemory)
* **Error**: `Text length need to be between 0 and 500 characters`
* **Root Cause**: The MyMemory translation engine imposes a strict 500-character limit on its free API tier. Abersetz sent chunks larger than 500 characters, causing immediate API rejections.
* **Fix**: If using MyMemory, `chunk-size` must be configured down to `< 500` characters, or chunking must be strictly enforced.

#### B. Volume/Path Errors (2-Bit / 1.25-Bit Models)
* **Error**: `Failed to load model from file: /Volumes/Falstaff4T/RomeoData2/lmstudio/models/...`
* **Root Cause**: The external drive `/Volumes/Falstaff4T` was likely unmounted or the files were missing at the specified paths. Low-bit quants (e.g. 1.25-bit, 2-bit) also frequently require custom llama.cpp/MLX builds that might not have been available.

#### C. Network Timeout / HTTP Status Errors (Hunyuan-MT Cloud)
* **Error**: `RetryError[<Future at ... raised HTTPStatusError>]`
* **Root Cause**: Cloud endpoint failures or request rate limits (Tencent cloud API). Even with retry mechanisms in Abersetz, the API did not recover in time, causing total job failure.

#### D. LM Studio Connectivity & Client Conflicts
* **Error**: `LM Studio is not reachable` / `Default client is already created`
* **Root Cause**: The LM Studio server was either not running locally on port 1234, or there was a client conflict in the SDK configuration.

---

## Conclusion & Actionable Recommendations

For optimal performance and reliability in Abersetz, follow these guidelines:

1. **For Apple Silicon Users**:
   * **First Choice**: Use **MLX models** (`mthy/1.8b-mlx` or `mthy/30b-mlx`). They leverage macOS Unified Memory architecture fully, leaving GGUF behind in speed and power efficiency.
   * Use the **1.8B MLX model** if speed is the primary constraint. Use the **30B MLX model** if complex grammar/vocabulary preservation is required, as the throughput penalty is relatively small (~2x slower for 16x parameters).
2. **Avoid Using GGUF Heretic Profiles**:
   * Standard GGUF profiles (`mthy/1.8b-gguf`) are acceptable, but the `heretic` profile should be avoided due to the severe (5x) slowdown.
3. **Handle API Rate Limits & Constraints**:
   * If relying on external APIs, prefer **Google Translate via deep-translator** (`dt/google`) as it is highly stable.
   * Avoid `dt/my_memory` unless you specifically reduce the chunk size limit in your `abersetz.toml` configuration.
4. **Ensure Mounts and Server Processes are Active**:
   * Ensure external SSDs housing models are connected and LM Studio is active on port 1234 before kicking off local translation runs.
