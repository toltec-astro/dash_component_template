"""Test that None is handled correctly as a valid prop value.

The _PropsNamespace should distinguish between "key not set" and "key set to None".
This is important because some Dash components may legitimately use None as a value.
"""

import pytest
from dash import html

from dash_component_template.lazy_component import _make_lazy_component_cls


def test_none_is_valid_prop_value():
    """Test that None can be explicitly set as a prop value."""
    DivTemplate = _make_lazy_component_cls(html.Div)
    template = DivTemplate(className=None)

    # Check that className is in props (explicitly set)
    assert "className" in template._props
    # And that its value is None
    assert template._props["className"] is None

    # Materialize and check the component
    components = template.materialize()
    component = components[0]

    # The materialized component should have className=None
    assert component.className is None


def test_unset_prop_not_in_namespace():
    """Test that unset props are not in the namespace."""
    DivTemplate = _make_lazy_component_cls(html.Div)
    template = DivTemplate(id="my-div")

    # Check that className is NOT in props (not set)
    assert "className" not in template._props
    # Accessing it raises KeyError
    with pytest.raises(KeyError, match="Property 'className' has not been set"):
        _ = template._props["className"]


def test_id_prop_cannot_be_none():
    """Test that id cannot be set to None - raises TypeError.

    IDs must be strings or dicts. None is not a valid component ID.
    """
    DivTemplate = _make_lazy_component_cls(html.Div)
    template = DivTemplate(id=None)

    # Check that id is in props
    assert "id" in template._props
    # And that its value is None
    assert template._props["id"] is None

    # The _make_component_id should raise TypeError for None
    with pytest.raises(
        TypeError, match="Component ID must be a string or dict, got NoneType"
    ):
        template._make_component_id()


def test_invalid_id_types_raise_error():
    """Test that invalid ID types (int, float, bool, etc.) raise TypeError."""
    DivTemplate = _make_lazy_component_cls(html.Div)

    # Test int ID
    template_int = DivTemplate(id=123)
    with pytest.raises(
        TypeError, match="Component ID must be a string or dict, got int"
    ):
        template_int._make_component_id()

    # Test float ID
    template_float = DivTemplate(id=45.6)
    with pytest.raises(
        TypeError, match="Component ID must be a string or dict, got float"
    ):
        template_float._make_component_id()

    # Test bool ID
    template_bool = DivTemplate(id=True)
    with pytest.raises(
        TypeError, match="Component ID must be a string or dict, got bool"
    ):
        template_bool._make_component_id()

    # Test list ID
    template_list = DivTemplate(id=["a", "b"])
    with pytest.raises(
        TypeError, match="Component ID must be a string or dict, got list"
    ):
        template_list._make_component_id()


def test_id_prop_unset_uses_default():
    """Test that when id is not set, the default template.id is used."""
    DivTemplate = _make_lazy_component_cls(html.Div)
    template = DivTemplate()

    # Check that id is NOT in props
    assert "id" not in template._props

    # The _make_component_id should fall back to template.id
    component_id = template._make_component_id()
    assert isinstance(component_id, str)
    assert component_id == template.id


def test_none_value_in_dict_id():
    """Test that dict IDs can have None values in props (Dash rejects on materialize).

    While we allow None in the props namespace, Dash itself requires dict ID values
    to be strings, numbers, or bools. This test verifies that None is preserved
    through _make_component_id but will be rejected by Dash at materialize time.
    """
    ButtonTemplate = _make_lazy_component_cls(html.Button)
    template = ButtonTemplate(id={"type": "my-button", "index": None})

    # The id should be preserved with None value in props
    assert "id" in template._props
    base_id = template._props["id"]
    assert isinstance(base_id, dict)
    assert base_id["index"] is None

    # Our _make_component_id should preserve None values
    # (even though Dash will reject them at materialize time)
    component_id = template._make_component_id()

    # Should have None preserved
    assert isinstance(component_id, dict)
    assert component_id["index"] is None
    # But should have scope injected
    assert "_template_name" in component_id
    assert "_template_id" in component_id

    # Dash will reject None values in dict IDs at materialize time
    with pytest.raises(
        TypeError, match="dict id values must be strings, numbers or bools"
    ):
        template.materialize()


