"""Integration tests for typed .child[] method with property descriptors."""

import pytest
from dash import dcc, html
from dash_mantine_components import Button

from dash_component_template import Template
from dash_component_template.lazy_component import (
    LazyComponent,
    _make_lazy_component_cls,
)


class TestTypedChildBasics:
    """Tests for basic typed child functionality."""

    def test_child_returns_component_template_subclass(self):
        """Should return typed ComponentTemplate subclass instance."""
        parent = Template()
        child = parent.child[html.Div](className="test")

        assert isinstance(child, LazyComponent)
        assert child._component_cls is html.Div

    def test_child_is_added_to_tree(self):
        """Child should be added to parent's tree."""
        parent = Template()
        child = parent.child[html.Div](className="test")

        assert child.parent is parent
        assert child in parent.children

    def test_child_has_hierarchical_id(self):
        """Child should have hierarchical ID based on parent."""
        parent = Template()
        child = parent.child[html.Div](className="test")

        assert child.id.startswith(parent.id)
        assert "-" in child.id


class TestPropertyDescriptors:
    """Tests for property descriptors on typed children."""

    def test_can_set_property_via_descriptor(self):
        """Should set property via props namespace."""
        parent = Template()
        child = parent.child[html.Div](className="initial")

        # Should be able to access property via props
        assert child.props.className == "initial"

        # Should be able to modify property via props
        child.props.className = "modified"
        assert child.props.className == "modified"

    def test_can_set_multiple_properties(self):
        """Should set multiple properties via props namespace."""
        parent = Template()
        child = parent.child[html.Div](className="test", style={"color": "red"})

        assert child.props.className == "test"
        assert child.props.style == {"color": "red"}

    def test_property_modification_before_materialize(self):
        """Should be able to modify properties before materialization."""
        parent = Template()

        child = parent.child[html.Button](children="Click", className="btn")

        # Modify property before materialization via props
        child.props.className = "btn-primary"
        child.props.children = "Click Me!"

        # Materialize the child directly
        result = child.materialize()

        assert isinstance(result, list) and len(result) == 1

        component = result[0]

        # Check materialized component has updated props
        assert component.className == "btn-primary"
        # Dash wraps single children in a list
        assert component.children == ["Click Me!"]

    def test_unset_property_returns_none(self):
        """Unset property should raise AttributeError via props namespace."""
        parent = Template()
        child = parent.child[html.Div]()

        # className not set, should raise AttributeError
        with pytest.raises(
            AttributeError, match="Property 'className' has not been set"
        ):
            _ = child.props.className


class TestPropertyDescriptorIndependence:
    """Tests for property descriptor independence across instances."""

    def test_different_instances_have_independent_properties(self):
        """Different instances should have independent property values."""
        parent = Template()

        child1 = parent.child[html.Div](className="child1")
        child2 = parent.child[html.Div](className="child2")

        assert child1.props.className == "child1"
        assert child2.props.className == "child2"

        # Modify one shouldn't affect the other
        child1.props.className = "modified1"
        assert child1.props.className == "modified1"
        assert child2.props.className == "child2"


class TestChaining:
    """Tests for chaining typed children."""

    def test_can_chain_multiple_levels(self):
        """Should be able to chain child creation."""
        root = Template()

        level1 = root.child[html.Div](className="level1")
        level2 = level1.child[html.Div](className="level2")
        level3 = level2.child[html.Button](children="Deep", className="level3")

        # Check hierarchy
        assert level1.parent is root
        assert level2.parent is level1
        assert level3.parent is level2

        # Check IDs reflect hierarchy
        assert level1.id.startswith(root.id)
        assert level2.id.startswith(level1.id)
        assert level3.id.startswith(level2.id)

    def test_chained_children_materialize_correctly(self):
        """Chained children should materialize correctly."""
        root = Template()

        level1 = root.child[html.Div](className="level1")
        level2 = level1.child[html.Button](children="Click", className="level2")

        # Materialize root - returns level1 Div directly since Template has no component_cls  # noqa: E501
        result = root.materialize()

        assert isinstance(result, list) and len(result) == 1

        level1_comp = result[0]

        # Check structure
        assert level1_comp.className == "level1"
        assert len(level1_comp.children) == 1

        level2_comp = level1_comp.children[0]
        # Dash wraps single children in list
        assert level2_comp.children == ["Click"]
        assert level2_comp.className == "level2"


