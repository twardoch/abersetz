# Todo List

This file tracks the detailed tasks for Abersetz local model discovery and local situation support. Detailed requirements can be found in [issues/109.md](file:///Users/adam/Developer/vcs3/github.twardoch/pub/abersetz/issues/109.md) and [issues/110.md](file:///Users/adam/Developer/vcs3/github.twardoch/pub/abersetz/issues/110.md).

## Task 109: Local Model Discovery
- [x] Implement the `LocalModelFinder` scanner class in [local_discovery.py](file:///Users/adam/Developer/vcs3/github.twardoch/pub/abersetz/src/abersetz/providers/llm/local_discovery.py) to locate local AI model downloads.
  - [x] Query standard cache directories using platform-specific logic and `platformdirs`.
  - [x] Scan Hugging Face hub cache directory (`~/.cache/huggingface/hub`).
  - [x] Scan Ollama models directory (`~/.ollama/models`), with special support for extensionless SHA-256 files under the `blobs/` directory.
  - [x] Scan LM Studio models directory by reading `$HOME/.lmstudio-home-pointer` for custom paths, with standard path fallback (`~/.cache/lm-studio/models`).
  - [x] Scan Pinokio application model subdirectories (`~/pinokio`).
  - [x] Scan GPT4All model directories (`~/Library/Application Support/nomic.ai/GPT4All` on macOS, or `~/AppData/Local/nomic.ai/GPT4All` on Windows).
  - [x] Scan and filter files by standard extensions: `.gguf`, `.safetensors`, `.bin`, `.pt`, `.pth`, `.onnx`.
  - [x] Scan directory-based CoreML `.mlpackage` bundles recursively to calculate total package size without walking inside them.
  - [x] Support minimum file size threshold (default 100MB) to filter out config and metadata files.
  - [x] Implement a Fire-based CLI command execution entry point for local discovery.

## Task 110: Local Situation Support (Hunyuan-MT2)
- [x] Support automatic path resolution and usage of local Hunyuan-MT2 models for both GGUF and MLX backends (see [issues/110.md](file:///Users/adam/Developer/vcs3/github.twardoch/pub/abersetz/issues/110.md)).
  - [x] Map GGUF models:
    - `models/tencent/Hy-MT2-1.8B-2Bit-GGUF/Hy-MT2-1.8B-2Bit.gguf`
    - `models/tencent/Hy-MT2-1.8B-1.25Bit-GGUF/Hy-MT2-1.8B-1.25Bit.gguf`
    - `models/tencent/Hy-MT2-1.8B-GGUF/Hy-MT2-1.8B-Q8_0.gguf`
    - `models/tencent/Hy-MT2-7B-GGUF/HY-MT2-7B-Q8_0.gguf`
  - [x] Map MLX models:
    - `models/p0we7/Hy-MT2-1.8B-oQ8-fp16/`
    - `models/tevino/Hy-MT2-7B-oQ8/`
    - `models/QwQbb/Hy-MT2-30B-A3B-MLX-4bit/`
    - `models/sahilchachra/hy-mt2-7b-8bit-mlx/`
  - [x] Integrate local model finder into `resolve_and_download_model` in [mlx.py](file:///Users/adam/Developer/vcs3/github.twardoch/pub/abersetz/src/abersetz/providers/mlx.py).
  - [x] Explicitly block and raise `EngineError` for obsolete/unsupported Hunyuan-MT1.x models (e.g. `Hunyuan-MT-7B`, `Hunyuan-MT1`, `Hy-MT1`, `HY-MT1`).
  - [x] **Bugfix**: Ensure MLX local model resolution returns the directory containing the model weights (the parent directory of the matched weights file) rather than the path to the individual weight file, since `mlx_lm.load` expects a directory path.
  - [x] Add unit test for local MLX model resolution directory path returns in [test_local_discovery.py](file:///Users/adam/Developer/vcs3/github.twardoch/pub/abersetz/tests/test_local_discovery.py).

## Task 108.1.5: Benchmark Example Rewrite
- [x] Update [benchmark.py](file:///Users/adam/Developer/vcs3/github.twardoch/pub/abersetz/examples/benchmark.py) to support benchmarking specific providers separately.
  - [x] Support a `--providers` CLI parameter for a comma-separated list of provider names.
  - [x] Resolve provider name keywords dynamically to active engine configurations.
  - [x] Non-destructively merge new results in `benchmark_results.json` to keep previous data.
  - [x] Support both non-LLM (translators, deep-translator) and local LLM engines.

## Task 108.2: Verification and Quality Control
- [x] Write unit tests in [test_local_discovery.py](file:///Users/adam/Developer/vcs3/github.twardoch/pub/abersetz/tests/test_local_discovery.py) to cover scanning, filter by size, and alias resolution.
- [x] Write unit tests in [test_examples.py](file:///Users/adam/Developer/vcs3/github.twardoch/pub/abersetz/tests/test_examples.py) to verify benchmark runner and result merging.
- [x] Run full test suite, linting, formatting, and verify 100% success.
- [x] Update [CHANGELOG.md](file:///Users/adam/Developer/vcs3/github.twardoch/pub/abersetz/CHANGELOG.md) and [WORK.md](file:///Users/adam/Developer/vcs3/github.twardoch/pub/abersetz/WORK.md).
