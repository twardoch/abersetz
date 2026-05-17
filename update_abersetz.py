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

# abersetz.py
abersetz_replacements = [
    ('"""Legacy shim exporting the primary pipeline API."""',
     '"""Legacy shim exporting the primary pipeline API.\n\nKept around so scripts relying on `from abersetz.abersetz import translate_path` don\'t suddenly break."""')
]
replace_file_content("src/abersetz/abersetz.py", abersetz_replacements)

