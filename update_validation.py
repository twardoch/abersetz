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

# validation.py
validation_replacements = [
    ('"""Runtime engine validation utilities."""',
     '"""Runtime engine validation utilities.\n\nPings your configured engines with a tiny string ("Hello, world!") to see what breaks. Handles timeouts, measures latency, and catches auth errors before you try translating a massive novel."""'),
    ('"""Outcome of validating a single engine selector."""',
     '"""Outcome of validating a single engine selector.\n\nTracks whether the test translation worked, how long it took, what the result was, or what exploded."""'),
    ('"""Validate configured engines by performing a tiny translation."""',
     '"""Validate configured engines by performing a tiny translation.\n\nFires the test string through the engines, measures the time, and catches any errors. Used heavily by the `setup` wizard and `validate` CLI commands."""')
]
replace_file_content("src/abersetz/validation.py", validation_replacements)

