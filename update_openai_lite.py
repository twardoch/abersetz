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

# openai_lite.py
openai_lite_replacements = [
    ('"""Lightweight HTTP client for OpenAI-compatible APIs."""',
     '"""Lightweight HTTP client for OpenAI-compatible APIs.\n\nWe don\'t need the massive official `openai` package just to make a few POST requests. This handles the basics: auth, JSON payloads, and error raising."""'),
    ('"""A lightweight implementation of the OpenAI client for basic chat completions."""',
     '"""A lightweight implementation of the OpenAI client for basic chat completions.\n\nMimics the official API structure enough that our engines don\'t know the difference."""')
]
replace_file_content("src/abersetz/openai_lite.py", openai_lite_replacements)

# setup.py (skip for now since we haven't read it yet)
