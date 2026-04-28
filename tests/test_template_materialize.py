"""Test Template.materialize() behavior with mixed children."""

import pytest
from dash import html

from dash_component_template.lazy_component import _make_lazy_component_cls
from dash_component_template.template import Template


class TestTemplateMaterialize:
    """Test Template.materialize() returns consistent list[Component]."""

    def test_materialize_no_children_returns_empty_list(self):
        """Template with no children returns empty list."""
        t = Template()
        result = t.materialize()
        assert isinstance(result, list)
        assert len(result) == 0

    def test_materialize_one_child_returns_list_with_one_component(self):
        """Template with one child returns list with single component."""
        DivTemplate = _make_lazy_component_cls(html.Div)

        t = Template()
        child = DivTemplate(children="Hello", _parent=t)

        result = t.materialize()
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], html.Div)
        assert result[0].children == ["Hello"]  # Dash wraps in list

    def test_materialize_multiple_children_returns_flat_list(self):
        """Template with multiple children returns flat list of components."""
        DivTemplate = _make_lazy_component_cls(html.Div)

        t = Template()
        c1 = DivTemplate(children="Child 1", _parent=t)
        c2 = DivTemplate(children="Child 2", _parent=t)

        result = t.materialize()
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(c, html.Div) for c in result)
        assert result[0].children == ["Child 1"]  # Dash wraps in list
        assert result[1].children == ["Child 2"]  # Dash wraps in list

    def test_materialize_mixed_children_no_nested_lists(self):
        """Template with mixed Template and ComponentTemplate children
        returns flat list.

        This is the critical test for the fix: when mixing Template and
        ComponentTemplate
        as siblings, we should get a flat list, not nested lists.

        Tree structure:
            t0 - c1 (Div)
             |
              - t2 - c3 (Div)

        Expected result: [Div, Div] (flat list)
        NOT: [Div, [Div]] (nested list)
        """
        DivTemplate = _make_lazy_component_cls(html.Div)

        # Create tree structure
        t0 = Template()
        c1 = DivTemplate(children="C1", _parent=t0)
        t2 = Template(_parent=t0)
        c3 = DivTemplate(children="C3", _parent=t2)

        # Verify tree structure
        assert len(t0.children) == 2
        assert t0.children[0] is c1
        assert t0.children[1] is t2
        assert len(t2.children) == 1
        assert t2.children[0] is c3

        # Materialize
        result = t0.materialize()

        # Critical assertions
        assert isinstance(result, list), "Result should be a list"
        assert len(result) == 2, "Should have exactly 2 components (flattened)"

        # Check no nested lists
        for i, item in enumerate(result):
            assert not isinstance(item, list), (
                f"Item {i} should not be a list (no nesting)"
            )
            assert isinstance(item, html.Div), f"Item {i} should be a Div component"

        # Verify content
        # Note: t2 has sibling c1, so NO automatic wrapper
        # t2 materializes to [c3], which gets extended into result
        # Result: [c1, c3] (flat list, both Divs at same level)
        assert result[0].children == ["C1"]  # c1 directly
        assert result[1].children == ["C3"]  # c3 directly (no wrapper)

    def test_materialize_deeply_nested_templates_flattens_correctly(self):
        """Deeply nested Template nodes properly flatten to single list."""
        DivTemplate = _make_lazy_component_cls(html.Div)

        # Create deeply nested structure:
        # t0 - t1 - t2 - c1
        #   |
        #    - c2
        t0 = Template()
        t1 = Template(_parent=t0)
        t2 = Template(_parent=t1)
        c1 = DivTemplate(children="C1", _parent=t2)
        c2 = DivTemplate(children="C2", _parent=t0)

        result = t0.materialize()

        # t1 and t2 are virtual templates with sibling c2
        # t1 has sole child t2, so gets squeezed: t0 -> [t1, t2 -> c1, c2]
        # After squeeze, t2 has siblings, but NO automatic wrapper
        # t2 materializes to [c1], which gets extended into result
        # Result: [c1, c2] (flat list)
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(c, html.Div) for c in result)
        # No wrapper - both components at same level
        assert result[0].children == ["C1"]  # c1 directly
        assert result[1].children == ["C2"]  # c2 directly

    def test_materialize_preserves_component_hierarchy(self):
        """ComponentTemplate's own children are preserved in component.children."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        ButtonTemplate = _make_lazy_component_cls(html.Button)

        # Create structure where ComponentTemplate has ComponentTemplate child
        # t0 - div1 - button1
        #   |
        #    - div2
        t0 = Template()
        div1 = DivTemplate(_parent=t0)
        button1 = ButtonTemplate(children="Click me", _parent=div1)
        div2 = DivTemplate(children="Sibling", _parent=t0)

        result = t0.materialize()

        # t0.materialize() returns [div1_component, div2_component]
        assert len(result) == 2

        # div1 should have button1 as its child
        div1_component = result[0]
        assert isinstance(div1_component, html.Div)
        assert len(div1_component.children) == 1
        assert isinstance(div1_component.children[0], html.Button)
        assert div1_component.children[0].children == ["Click me"]  # Dash wraps

        # div2 should have its children
        div2_component = result[1]
        assert isinstance(div2_component, html.Div)
        assert div2_component.children == ["Sibling"]  # Dash wraps


class TestTemplateLayout:
    """Test Template.layout() convenience method."""

    def test_layout_calls_materialize(self):
        """layout() calls materialize() and returns single component."""
        DivTemplate = _make_lazy_component_cls(html.Div)

        class MyTemplate(Template):
            def __init__(self):
                super().__init__()
                self.div = DivTemplate(children="Setup!", _parent=self)

        t = MyTemplate()
        result = t.layout()

        # layout() returns single Component (unwrapped from list)
        assert isinstance(result, html.Div)
        assert result.children == ["Setup!"]  # Dash wraps

    def test_layout_raises_error_on_multiple_components(self):
        """layout() raises ValueError when materialize returns multiple components."""
        DivTemplate = _make_lazy_component_cls(html.Div)

        class MyTemplate(Template):
            def __init__(self):
                super().__init__()
                self.div1 = DivTemplate(children="First", _parent=self)
                self.div2 = DivTemplate(children="Second", _parent=self)

        t = MyTemplate()

        with pytest.raises(ValueError, match="returned 2 components"):
            t.layout()

    def test_layout_raises_error_on_empty_list(self):
        """layout() raises ValueError when materialize returns empty list."""

        class EmptyTemplate(Template):
            def materialize(self):
                return []

        t = EmptyTemplate()

        with pytest.raises(ValueError, match="returned empty list"):
            t.layout()
