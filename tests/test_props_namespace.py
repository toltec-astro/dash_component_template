"""Tests for PropsNamespace functionality.

Tests the props namespace, including:
- Dict-style access for wildcard properties (data-*, aria-*)
- Attribute-style access for standard properties
- Dict protocol methods (keys, items, values, etc.)
- update() method for batch updates
"""

from dash import html

from dash_component_template.lazy_component import (
    LazyComponent,
    _make_lazy_component_cls,
)


class TestPropsNamespaceBasics:
    """Basic props namespace functionality."""

    def test_attribute_style_access(self):
        """Should access props via attribute style."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate(className="test")

        assert template.props.className == "test"

        template.props.className = "updated"
        assert template.props.className == "updated"

    def test_dict_style_access(self):
        """Should access props via dict style."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate()

        template.props["className"] = "test"
        assert template.props["className"] == "test"

        assert template.props.className == "test"  # Also accessible via attribute


class TestWildcardProperties:
    """Tests for wildcard properties (data-*, aria-*)."""

    def test_data_attribute(self):
        """Should support data-* attributes via dict access."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate()

        # Set data-testid (wildcard property)
        template.props["data-testid"] = "my-component"

        assert template.props["data-testid"] == "my-component"

    def test_aria_attribute(self):
        """Should support aria-* attributes via dict access."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate()

        # Set aria-label (wildcard property)
        template.props["aria-label"] = "Navigation menu"

        assert template.props["aria-label"] == "Navigation menu"

    def test_multiple_wildcards(self):
        """Should support multiple wildcard properties."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate()

        template.props["data-testid"] = "test-component"
        template.props["data-cy"] = "cypress-test"
        template.props["aria-label"] = "Test label"
        template.props["aria-hidden"] = "true"

        assert template.props["data-testid"] == "test-component"
        assert template.props["data-cy"] == "cypress-test"
        assert template.props["aria-label"] == "Test label"
        assert template.props["aria-hidden"] == "true"

    def test_wildcards_in_materialized_component(self):
        """Wildcard properties should appear in materialized component."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate(className="container")

        template.props["data-testid"] = "main-container"
        template.props["aria-label"] = "Main container"

        result = template.materialize()

        assert isinstance(result, list) and len(result) == 1

        component = result[0]

        # Check that wildcard props made it to the component
        # Note: Dash components expose these via their data attribute
        assert hasattr(
            component, "data-testid"
        ) or "data-testid" in component.__dict__.get("_prop_names", [])
        assert hasattr(
            component, "aria-label"
        ) or "aria-label" in component.__dict__.get("_prop_names", [])


class TestDictProtocol:
    """Tests for dict protocol methods on PropsNamespace."""

    def test_contains(self):
        """Should support 'in' operator."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate(className="test")

        assert "className" in template.props
        assert "style" not in template.props

    def test_keys(self):
        """Should return all prop keys via template.props_dict()."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate(className="test", style={"color": "red"})

        keys = list(template.props_dict().keys())
        assert "className" in keys
        assert "style" in keys

    def test_items(self):
        """Should return all prop items via template.props_dict()."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate(className="test", style={"color": "red"})

        items = template.props_dict()
        assert items["className"] == "test"
        assert items["style"] == {"color": "red"}

    def test_values(self):
        """Should return all prop values via template.props_dict()."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate(className="test", id="my-div")

        values = list(template.props_dict().values())
        assert "test" in values
        assert "my-div" in values

    def test_len(self):
        """Should return number of props."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate(className="test", style={"color": "red"})

        assert len(template.props) == 2

    def test_iter(self):
        """Should iterate over prop keys."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate(className="test", style={"color": "red"})

        keys = list(template.props)
        assert "className" in keys
        assert "style" in keys


class TestPropsUpdate:
    """Tests for template.props_update() method."""

    def test_update_with_dict(self):
        """Should update multiple props from dict."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate()

        template.props_update(
            {"className": "container", "style": {"padding": "10px"}, "id": "main"}
        )

        assert template.props.className == "container"
        assert template.props.style == {"padding": "10px"}
        assert template.props["id"] == "main"

    def test_update_with_wildcards(self):
        """Should update wildcard properties via props_update()."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate()

        template.props_update(
            {
                "className": "test",
                "data-testid": "my-component",
                "aria-label": "Test component",
            }
        )

        assert template.props.className == "test"
        assert template.props["data-testid"] == "my-component"
        assert template.props["aria-label"] == "Test component"

    def test_update_overwrites_existing(self):
        """Should overwrite existing props."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate(className="initial")

        template.props_update({"className": "updated"})

        assert template.props.className == "updated"


class TestPropsClear:
    """Tests for clearing props via direct dict access."""

    def test_clear_all_props(self):
        """Should clear all props by clearing internal dict."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate(className="test", style={"color": "red"})

        template.props._data.clear()

        assert len(template.props) == 0
        assert "className" not in template.props


class TestPropsToDict:
    """Tests for template.props_dict() method."""

    def test_to_dict_returns_all_props(self):
        """Should return all props as dict."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate(className="test", style={"color": "red"})

        props_dict = template.props_dict()

        assert props_dict["className"] == "test"
        assert props_dict["style"] == {"color": "red"}

    def test_to_dict_includes_wildcards(self):
        """Should include wildcard properties in props_dict()."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate(className="test")
        template.props["data-testid"] = "my-component"

        props_dict = template.props_dict()

        assert props_dict["className"] == "test"
        assert props_dict["data-testid"] == "my-component"


class TestPropsWithTypedChildren:
    """Test props namespace with typed child templates."""

    def test_child_has_props_namespace(self):
        """Child templates should have props namespace."""
        parent = LazyComponent()
        child = parent.child[html.Div](className="child-class")

        assert hasattr(child, "props")
        assert child.props.className == "child-class"

    def test_modify_child_props(self):
        """Should be able to modify child props."""
        parent = LazyComponent()
        child = parent.child[html.Div](className="initial")

        child.props.className = "modified"
        child.props["data-testid"] = "child-test"

        assert child.props.className == "modified"
        assert child.props["data-testid"] == "child-test"


class TestPropsIndependence:
    """Test that props are independent between instances."""

    def test_different_instances_independent(self):
        """Different instances should have independent props."""
        DivTemplate = _make_lazy_component_cls(html.Div)

        template1 = DivTemplate(className="class1")
        template2 = DivTemplate(className="class2")

        assert template1.props.className == "class1"
        assert template2.props.className == "class2"

        template1.props.className = "modified1"
        assert template1.props.className == "modified1"
        assert template2.props.className == "class2"  # Unchanged
