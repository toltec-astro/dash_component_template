"""Tests for package metadata exposed by the public module."""

from importlib.metadata import version

import dash_component_template


def test_package_version_comes_from_installed_metadata():
    """The package must import cleanly from an editable installation."""
    assert dash_component_template.__version__ == version("dash_component_template")
