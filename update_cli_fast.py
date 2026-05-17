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

# cli_fast.py
cli_fast_replacements = [
    ('"""Fast CLI entry point that checks for --version before loading heavy modules."""',
     '"""Fast CLI entry point that checks for --version before loading heavy modules.\n\nPython imports can be slow. If the user just wants the version, we don\'t want to load PyTorch, MLX, or the entire translation pipeline. We intercept it here."""'),
    ('"""Handle --version flag with minimal imports."""',
     '"""Handle --version flag with minimal imports.\n\nScans `sys.argv`. If we see a version request, we print and exit immediately. No heavy lifting."""'),
    ('"""Fast CLI entry point that defers heavy imports."""',
     '"""Fast CLI entry point that defers heavy imports.\n\nChecks the flags, and if it\'s a real command, hands off to the main `fire`-based CLI."""')
]
replace_file_content("src/abersetz/cli_fast.py", cli_fast_replacements)

