"""Tests for flexible .child interface supporting three usage patterns."""

from dash import html

from dash_component_template import Template
from dash_component_template.wrapped_component import WrappedComponent


class TestFactoryPattern:
    """Test the original factory pattern: template.child[Type](...)"""

    def test_factory_creates_typed_template(self):
        """Factory pattern creates typed component template."""
        root = Template()
        div = root.child[html.Div](className="container")

        assert div.parent is root
        assert div in root.children
        assert hasattr(div, "props")
        assert div.props.className == "container"

    def test_factory_with_nested_children(self):
        """Factory pattern works for nested hierarchy."""
        root = Template()
        parent_div = root.child[html.Div]()
        child_div = parent_div.child[html.Div](children="Hello")

        assert parent_div.parent is root
        assert child_div.parent is parent_div
        assert child_div in parent_div.children


class TestWrapComponentPattern:
    """Test wrapping existing Dash component instances: template.child(component)"""

    def test_wrap_simple_component(self):
        """Can wrap a Dash component instance."""
        root = Template()
        component = html.Div("Hello", className="box")
        wrapped = root.child(component)

        assert isinstance(wrapped, WrappedComponent)
        assert wrapped.parent is root
        assert wrapped in root.children

    def test_wrap_component_with_complex_props(self):
        """Can wrap component with multiple props."""
        root = Template()
        component = html.Button(
            "Click me",
            id="my-button",
            className="btn btn-primary",
            style={"color": "red"},
        )
        wrapped = root.child(component)

        assert isinstance(wrapped, WrappedComponent)
        assert wrapped.parent is root

        # Materialize to verify component is preserved
        result = wrapped.materialize()
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0] is component

    def test_wrap_multiple_components(self):
        """Can wrap multiple components as siblings."""
        root = Template()
        comp1 = html.Div("First")
        comp2 = html.Div("Second")

        wrapped1 = root.child(comp1)
        wrapped2 = root.child(comp2)

        assert wrapped1 in root.children
        assert wrapped2 in root.children
        assert len(root.children) == 2

    def test_wrap_nested_component_structure(self):
        """Can create nested structure with wrapped components."""
        root = Template()

        # Create nested structure
        parent_comp = html.Div(className="parent")
        parent_wrapped = root.child(parent_comp)

        child_comp = html.Span("Child")
        child_wrapped = parent_wrapped.child(child_comp)

        assert parent_wrapped.parent is root
        assert child_wrapped.parent is parent_wrapped


class TestAddTemplatePattern:
    """Test adding existing template instances: template.child(template)"""

    def test_add_existing_template(self):
        """Can add existing template as child."""
        root = Template()
        header = Template()

        added = root.child(header)

        assert added is header
        assert header.parent is root
        assert header in root.children

    def test_add_template_reparents_it(self):
        """Adding template to new parent reparents it."""
        parent1 = Template()
        parent2 = Template()
        child = Template()

        # Initially add to parent1
        parent1.child(child)
        assert child.parent is parent1

        # Move to parent2
        parent2.child(child)
        assert child.parent is parent2
        assert child in parent2.children

    def test_add_custom_template_subclass(self):
        """Can add custom Template subclass."""

        class HeaderTemplate(Template):
            def __init__(self):
                super().__init__()
                self.title = self.child[html.H1](children="Title")

        root = Template()
        header = HeaderTemplate()

        added = root.child(header)

        assert added is header
        assert header.parent is root
        assert isinstance(header, HeaderTemplate)

    def test_add_template_with_children(self):
        """Can add template that already has children."""
        root = Template()

        # Create header with children
        header = Template()
        header.child[html.H1](children="Title")
        header.child[html.H2](children="Subtitle")

        # Add header to root
        root.child(header)

        assert header.parent is root
        assert len(header.children) == 2


class TestMixedPatterns:
    """Test mixing all three patterns together."""

    def test_factory_and_wrap_mixed(self):
        """Can mix factory pattern and component wrapping."""
        root = Template()

        # Factory pattern
        div1 = root.child[html.Div](className="factory")

        # Wrap pattern
        comp = html.Div("wrapped")
        div2 = root.child(comp)

        assert len(root.children) == 2
        assert div1 in root.children
        assert div2 in root.children

    def test_all_three_patterns_mixed(self):
        """Can use all three patterns in same hierarchy."""
        root = Template()

        # Pattern 1: Factory
        header = root.child[html.Header]()

        # Pattern 2: Wrap component
        nav_comp = html.Nav("Navigation")
        nav = root.child(nav_comp)

        # Pattern 3: Add template
        footer = Template()
        footer.child[html.Footer](children="Footer text")
        root.child(footer)

        assert len(root.children) == 3
        assert header.parent is root
        assert nav.parent is root
        assert footer.parent is root

    def test_nested_mixed_patterns(self):
        """Can nest different patterns within each other."""
        root = Template()

        # Factory creates container
        container = root.child[html.Div](className="container")

        # Add custom template to container
        sidebar = Template()
        sidebar.child[html.Aside](children="Sidebar")
        container.child(sidebar)

        # Wrap component in container
        main_comp = html.Main("Main content")
        container.child(main_comp)

        assert len(container.children) == 2


class TestMaterializationWithMixedPatterns:
    """Test that materialization works correctly with all patterns."""

    def test_materialize_factory_children(self):
        """Factory children materialize correctly."""
        root = Template()
        div = root.child[html.Div](children="Content")

        components = root.materialize()
        assert len(components) == 1
        assert isinstance(components[0], html.Div)

    def test_materialize_wrapped_children(self):
        """Wrapped components materialize correctly."""
        root = Template()
        comp = html.Div("Wrapped")
        root.child(comp)

        components = root.materialize()
        assert len(components) == 1
        assert components[0] is comp

    def test_materialize_template_children(self):
        """Template children materialize correctly."""
        root = Template()
        child_template = Template()
        child_template.child[html.Div](children="Child")
        root.child(child_template)

        components = root.materialize()
        assert len(components) == 1
        assert isinstance(components[0], html.Div)

    def test_materialize_mixed_children(self):
        """Mixed children materialize correctly."""
        root = Template()

        # Factory
        root.child[html.Div](children="Factory")

        # Wrapped
        root.child(html.Div("Wrapped"))

        # Template
        template = Template()
        template.child[html.Div](children="Template")
        root.child(template)

        components = root.materialize()
        assert len(components) == 3
        assert all(isinstance(c, html.Div) for c in components)


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_add_template_to_none_owner(self):
        """Can add template when owner is None (root level)."""
        from dash_component_template.lazy_component import _LazyComponentFactory

        factory = _LazyComponentFactory(owner=None)
        template = Template()

        result = factory(template)

        assert result is template
        assert template.parent is None

    def test_wrap_component_with_none_owner(self):
        """Can wrap component when owner is None."""
        from dash_component_template.lazy_component import _LazyComponentFactory

        factory = _LazyComponentFactory(owner=None)
        comp = html.Div("Content")

        wrapped = factory(comp)

        assert isinstance(wrapped, WrappedComponent)
        assert wrapped.parent is None
