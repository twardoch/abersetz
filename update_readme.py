import os

def replace_file_content(path, replacements):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
        else:
            print(f"Warning: could not find text to replace in {path}")
            
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {path}")

# README.md
readme_replacements = [
    ('A minimalist file translator that uses established machine translation engines while keeping configuration portable and repeatable. It follows a simple pipeline: locate → chunk → translate → merge. Provides both a Python API and a CLI powered by `fire`.',
     'Abersetz takes text files, translates them using modern AI engines, and spits them back out without breaking formatting. It skips the bloated frameworks and focuses on a simple pipeline: locate → chunk → translate → merge.\n\nBuilt for developers who want translations to "just work" from the terminal or via Python API.'),
    ('## Why abersetz?',
     '## Why abersetz?\n\nStop writing custom scripts to loop over files and call OpenAI. Abersetz gives you:\n'),
    ('- Translates files, not just strings.',
     '- **File-First**: Translates entire directories of markdown or text, not just short strings.'),
    ('- Supports engines from `translators`, `deep-translator`, and pluggable LLM-based backends for consistent terminology.',
     '- **Engine Agnostic**: Speak to standard APIs (Google, DeepL via `translators`/`deep-translator`) or modern LLMs (OpenAI, Anthropic, SiliconFlow).'),
    ('- Stores engine preferences and credentials using `platformdirs`, supporting either raw values or environment variables.',
     '- **Zero Secrets in Code**: Reads API keys from environment variables or a portable `.toml` config.'),
    ('- Shares vocabulary across chunks to maintain consistency in long documents.',
     '- **Memory**: Accumulates vocabulary terms across chunks so the 10th paragraph uses the same jargon as the 1st.'),
    ('- Keeps the codebase small: no custom infrastructure, just clear components doing their job.',
     '- **Tiny footprint**: Minimal dependencies. No enterprise bloat.'),
    ('## Key Features',
     '## Key Features'),
    ('- Recursive file discovery with include/exclude filters.',
     '- **Smart Discovery**: `abtr es ./docs --xclude "*.draft.md"` finds files recursively but ignores the drafts.'),
    ('- Automatic HTML vs. plain-text detection to preserve markup where possible.',
     '- **Format Awareness**: Detects HTML versus plain text and adjusts chunking strategies to avoid breaking tags.'),
    ('- Semantic chunking via `semantic-text-splitter`, with per-engine configurable lengths.',
     '- **Semantic Slicing**: Splits massive files by sentences and paragraphs, not arbitrarily through the middle of words.'),
    ('- Vocabulary-aware translation pipeline that merges `<voc>` JSON output from LLM engines.',
     '- **Vocab Sync**: LLMs can return `<voc>{"term":"translation"}</voc>` pairs which are fed into subsequent chunks.'),
    ('- Dry-run mode for offline testing and demos.',
     '- **Dry Run**: `abtr pl ./file.txt --dry-run` to verify paths without burning API credits.'),
    ('- Optional vocabulary sidecar files when `--save-voc` is enabled.',
     '- **Sidecars**: `--save-voc` drops a `.voc.json` file next to the translation so you can see what terms the engine learned.'),
    ('- Built-in `abersetz validate` command that pings configured engines, reports latency, and shows pricing hints from the research catalog.',
     '- **Health Checks**: `abersetz validate` pings engines with "Hello, world!" and reports latency to prove your keys work.'),
    ('- Optional local MLX/GGUF engines for HY-MT and TranslateGemma when configured (`mthy`, `gemma`).',
     '- **Local Models**: Run heavy-hitters like Tencent\'s Hunyuan-MT entirely locally via MLX or GGUF.')
]
replace_file_content("README.md", readme_replacements)

