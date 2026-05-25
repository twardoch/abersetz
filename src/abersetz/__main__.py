"""Entry point for python -m abersetz and the uvx bin script.

Allows users to run the CLI directly via the module or as an installed binary, delegating to the fast CLI handler to speed up start times."""
# this_file: src/abersetz/__main__.py

from .cli_fast import main

if __name__ == "__main__":
    main()
