"""Tests for pattern-matching ID scope injection.

These tests verify that dict IDs get properly injected with _template_name
and _template_id for proper callback scoping.
"""

import pytest
from dash import MATCH, html

from dash_component_template import Template
from dash_component_template.lazy_component import _make_lazy_component_cls


class TestPatternMatchingScope:
    """Test scope injection for pattern-matching callbacks."""

    def test_dict_id_gets_scope_injected_during_materialization(self):
        """Dict IDs should have _template_name and _template_id injected."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate(id={"type": "btn", "index": 0})

        components = template.materialize()
        component = components[0]

        # Should have original keys plus scope keys
        assert component.id["type"] == "btn"
        assert component.id["index"] == 0
        assert component.id["_template_name"] == "LazyComponentHtmlDiv"
        assert component.id["_template_id"] == template.id

    def test_string_id_not_modified_during_materialization(self):
        """String IDs should remain unchanged (no scope injection)."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate()  # Default string ID

        components = template.materialize()
        component = components[0]

        # Should be a plain string
        assert isinstance(component.id, str)
        assert component.id == template.id

    def test_call_with_overrides_merges_correctly(self):
        """__call__() should merge user overrides with base ID and scope."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate(id={"type": "btn", "index": 0})
        template.materialize()

        # Call with overrides
        result = template({"index": MATCH})

        # Should have merged dict
        assert isinstance(result, dict)
        assert result["type"] == "btn"
        assert result["index"] == MATCH
        assert result["_template_name"] == "LazyComponentHtmlDiv"
        assert result["_template_id"] == template.id

    def test_call_without_overrides_returns_component(self):
        """__call__() without overrides should return the component directly."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate(id={"type": "btn", "index": 0})
        template.materialize()

        # Call without overrides
        result = template()

        # Should return the component itself
        assert result is template.materialized

    def test_call_with_string_id_raises_error(self):
        """__call__() with overrides on string ID should raise clear error."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate()  # Default string ID
        template.materialize()

        # Should raise ValueError with helpful message
        with pytest.raises(
            ValueError, match="Cannot use pattern matching with string ID"
        ):
            template({"index": MATCH})

    def test_nested_templates_get_unique_scope(self):
        """All components within the same Template share the same _template_id.

        The _template_id is set to the nearest Template ancestor's ID, not the
        individual component's tree ID. This ensures pattern-matching callbacks
        correctly isolate one Template instance from another while matching
        multiple components within the same instance.
        """
        root = Template()
        div = root.child[html.Div](id={"type": "container", "level": 0})
        child = div.child[html.Button](id={"type": "btn", "level": 1})

        root.materialize()

        # Both div and child are owned by root (the nearest Template ancestor)
        div_component = div.materialized
        child_component = child.materialized

        assert div_component.id["_template_id"] == root.id
        assert child_component.id["_template_id"] == root.id
        # All components within the same Template share the same _template_id
        assert div_component.id["_template_id"] == child_component.id["_template_id"]

    def test_multiple_instances_have_unique_template_ids(self):
        """Multiple instances should have unique _template_id values."""
        DivTemplate = _make_lazy_component_cls(html.Div)

        t1 = DivTemplate(id={"type": "btn", "index": 0})
        t2 = DivTemplate(id={"type": "btn", "index": 0})

        t1.materialize()
        t2.materialize()

        # Same template class name
        assert (
            t1.materialized.id["_template_name"] == t2.materialized.id["_template_name"]
        )

        # Different template IDs
        assert t1.materialized.id["_template_id"] != t2.materialized.id["_template_id"]
        assert t1.materialized.id["_template_id"] == t1.id
        assert t2.materialized.id["_template_id"] == t2.id

    def test_scope_preserves_all_user_keys(self):
        """Scope injection should not overwrite any user keys."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate(
            id={
                "type": "btn",
                "index": 0,
                "custom_key": "custom_value",
                "another_key": 42,
            }
        )

        components = template.materialize()
        component = components[0]

        # All user keys preserved
        assert component.id["type"] == "btn"
        assert component.id["index"] == 0
        assert component.id["custom_key"] == "custom_value"
        assert component.id["another_key"] == 42

        # Plus scope keys added
        assert "_template_name" in component.id
        assert "_template_id" in component.id


class TestCallOperatorErrorMessages:
    """Test that __call__() provides helpful error messages."""

    def test_error_message_shows_component_type(self):
        """Error message should show the component type being used."""
        ButtonTemplate = _make_lazy_component_cls(html.Button)
        template = ButtonTemplate()
        template.materialize()

        with pytest.raises(ValueError) as exc_info:
            template({"index": MATCH})

        # Should mention Button in the error
        assert "Button" in str(exc_info.value)

    def test_error_message_shows_example_dict_id(self):
        """Error message should show how to create dict ID."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate()
        template.materialize()

        with pytest.raises(ValueError) as exc_info:
            template({"index": MATCH})

        # Should show dict ID example
        assert "id={'type':" in str(exc_info.value)
        assert "'index':" in str(exc_info.value)
