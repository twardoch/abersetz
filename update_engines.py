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

# engines.py
engines_replacements = [
    ('"""Translation engine adapters."""',
     '"""Translation engine adapters.\n\nThe translation muscle. This file hooks up the pipeline to different backends—from local models to cloud translation APIs to LLMs. It handles retries, batching hints, and prompt formatting so the rest of the app doesn\'t have to."""'),
    ('"""Raised when an engine cannot be constructed or invoked."""',
     '"""Raised when an engine cannot be constructed or invoked.\n\nCatch this when API keys are missing, dependencies aren\'t installed, or an engine throws an unrecoverable fit."""'),
    ('"""Resolve HY-MT language code/name to Chinese label."""',
     '"""Resolve HY-MT language code/name to Chinese label.\n\nHunyuan-MT requires target languages written in Chinese. This translates ISO codes or English names into what the model understands."""'),
    ('"""Payload passed to engines."""',
     '"""Payload passed to engines.\n\nEverything an engine needs to translate one chunk: the text, the languages, format flags, and vocabulary hints."""'),
    ('"""Normalized engine output."""',
     '"""Normalized engine output.\n\nContains the translated text and any new vocabulary terms the engine learned/decided on during this chunk."""'),
    ('"""Protocol implemented by engine adapters."""',
     '"""Protocol implemented by engine adapters.\n\nAny new translation backend must implement this interface. It defines how to translate a chunk and what size chunks it prefers."""'),
    ('"""Shared helpers for engines."""',
     '"""Shared helpers for engines.\n\nBase class providing default chunk sizing logic."""'),
    ('"""Local MLX-backed engine for HY-MT and TranslateGemma."""',
     '"""Local MLX-backed engine for HY-MT and TranslateGemma.\n\nRuns models locally on Apple Silicon using MLX. Fast, private, but requires hefty hardware."""'),
    ('"""Local GGUF-backed engine for HY-MT and TranslateGemma."""',
     '"""Local GGUF-backed engine for HY-MT and TranslateGemma.\n\nRuns quantized models locally via llama.cpp. Great for standard hardware where MLX isn\'t an option."""'),
    ('"""Wrapper around the `translators` package with retry logic."""',
     '"""Wrapper around the `translators` package with retry logic.\n\nHooks into the `translators` Python library to scrape/use web-based translation endpoints (Google, Bing, etc.). Since these are often undocumented web endpoints, we wrap calls in a tenacious retry loop."""'),
    ('"""Adapter for `deep-translator` providers with retry logic."""',
     '"""Adapter for `deep-translator` providers with retry logic.\n\nHooks into `deep-translator` for more stable, often officially-supported web translation APIs. We still retry on network hiccups."""'),
    ('"""Shared logic for LLM backed engines."""',
     '"""Shared logic for LLM backed engines.\n\nTalks to OpenAI-compatible endpoints. It wraps the text in XML tags, feeds it to the LLM, and extracts the translation from the resulting `<output>` block."""'),
    ('"""Specialised HYSF engine with fixed prompt semantics."""',
     '"""Specialised HYSF engine with fixed prompt semantics.\n\nTencent\'s Hunyuan model works best with a very specific, simple prompt structure. This engine bypasses the XML-heavy LLM logic for a more direct approach."""'),
    ('"""Create an OpenAI client respecting optional base URL."""',
     '"""Create an OpenAI client respecting optional base URL.\n\nPoints the client at OpenAI, SiliconFlow, or any local proxy that speaks the OpenAI protocol."""'),
    ('"""Factory that builds the requested engine supporting short aliases."""',
     '"""Factory that builds the requested engine supporting short aliases.\n\nGive it `tr/google` and it builds a TranslatorsEngine backed by Google. Give it `hy/hysf` and it builds a SiliconFlow endpoint. It wires up the config, credentials, and adapter."""')
]
replace_file_content("src/abersetz/engines.py", engines_replacements)

# engine_catalog.py
catalog_replacements = [
    ('"""Engine catalog utilities for abersetz."""',
     '"""Engine catalog utilities for abersetz.\n\nResolves engine aliases (like `tr/google`) into their full internal names (`translators`, variant `google`). It also maintains lists of which providers are free, paid, or community-supported."""'),
    ('"""Return canonical short selector for supported engine families."""',
     '"""Return canonical short selector for supported engine families.\n\nTurns things like `translators/google` into `tr/google`. Keeps the CLI and config tidy."""'),
    ('"""Resolve selector (short or long) into engine config key and variant."""',
     '"""Resolve selector (short or long) into engine config key and variant.\n\nTurns `tr/google` into `(\"translators\", \"google\")` so the factory knows exactly what to build."""'),
    ('"""Return translator providers available in current environment."""',
     '"""Return translator providers available in current environment.\n\nChecks what the `translators` library actually supports on your machine right now."""'),
    ('"""Return deep-translator providers supported by abersetz."""',
     '"""Return deep-translator providers supported by abersetz.\n\nLists the `deep-translator` backends we know how to talk to."""'),
    ('"""Descriptor for CLI listing."""',
     '"""Descriptor for CLI listing.\n\nUsed by the `--list-engines` command to format output."""')
]
replace_file_content("src/abersetz/engine_catalog.py", catalog_replacements)

