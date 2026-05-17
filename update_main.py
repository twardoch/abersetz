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

# __main__.py
main_replacements = [
    ('"""Entry point for python -m abersetz."""',
     '"""Entry point for python -m abersetz.\n\nAllows users to run the CLI directly via the module rather than the installed bin script."""')
]
replace_file_content("src/abersetz/__main__.py", main_replacements)

