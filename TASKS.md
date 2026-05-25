---
this_file: TASKS.md
---
# Abersetz Enhancements Plan (Task 108, 109 & 110)

## Scope (One Sentence)
Extend Abersetz with LM Studio auto-starting, modular LLM provider discovery with wildcard model matching, local model discovery (Issue 109), local situation support for Hunyuan-MT2 (Issue 110), htmladapt-based structured HTML translation, twat-cache and twat-task workflow integrations, and a flexible provider-centric benchmarking tool.

## Guiding Principles
- Avoid duplicating functionality; leverage local packages in `external/` via path dependencies.
- Ensure all tests run locally and verify both success and failure/fallback behaviors.
- Ensure backward compatibility: keep existing selector formats functional.

## Detailed Plan

### Phase 1: Dependency Integration & LM Studio Auto-Start
- Update `pyproject.toml` to declare local path sources for `htmladapt`, `twat`, `twat-cache`, and `twat-task`.
- Synchronize development environment with `uv sync --all-extras`.
- Modify `src/abersetz/providers/lmstudio.py` to:
  - Locate `lms` CLI tool.
  - Query status via `lms server status --json`.
  - Auto-start using `lms daemon up --json` if down.
  - Pass custom per-request `temperature` parameter.

### Phase 2: LLM Provider Registry & Modularization
- Move logic from `src/abersetz/providers/llm.py` into `src/abersetz/providers/llm/__init__.py`, `inference.py`, and `discovery.py`.
- Define dedicated provider files under `src/abersetz/providers/llm/api/` for `openai.py`, `siliconflow.py`, `groq.py`, `deepseek.py`, `gemini.py`, `openrouter.py`, `together.py`, `lmstudio.py`, and `anthropic.py`.
- Implement `fnmatch` wildcard model matching (e.g. `openrouter:*:free`).
- Add `src/abersetz/providers/llm/recommended_settings.json` to store recommended temperatures, context lengths, and chunk sizes.
- Expose `temperature` parameter through the CLI `--temperature` option and `TranslatorOptions`.

### Phase 3: htmladapt & Twat Integration
- Integrate `htmladapt` for HTML mode in `pipeline.py`:
  - Extract translatable content subset HTML using `HTMLExtractMergeTool.extract`.
  - Chunk translatable HTML elements at tags within chunk size limits.
  - Merge structural details back using `HTMLExtractMergeTool.merge`.
- Decorate chunk translation calls with `twat_cache.decorators.bcache` (disk-based persistent cache) to skip repeat requests.
- Expose a translation job task/flow using `twat_task` Prefect integration.

### Phase 4: Local Model Discovery (Issue 109)
- Implement `src/abersetz/providers/llm/local_discovery.py` featuring `LocalModelFinder`.
- Check paths: HuggingFace hub, Ollama, LMStudio pointer, Pinokio, GPT4All nomic folder.
- Parse formats: `.gguf`, `.safetensors`, `.bin`, `.pt`, `.pth`, `.onnx` and directory-based CoreML `.mlpackage`.
- Parse Ollama's custom `sha256-` blobs under the blobs folder.
- Expose a CLI tool using `fire` to scan/discover models.

### Phase 5: Local Hunyuan-MT2 Model Support (Issue 110)
- Mapped models: GGUF models (`Hy-MT2-1.8B-2Bit`, `Hy-MT2-1.8B-1.25Bit`, `Hy-MT2-1.8B`, `Hy-MT2-7B`) and MLX models (`1.8B-oQ8-fp16`, `7B-oQ8`, `30B-A3B-MLX-4bit`, `7b-8bit-mlx`).
- Avoid snapshot downloading if local finder discovers the model directory or gguf file on disk.
- Explicitly block obsolete Hunyuan-MT1.x models.

### Phase 6: Benchmarking Tool Rewrite
- Modify `./examples/benchmark.py` to resolve provider name keywords (e.g., `google`, `siliconflow`) into active engine configurations.
- Allow benchmarking all providers in sequence, separately, or via a comma-separated list of providers.
- Read existing `benchmark_results.json` and non-destructively update it.

## Verification Plan

### Automated Tests
- Test LM Studio check and startup logic.
- Test wildcard matching for model selectors.
- Test htmladapt extraction, element-based chunking, and merging.
- Test twat cache hits on repeat translations.
- Test local model finder scanning and format detection.
- Test Hy-MT2 local resolution.
- Run all Hatch tests: `uvx hatch test`.

### Manual Verification
- Run benchmark dry-run: `uv run examples/benchmark.py --providers google,lms,siliconflow --dry-run`.
- Verify validation command: `abersetz validate`.
