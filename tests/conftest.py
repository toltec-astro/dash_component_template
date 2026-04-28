"""Pytest configuration and fixtures for dash_component_template tests."""

from __future__ import annotations

import pytest
from dash import Dash, html

from dash_component_template import Template


@pytest.fixture
def reset_tree():
    """Reset the Template tree before and after each test.

    This ensures test isolation by clearing the class-level tree.
    """
    Template.reset_tree()
    yield
    Template.reset_tree()


@pytest.fixture
def basic_template(reset_tree):
    """Create a basic root template for testing.

    Returns
    -------
    Template
        A root template with name "root"
    """
    return Template(name="root")


@pytest.fixture
def nested_template(reset_tree):
    """Create a nested template hierarchy for testing.

    Returns
    -------
    tuple[Template, Template, Template]
        Tuple of (root, child1, grandchild1)
    """
    root = Template(name="root")
    child1 = Template(name="child1", _parent=root)
    grandchild1 = Template(name="grandchild1", _parent=child1)
    return root, child1, grandchild1


@pytest.fixture
def dash_app():
    """Create a basic Dash application for testing.

    Returns
    -------
    Dash
        A Dash application instance
    """
    return Dash(__name__)


class SimpleTemplate(Template):
    """Simple template for testing with container."""

    _component_cls = html.Div

    def layout(self):
        """Create simple layout with title and button."""
        self.title = self.child(html.H1, children="Test Title")
        self.button = self.child(html.Button, children="Click Me")
        # Call parent to create root component
        return super().layout()


class NestedTemplate(Template):
    """Template that nests other templates."""

    _component_cls = html.Div

    def __init__(self, num_children: int = 2, **kwargs) -> None:
        """Initialize with specified number of child templates."""
        super().__init__(**kwargs)
        self.num_children = num_children

    def layout(self):
        """Create layout with nested SimpleTemplate instances."""
        for i in range(self.num_children):
            child = self.child(SimpleTemplate, name=f"simple{i + 1}")
            child.layout()
        # Call parent to create root component
        return super().layout()


@pytest.fixture
def simple_template_class():
    """Provide SimpleTemplate class for testing."""
    return SimpleTemplate


@pytest.fixture
def nested_template_class():
    """Provide NestedTemplate class for testing."""
    return NestedTemplate


@pytest.fixture
def simple_template_instance(reset_tree):
    """Create a SimpleTemplate instance with layout."""
    template = SimpleTemplate(name="simple")
    template.layout()
    return template
