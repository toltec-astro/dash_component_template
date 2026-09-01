"""Top-level package for dash_component_template."""

from importlib.metadata import version

from .lazy_component import (
    LazyComponent,
)
from .template import Template, callback_scope
from .wrapped_component import WrappedComponent

__author__ = """Zhiyuan Ma"""
__email__ = "zhiyuanma@umass.edu"
__version__ = version("dash_component_template")

__all__ = [
    "LazyComponent",
    "Template",
    "WrappedComponent",
    "callback_scope",
]
