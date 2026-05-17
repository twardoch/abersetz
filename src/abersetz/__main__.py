"""Entry point for python -m abersetz.

Allows users to run the CLI directly via the module rather than the installed bin script."""
# this_file: src/abersetz/__main__.py

from .cli import main

if __name__ == "__main__":
    main()
