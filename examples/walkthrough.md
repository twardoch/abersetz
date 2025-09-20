---
this_file: examples/walkthrough.md
---
# Sample Translation Walkthrough

```bash
abersetz tr planslate examples/poem_en.txt \ \
  --engine hysf \
  --output examples/out \
  --save-voc \
  --verbose
```

The command writes the translated poem to `examples/out/poem_en.txt` and saves the evolving voc as `examples/out/poem_en.txt.voc.json`.
