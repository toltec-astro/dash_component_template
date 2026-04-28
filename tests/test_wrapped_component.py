"""Tests for WrappedComponent class.

Tests the pattern of wrapping existing Dash components into the template tree while
maintaining tree structure for organization and keeping original component unchanged.
"""

import pytest
from dash import dcc, html

from dash_component_template.lazy_component import LazyComponent
from dash_component_template.wrapped_component import WrappedComponent


@pytest.fixture(autouse=True)
def reset_class_counters():
    """Reset class counters before each test."""
    # Reset counters for all classes
    from dash_component_template.idtree import IdTree

    IdTree._class_counters.clear()
    yield
    # Clean up after test
    IdTree._class_counters.clear()


class TestWrappedComponentBasics:
    """Test basic WrappedComponent functionality."""

    def test_wrap_component_without_id(self):
        """Wrap component without ID attribute."""
        button = html.Button("Click me")
        wrapped = WrappedComponent(button)

        # Should have component
        assert wrapped.component is button

        # Should have auto-generated tree ID using component class name
        assert wrapped.id == "button0"

    def test_wrap_component_with_id(self):
        """Wrap component with ID attribute."""
        button = html.Button("Click me", id="my-button")
        wrapped = WrappedComponent(button)

        # Component unchanged
        assert wrapped.component is button
        assert getattr(button, "id", None) == "my-button"

        # Tree ID uses wrapped component class name (not component ID)
        assert wrapped.id == "button0"

    def test_multiple_wrapped_components(self):
        """Multiple wrapped components get unique tree IDs."""
        button1 = html.Button("Button 1")
        button2 = html.Button("Button 2")
        button3 = html.Button("Button 3")

        wrapped1 = WrappedComponent(button1)
        wrapped2 = WrappedComponent(button2)
        wrapped3 = WrappedComponent(button3)

        assert wrapped1.id == "button0"
        assert wrapped2.id == "button1"
        assert wrapped3.id == "button2"


class TestWrappedComponentWithParent:
    """Test WrappedComponent in tree hierarchy."""

    def test_wrapped_as_child(self):
        """WrappedComponent can be child of LazyComponent node."""
        root = LazyComponent()
        button = html.Button("Click me")
        wrapped = WrappedComponent(button, _parent=root)

        # Tree structure correct
        assert wrapped.parent == root

        # Tree ID includes parent prefix and uses component class name
        assert wrapped.id == f"{root.id}-button0"

        # Component unchanged
        assert wrapped.component is button

    def test_wrapped_as_parent(self):
        """WrappedComponent can be parent of other nodes."""
        button = html.Button("Container")
        wrapped = WrappedComponent(button)

        child1 = LazyComponent(_parent=wrapped)
        child2 = LazyComponent(_parent=wrapped)

        # Tree structure correct
        assert child1.parent == wrapped
        assert child2.parent == wrapped

        # Children use wrapped's tree ID (button0)
        assert child1.id == "button0-lazycomponent0"
        assert child2.id == "button0-lazycomponent1"

    def test_complex_hierarchy(self):
        """WrappedComponent in complex hierarchy."""
        # Root LazyComponent
        root = LazyComponent()

        # Wrapped component as child
        div = html.Div()
        wrapped_div = WrappedComponent(div, _parent=root)

        # Regular LazyComponent as child of wrapped
        section = LazyComponent(_parent=wrapped_div)

        # Another wrapped as child of section
        button = html.Button("Click")
        wrapped_button = WrappedComponent(button, _parent=section)

        # Check tree IDs using component class names
        assert root.id == "lazycomponent0"
        assert wrapped_div.id == "lazycomponent0-div0"
        assert section.id == "lazycomponent0-div0-lazycomponent1"
        assert wrapped_button.id == "lazycomponent0-div0-lazycomponent1-button1"


class TestWrappedComponentTreeManipulation:
    """Test tree manipulation with WrappedComponent."""

    def test_attach_wrapped_to_parent(self):
        """Attach WrappedComponent to parent updates tree ID."""
        button = html.Button("Click")
        wrapped = WrappedComponent(button)

        # Initially root with component class name
        assert wrapped.id == "button0"

        # Attach to parent
        root = LazyComponent()
        wrapped.parent = root

        # Tree ID updated with parent prefix
        assert wrapped.id == f"{root.id}-button0"

        # Component unchanged
        assert wrapped.component is button

    def test_detach_wrapped_from_parent(self):
        """Detach WrappedComponent from parent."""
        root = LazyComponent()
        button = html.Button("Click")
        wrapped = WrappedComponent(button, _parent=root)

        assert wrapped.id == f"{root.id}-button0"

        # Detach
        wrapped.parent = None

        # Tree ID simplified to component class name
        assert wrapped.id == "button0"

    def test_move_wrapped_between_parents(self):
        """Move WrappedComponent between parents."""
        parent1 = LazyComponent()
        parent2 = LazyComponent()
        button = html.Button("Click")
        wrapped = WrappedComponent(button, _parent=parent1)

        assert wrapped.id == f"{parent1.id}-button0"

        # Move to parent2
        wrapped.parent = parent2

        # Tree ID uses new parent
        assert wrapped.id == f"{parent2.id}-button0"


