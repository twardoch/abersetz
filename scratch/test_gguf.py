# this_file: scratch/test_gguf.py
from abersetz.config import EngineConfig
from abersetz.providers import LocalGgufEngine

try:
    engine = LocalGgufEngine(
        family="mthy",
        config=EngineConfig(name="mthy"),
        model_path="/Volumes/Falstaff4T/RomeoData2/lmstudio/models/tencent/Hy-MT2-1.8B-2Bit-GGUF/Hy-MT2-1.8B-2Bit.gguf",
        max_tokens=2048,
        temperature=0.0,
        n_gpu_layers=-1,
        n_ctx=4096,
    )
    print("Success: GGUF engine loaded!")
except Exception as e:
    print(f"Error: {e}")
    import traceback

    traceback.print_exc()
