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

# chunking.py
chunking_replacements = [
    ('"""Text detection and chunking utilities."""',
     '"""Text detection and chunking utilities.\n\nWe need chunks because language models have limits, and web translators have temper tantrums if you send them too much at once. This splits text cleanly."""'),
    ('"""Minimal set of supported text formats."""',
     '"""Minimal set of supported text formats.\n\nWe keep this dead simple: plain text or HTML. That tells the splitter how to slice."""'),
    ('"""Detect whether ``text`` looks like HTML."""',
     '"""Detect whether `text` looks like HTML.\n\nIt searches for basic HTML tags. If it finds one, it assumes HTML. Otherwise, plain text."""'),
    ('"""Simple slicing fallback when semantic splitter is unavailable."""',
     '"""Simple slicing fallback when semantic splitter is unavailable.\n\nBrute-force slices a string into chunks of `max_size`. Not pretty, but it works if the semantic splitter is missing."""'),
    ('"""Prefer semantic-text-splitter when installed."""',
     '"""Prefer semantic-text-splitter when installed.\n\nSlices text at sensible boundaries (like sentences or paragraphs) rather than cutting words in half.\nFalls back to brute-force slicing if the library isn\'t installed."""'),
    ('"""Chunk text according to the detected format."""',
     '"""Chunk text according to the detected format.\n\nHTML currently gets passed whole (we don\'t split it yet). Plain text gets semantic splitting."""')
]
replace_file_content("src/abersetz/chunking.py", chunking_replacements)

# config.py
config_replacements = [
    ('"""Configuration helpers for abersetz."""',
     '"""Configuration helpers for abersetz.\n\nReads, writes, and validates `config.toml`. This handles everything from default engines to API keys and chunk sizes."""'),
    ('"""Runtime defaults for translation."""',
     '"""Runtime defaults for translation.\n\nWhat engine to use, source/target languages, and how big text chunks should be."""'),
    ('"""Represents an API credential reference."""',
     '"""Represents an API credential reference.\n\nCould be an environment variable name, an explicit key, or a named reference to another credential."""'),
    ('"""Engine specific configuration block."""',
     '"""Engine specific configuration block.\n\nHolds options, chunk sizes, and credentials for a specific translation engine (e.g., Google Translate, DeepL, or an LLM provider)."""'),
    ('"""Aggregate configuration for the toolkit."""',
     '"""Aggregate configuration for the toolkit.\n\nThe root configuration object holding defaults, credentials, and engine-specific setups."""'),
    ('"""Return a deep copy of the default config mapping."""',
     '"""Return a deep copy of the default config mapping.\n\nProvides a safe, immutable baseline for creating new configs or restoring broken ones."""'),
    ('"""Return a fresh ``AbersetzConfig`` with defaults."""',
     '"""Return a fresh `AbersetzConfig` populated with the default settings."""'),
    ('"""Return directory holding the configuration file."""',
     '"""Return the directory holding the configuration file.\n\nRespects the `ABERSETZ_CONFIG_DIR` env var if set, otherwise uses the OS-specific user config directory."""'),
    ('"""Return absolute path to the configuration file."""',
     '"""Return the absolute path to the `config.toml` file."""'),
    ('"""Load configuration from disk, creating defaults if needed."""',
     '"""Load configuration from disk, creating defaults if needed.\n\nIf the file is missing, we create it. If it\'s corrupted, we back it up and create a fresh one.\nReturns a valid `AbersetzConfig` object no matter what."""'),
    ('"""Persist configuration to ``config.toml``."""',
     '"""Persist configuration to `config.toml`."""'),
    ('"""Resolve a credential reference to a usable secret.\n\n    Returns None if no credential found, logs helpful messages.\n    """',
     '"""Resolve a credential reference to a usable secret string.\n\n    Checks named references, environment variables, and explicit values.\n    Returns `None` if no usable secret is found, logging a helpful error about what to fix.\n    """')
]
replace_file_content("src/abersetz/config.py", config_replacements)

