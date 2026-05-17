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

# pipeline.py
pipeline_replacements = [
    ('"""High level translation pipeline."""',
     '"""High level translation pipeline.\n\nThe brain of the operation. This takes a file or directory, figures out what text format it is, chops it up into digestible chunks, sends it to the translation engine, and stitches it all back together into a finished file."""'),
    ('"""Runtime options controlling translation behaviour."""',
     '"""Runtime options controlling translation behaviour.\n\nAll the settings passed down from the CLI or library call: what engine to use, where to save things, what to include/exclude, etc."""'),
    ('"""Information about a translated artefact."""',
     '"""Information about a translated artefact.\n\nReturned when a file is finished. Tells you where the output was saved, what engine was used, how many chunks it took, and what vocabulary was accumulated."""'),
    ('"""Raised when translation cannot proceed."""',
     '"""Raised when translation cannot proceed.\n\nCatch this if you pass a bad path, lack read permissions, or something breaks catastrophically in the middle of translation."""'),
    ('"""Translate a file or directory tree."""',
     '"""Translate a file or directory tree.\n\nThe main entry point. Resolves paths, merges user options with defaults, finds all matching files, spins up the right engine, and feeds everything through the pipeline."""')
]
replace_file_content("src/abersetz/pipeline.py", pipeline_replacements)

