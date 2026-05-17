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

# setup.py
setup_replacements = [
    ('"""Smart configuration setup for abersetz."""',
     '"""Smart configuration setup for abersetz.\n\nProvides a CLI wizard that sniffs your environment variables for API keys (OpenAI, Anthropic, DeepL, etc.), tests them to make sure they actually work, and builds a working `config.toml` so you don\'t have to."""'),
    ('"""Information about a discovered API provider."""',
     '"""Information about a discovered API provider.\n\nTracks whether we found a key, if the endpoint is breathing, and what engines can use it."""'),
    ('"""Interactive setup wizard for abersetz configuration."""',
     '"""Interactive setup wizard for abersetz configuration.\n\nThe brain behind `abersetz setup`. It runs through four phases: discover keys, test endpoints, build config, save and validate."""'),
    ('"""Run the setup wizard."""',
     '"""Run the setup wizard.\n\nCoordinates the discovery, testing, and saving phases. Returns True if a valid config was created, False if no API keys were found."""'),
    ('"""Run validation after configuration is saved."""',
     '"""Run validation after configuration is saved.\n\nFires off a quick request to every configured engine to make sure they aren\'t hallucinating or timing out immediately."""'),
    ('"""Scan environment for API keys."""',
     '"""Scan environment for API keys.\n\nChecks `os.environ` for known key patterns (like `OPENAI_API_KEY`) and registers providers when it finds them."""'),
    ('"""Test discovered endpoints with lightweight API calls."""',
     '"""Test discovered endpoints with lightweight API calls.\n\nWe don\'t just trust an API key exists; we poke the endpoint (usually the `/models` route) to see if it responds with a 200 OK."""'),
    ('"""Test a single API endpoint."""',
     '"""Test a single API endpoint.\n\nMakes a quick GET request to verify the key works. Catches timeouts, auth errors, and DNS failures."""'),
    ('"""Display discovered providers in a table."""',
     '"""Display discovered providers in a table.\n\nUses Rich to print a pretty summary of what we found and whether it works."""'),
    ('"""Generate configuration from discovered providers."""',
     '"""Generate configuration from discovered providers.\n\nTakes the raw list of working keys and builds a proper `AbersetzConfig` object, prioritizing stable engines (like DeepL) over generic ones (like Translators)."""'),
    ('"""Choose the default engine based on configured priorities."""',
     '"""Choose the default engine based on configured priorities.\n\nWe prefer DeepL if you have it. If not, Google Translate via `translators`. If not that, Hunyuan. If none of those, we just pick the first thing that works."""'),
    ('"""Run the abersetz setup wizard.',
     '"""Run the abersetz setup wizard.\n\n    The main entry point for the `setup` CLI command.')
]
replace_file_content("src/abersetz/setup.py", setup_replacements)

