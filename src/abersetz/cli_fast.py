#!/usr/bin/env python
"""Fast CLI entry point that checks for --version before loading heavy modules.

Python imports can be slow. If the user just wants the version, we don't want to load PyTorch, MLX, or the entire translation pipeline. We intercept it here."""
# this_file: src/abersetz/cli_fast.py

import sys


def handle_version() -> None:
    """Handle --version flag with minimal imports.

    Scans `sys.argv`. If we see a version request, we print and exit immediately. No heavy lifting."""
    if "--version" in sys.argv or "version" in sys.argv:
        # Only import version, nothing else
        from importlib import metadata

        try:
            version = metadata.version("abersetz")
        except metadata.PackageNotFoundError:
            from .__about__ import __version__ as version  # type: ignore

        print(f"abersetz version {version}")
        sys.exit(0)


def main() -> None:
    """Fast CLI entry point that defers heavy imports.

    Checks the flags, and if it's a real command, hands off to the main `fire`-based CLI."""
    # Check for version flag first with minimal imports
    handle_version()

    # Now load the full CLI only if needed
    from .cli import main as cli_main

    cli_main()


if __name__ == "__main__":
    main()
