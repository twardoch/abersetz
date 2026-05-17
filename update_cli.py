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

# cli.py
cli_replacements = [
    ('"""Command line interface for abersetz."""',
     '"""Command line interface for abersetz.\n\nThe user-facing CLI. This translates terminal commands into pipeline options, formats output nicely with Rich, and handles the `abersetz tr` and `abersetz config` subcommands."""'),
    ('"""Validate language code format."""',
     '"""Validate language code format.\n\nEnsures the user didn\'t pass gibberish for a language code, though currently it mostly trusts the user."""'),
    ('"""Abersetz translation tool - translate files between languages.\n\n    Use \'abersetz tr\' to translate files, or \'abersetz config\' to manage configuration.\n    """',
     '"""Abersetz translation tool.\n\n    The main CLI application. Exposes `tr` for translation, `config` for settings, `lang` for language codes, and `engines` to see what backends are available.\n    """'),
    ('"""Show version information."""',
     '"""Show version information.\n\nPrints the current version of abersetz."""'),
    ('"""Configuration related helpers."""',
     '"""Configuration related helpers.\n\nSubcommands under `abersetz config` to show the current setup or print the config file path."""'),
    ('"""List available engines and whether they are configured."""',
     '"""List available engines and whether they are configured.\n\nPrints a formatted table showing every engine we know about, whether you have it set up, and if it requires a paid API key."""'),
    ('"""Validate configured engines by translating a short phrase."""',
     '"""Validate configured engines by translating a short phrase.\n\nFires a test string ("Hello, world!") through the selected engines to measure latency and verify they actually work."""'),
    ('"""Invoke the Fire CLI."""',
     '"""Invoke the Fire CLI.\n\nTurns the `AbersetzCLI` class into a command-line application."""'),
    ('"""Direct translation CLI - equivalent to \'abersetz tr\'."""',
     '"""Direct translation CLI.\n\nA shortcut command. `abtr es file.txt` is exactly the same as `abersetz tr es file.txt`."""')
]
replace_file_content("src/abersetz/cli.py", cli_replacements)

