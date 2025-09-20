"""Test suite for abersetz."""
# this_file: tests/test_package.py


def test_version() -> None:
    """Verify package exposes version."""
    import abersetz

    assert abersetz.__version__