class TestWrappedComponentIDIndependence:
    """Test that tree ID is independent of component manipulation."""

    def test_tree_manipulation_doesnt_affect_component(self):
        """Tree manipulation doesn't change component."""
        parent1 = LazyComponent()
        parent2 = LazyComponent()
        button = html.Button("Click", id="btn-id")
        wrapped = WrappedComponent(button, _parent=parent1)

        original_component_id = getattr(button, "id", None)

        # Move in tree
        wrapped.parent = parent2
        wrapped.parent = None

        # Component ID never changed
        assert getattr(button, "id", None) == original_component_id


class TestWrappedComponentWithVariousComponents:
    """Test wrapping different types of Dash components."""

    def test_wrap_html_div(self):
        """Wrap html.Div component."""
        div = html.Div(children=["Content"])
        wrapped = WrappedComponent(div)

        assert wrapped.component is div
        assert wrapped.id == "div0"

    def test_wrap_dcc_graph(self):
        """Wrap dcc.Graph component."""
        graph = dcc.Graph(figure={})
        wrapped = WrappedComponent(graph)

        assert wrapped.component is graph
        assert wrapped.id == "graph0"

    def test_wrap_html_button(self):
        """Wrap html.Button component."""
        button = html.Button("Click")
        wrapped = WrappedComponent(button)

        assert wrapped.component is button
        assert isinstance(wrapped.id, str)

    def test_wrap_html_div_with_id(self):
        """Wrap html.Div with ID."""
        div_elem = html.Div(id="div-1")
        wrapped = WrappedComponent(div_elem)

        assert wrapped.component is div_elem
        # Tree ID uses wrapped component class name (not component ID)
        assert wrapped.id == "div0"


class TestWrappedComponentCacheInvalidation:
    """Test cache invalidation with WrappedComponent."""

    def test_cache_invalidation_on_attachment(self):
        """Cache invalidated when attaching to parent."""
        button = html.Button("Click")
        wrapped = WrappedComponent(button)
        root = LazyComponent()

        # Access ID to populate cache
        _ = wrapped.id
        assert "_id_cached" in wrapped._tree.__dict__

        # Attach to parent
        wrapped.parent = root

        # Cache should be invalidated and repopulated
        assert "_id_cached" in wrapped._tree.__dict__
        assert wrapped.id == f"{root.id}-button0"

    def test_smart_invalidation_with_wrapped(self):
        """Smart invalidation works with WrappedComponent."""
        root = LazyComponent()  # componenttemplate0
        button = html.Button("Click")
        wrapped = WrappedComponent(button, _parent=root)  # button0
        child = LazyComponent(_parent=wrapped)  # componenttemplate0

        # Initial IDs
        root_id = root.id
        wrapped_id = wrapped.id
        child_id = child.id

        assert wrapped_id == f"{root_id}-button0"
        assert child_id == f"{root_id}-button0-lazycomponent1"

        # Attach root to a parent
        parent = LazyComponent()  # componenttemplate2
        root.parent = parent

        # All descendants should update
        assert wrapped.id == f"{root.id}-button0"
        assert child.id == f"{root.id}-button0-lazycomponent1"


class TestWrappedComponentUseCase:
    """Test real-world use cases for WrappedComponent."""

    def test_organize_legacy_components(self):
        """Organize existing components into tree structure."""
        # Existing components
        header = html.Header(id="app-header")
        sidebar = html.Div(id="sidebar")
        content = html.Div(id="main-content")

        # Wrap into tree structure
        root = LazyComponent()
        wrapped_header = WrappedComponent(header, _parent=root)
        wrapped_sidebar = WrappedComponent(sidebar, _parent=root)
        wrapped_content = WrappedComponent(content, _parent=root)

        # Tree structure for organization
        assert wrapped_header.parent == root
        assert wrapped_sidebar.parent == root
        assert wrapped_content.parent == root

        # Original components unchanged
        assert getattr(header, "id", None) == "app-header"
        assert getattr(sidebar, "id", None) == "sidebar"
        assert getattr(content, "id", None) == "main-content"

    def test_mixed_wrapped_and_template(self):
        """Mix WrappedComponent with template-generated components."""
        # Template root
        root = LazyComponent()  # componenttemplate0

        # Some components are wrapped (external)
        legacy_button = html.Button("Old Button", id="legacy-btn")
        wrapped = WrappedComponent(legacy_button, _parent=root)  # button0

        # Others are template-generated
        template_child = LazyComponent(_parent=root)  # componenttemplate0

        # Both coexist in tree
        assert wrapped.parent == root
        assert template_child.parent == root
        assert wrapped.id == f"{root.id}-button0"
        assert template_child.id == f"{root.id}-lazycomponent1"


class TestWrappedComponentRepr:
    """Test string representation of WrappedComponent."""

    def test_repr_without_name(self):
        """__repr__ should show tree_id and component repr."""
        button = html.Button("Click", id="my-id")
        wrapped = WrappedComponent(button)
        repr_str = repr(wrapped)

        assert repr_str.startswith("Wrapped(id='button0', ")
        assert "Button" in repr_str
        assert repr_str.endswith(")")


class TestWrappedComponentEdgeCases:
    """Test edge cases and error conditions."""

    def test_wrap_component_without_explicit_id(self):
        """Wrap component without explicitly setting id."""
        div = html.Div()  # No id parameter
        wrapped = WrappedComponent(div)

        # Should have auto-generated tree ID using component class name
        assert wrapped.id == "div0"

    def test_wrap_component_empty_string_id(self):
        """Wrap component with empty string ID."""
        div = html.Div(id="")
        wrapped = WrappedComponent(div)

        # Empty string doesn't affect tree ID (uses component class name)
        assert wrapped.id == "div0"