def test_props_namespace_get_behavior():
    """Test _PropsNamespace.__getitem__ raises KeyError for missing keys."""
    DivTemplate = _make_lazy_component_cls(html.Div)
    template = DivTemplate(id="test-div", className="set-class")

    props = template._props

    # Set prop returns its value
    assert props["className"] == "set-class"

    # Unset prop raises KeyError
    with pytest.raises(KeyError, match="Property 'style' has not been set"):
        _ = props["style"]

    # "in" check distinguishes set from unset
    assert "className" in props
    assert "style" not in props


def test_props_namespace_attribute_access_raises_error():
    """Test _PropsNamespace.__getattr__ raises AttributeError for missing props."""
    DivTemplate = _make_lazy_component_cls(html.Div)
    template = DivTemplate(id="test-div", className="set-class")

    props = template._props

    # Set prop returns its value
    assert props.className == "set-class"

    # Unset prop raises AttributeError
    with pytest.raises(AttributeError, match="Property 'style' has not been set"):
        _ = props.style

    # "in" check still works
    assert "className" in props
    assert "style" not in props


def test_delete_prop_dict_style():
    """Test deleting properties via dict-style access."""
    DivTemplate = _make_lazy_component_cls(html.Div)
    template = DivTemplate(id="test-div", className="test", style={"color": "red"})

    props = template._props

    # Verify prop exists
    assert "className" in props
    assert props["className"] == "test"

    # Delete the prop
    del props["className"]

    # Verify prop is gone
    assert "className" not in props
    with pytest.raises(KeyError, match="Property 'className' has not been set"):
        _ = props["className"]

    # Other props should still exist
    assert "style" in props


def test_delete_prop_attribute_style():
    """Test deleting properties via attribute access."""
    DivTemplate = _make_lazy_component_cls(html.Div)
    template = DivTemplate(id="test-div", className="test", style={"color": "red"})

    props = template._props

    # Verify prop exists
    assert "className" in props
    assert props.className == "test"

    # Delete the prop
    del props.className

    # Verify prop is gone
    assert "className" not in props
    with pytest.raises(AttributeError, match="Property 'className' has not been set"):
        _ = props.className

    # Other props should still exist
    assert "style" in props


def test_delete_nonexistent_prop_raises_error():
    """Test that deleting a nonexistent prop raises appropriate error."""
    DivTemplate = _make_lazy_component_cls(html.Div)
    template = DivTemplate(id="test-div")

    props = template._props

    # Dict-style deletion of missing prop raises KeyError
    with pytest.raises(KeyError, match="Property 'className' has not been set"):
        del props["className"]

    # Attribute-style deletion of missing prop raises AttributeError
    with pytest.raises(AttributeError, match="Property 'style' has not been set"):
        del props.style


def test_delete_wildcard_prop():
    """Test deleting wildcard properties like data-* and aria-*."""
    DivTemplate = _make_lazy_component_cls(html.Div)
    template = DivTemplate(id="test-div")

    props = template._props

    # Set wildcard props
    props["data-testid"] = "my-component"
    props["aria-label"] = "Label"

    assert "data-testid" in props
    assert "aria-label" in props

    # Delete wildcard props
    del props["data-testid"]
    del props["aria-label"]

    # Verify they're gone
    assert "data-testid" not in props
    assert "aria-label" not in props


def test_cannot_delete_internal_data():
    """Test that _data attribute cannot be deleted."""
    DivTemplate = _make_lazy_component_cls(html.Div)
    template = DivTemplate(id="test-div")

    props = template._props

    # Attempting to delete _data should raise AttributeError
    with pytest.raises(AttributeError, match="Cannot delete internal _data attribute"):
        del props._data