class TestMixedComponentTypes:
    """Tests for using different component types."""

    def test_works_with_html_components(self):
        """Should work with html.* components."""
        parent = Template()

        div = parent.child[html.Div](className="div")
        button = parent.child[html.Button](children="Click")
        span = parent.child[html.Span](children="Text")

        result = parent.materialize()

        # Template returns its 3 children directly
        assert isinstance(result, list) and len(result) == 3

        assert result[0].className == "div"
        # Dash wraps single children in list
        assert result[1].children == ["Click"]
        assert result[2].children == ["Text"]

    def test_works_with_dcc_components(self):
        """Should work with dcc.* components."""
        parent = Template()

        # Note: dcc.Graph doesn't accept 'children' prop
        # Must not pass children=None to Graph
        graph = parent.child[dcc.Graph](figure={})

        assert graph._component_cls is dcc.Graph

        result = parent.materialize()

        # Template returns the Graph component directly
        assert isinstance(result, list) and len(result) == 1

        component = result[0]
        # Graph component gets an id from tree_id
        assert component.id is not None
        assert isinstance(component, dcc.Graph)

    def test_works_with_dmc_components(self):
        """Should work with dmc.* components."""
        parent = Template()

        button = parent.child[Button](children="DMC Button", color="blue")

        assert button._component_cls is Button

        result = parent.materialize()

        assert isinstance(result, list) and len(result) == 1

        component = result[0]
        assert len(component.children) == 1


class TestDynamicClassCaching:
    """Tests for dynamic class generation and caching."""

    def test_same_component_type_reuses_class(self):
        """Should reuse same typed class for same component type."""
        parent = Template()

        child1 = parent.child[html.Div](className="child1")
        child2 = parent.child[html.Div](className="child2")

        # Should be instances of same class
        assert type(child1) is type(child2)
        assert type(child1).__name__ == "LazyComponentHtmlDiv"

    def test_different_component_types_get_different_classes(self):
        """Should create different classes for different component types."""
        parent = Template()

        div = parent.child[html.Div]()
        button = parent.child[html.Button]()

        # Should be different classes
        assert type(div) is not type(button)
        assert type(div).__name__ == "LazyComponentHtmlDiv"
        assert type(button).__name__ == "LazyComponentHtmlButton"


class TestIntegrationWithExistingFeatures:
    """Tests for integration with existing ComponentTemplate features."""

    def test_works_with_custom_subclass(self):
        """Should work with custom ComponentTemplate subclass."""

        class MyTemplate(LazyComponent):
            _component_cls = html.Div

            def __init__(self):
                super().__init__()
                self.header = self.child[html.H1](children="Title")
                self.content = self.child[html.P](children="Content")

        template = MyTemplate()

        # Check children created
        assert len(template.children) == 2
        assert template.header._component_cls is html.H1
        assert template.content._component_cls is html.P

        # Modify properties before materialization via props
        template.header.props.children = "New Title"
        template.content.props.children = "New Content"

        # Materialize
        result = template.materialize()

        assert isinstance(result, list) and len(result) == 1

        component = result[0]

        # Check materialized
        assert len(component.children) == 2
        # Dash wraps single children in list
        assert component.children[0].children == ["New Title"]
        assert component.children[1].children == ["New Content"]


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_child_without_props(self):
        """Should work with no props provided."""
        parent = Template()
        child = parent.child[html.Div]()

        assert isinstance(child, LazyComponent)
        assert child._component_cls is html.Div

    def test_multiple_parents_create_multiple_children(self):
        """Different parents should create independent children."""
        parent1 = LazyComponent()
        parent2 = LazyComponent()

        child1 = parent1.child[html.Div](className="child1")
        child2 = parent2.child[html.Div](className="child2")

        assert child1.parent is parent1
        assert child2.parent is parent2
        assert child1 is not child2


# Fixture to auto-clear lru_cache between tests
@pytest.fixture(autouse=True)
def auto_clear_cache():
    """Automatically clear lru_cache before each test."""
    _make_lazy_component_cls.cache_clear()
    yield
    _make_lazy_component_cls.cache_clear()
