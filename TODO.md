---
this_file: TODO.md
---

## Phase 1

- [x] Refactor ./src/abersetz/ : split up providers into separate modules inside ./src/abersetz/providers/ 
- [x] Add support for the Hy-MT2 MLX models (make sure to support the LMStudio locations of these models if downloaded, otherwise download them using standard HuggingFace tooling, and support the location): 
  - /Volumes/Falstaff4T/RomeoData2/lmstudio/models/QwQbb/Hy-MT2-30B-A3B-MLX-4bit 
  - /Volumes/Falstaff4T/RomeoData2/lmstudio/models/p0we7/Hy-MT2-1.8B-oQ8-fp16 
- [x] Add support for the Hy-MT2 GGUF models: 
  - /Volumes/Falstaff4T/RomeoData2/lmstudio/models/tencent/Hy-MT2-7B-GGUF/HY-MT2-7B-Q8_0.gguf 
  - /Volumes/Falstaff4T/RomeoData2/lmstudio/models/mradermacher/Hy-MT2-1.8B-heretic-GGUF/Hy-MT2-1.8B-heretic.Q8_0.gguf 
  - /Volumes/Falstaff4T/RomeoData2/lmstudio/models/tencent/Hy-MT2-1.8B-GGUF/Hy-MT2-1.8B-Q8_0.gguf 
  - /Volumes/Falstaff4T/RomeoData2/lmstudio/models/tencent/Hy-MT2-1.8B-2Bit-GGUF/Hy-MT2-1.8B-2Bit.gguf 
  - /Volumes/Falstaff4T/RomeoData2/lmstudio/models/tencent/Hy-MT2-1.8B-1.25Bit-GGUF/Hy-MT2-1.8B-1.25Bit.gguf 
- [x] Remove support for the Hy-MT1.x models. 
- [x] Make sure the new Hy-MT2 model support works with the new prompting format described in 
    - [x] https://huggingface.co/tencent/Hy-MT2-30B-A3B
    - [x] https://huggingface.co/tencent/Hy-MT2-7B
    - [x] https://huggingface.co/tencent/Hy-MT2-1.8B
    - [x] https://github.com/Tencent-Hunyuan/Hy-MT2
- [x] Make sure we support https://github.com/Tencent/AngelSlim and the models https://huggingface.co/tencent/Hy-MT2-1.8B-2Bit-GGUF and https://huggingface.co/tencent/Hy-MT2-1.8B-1.25Bit-GGUF 
- [x] Make sure you use native MLX and GGUF engines, or alternatively the LMStudio package. Note that the 1.25bit and 2bit quantizations may need some special versions. You must autonomously and relentlessly research, implement and test. 


## Phase 2

- [x] Add `--include-community` flag to setup for community/self-hosted engines.
- [ ] Automate provider metadata extraction from `external/translators.txt` and `external/deep-translator.txt`.
- [ ] Sync pricing/tier hints into setup output using current provider research.
- [ ] Add structured hints for optional packages (for example `translators[google]`).
- [ ] Add docs guidance on picking engines based on cost and availability.
- [ ] Ensure docs link checks/CLI validation flows have regression coverage.
