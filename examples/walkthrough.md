---
this_file: examples/walkthrough.md
---
# Sample Translation Walkthrough

```bash
abersetz translate examples/poem_en.txt \
  --to-lang pl \
  --engine hysf \
  --output examples/out \
  --save-voc \
  --verbose
```

The command writes the translated poem to `examples/out/poem_en.txt` and saves the evolving vocabulary as `examples/out/poem_en.txt.vocabulary.json`.
