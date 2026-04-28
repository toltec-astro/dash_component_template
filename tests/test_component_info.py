"""Tests for component_info module."""

import dash_mantine_components as dmc
import pytest
from dash import dcc, html

from dash_component_template.component_info import (
    DashComponentInfo,
    clear_component_info_cache,
    get_component_info,
)


class TestDashComponentInfo:
    """Test DashComponentInfo dataclass."""

    def test_from_component_cls_html_div(self):
        """Test introspecting html.Div."""
        info = DashComponentInfo.from_component_cls(html.Div)

        assert info.component_cls is html.Div
        assert isinstance(info.prop_names, tuple)
        assert len(info.prop_names) > 0

        # Common properties should be present
        assert "children" in info.prop_names
        assert "id" in info.prop_names
        assert "className" in info.prop_names
        assert "style" in info.prop_names

    def test_from_component_cls_html_button(self):
        """Test introspecting html.Button."""
        info = DashComponentInfo.from_component_cls(html.Button)

        assert info.component_cls is html.Button
        assert "children" in info.prop_names
        assert "id" in info.prop_names
        assert isinstance(info.prop_names, tuple)

    def test_from_component_cls_dcc_dropdown(self):
        """Test introspecting dcc.Dropdown."""
        info = DashComponentInfo.from_component_cls(dcc.Dropdown)

        assert info.component_cls is dcc.Dropdown
        assert "id" in info.prop_names
        assert "options" in info.prop_names
        assert "value" in info.prop_names

    def test_from_component_cls_dmc_button(self):
        """Test introspecting dmc.Button."""
        info = DashComponentInfo.from_component_cls(dmc.Button)

        assert info.component_cls is dmc.Button
        assert "children" in info.prop_names
        assert isinstance(info.prop_names, tuple)

    def test_prop_defaults(self):
        """Test extracting default values."""
        info = DashComponentInfo.from_component_cls(html.Div)

        # Should have defaults dict (even if empty for some components)
        assert isinstance(info.prop_defaults, dict)

        # Most Dash components have many optional parameters with defaults
        # Just verify the structure is correct
        for prop_name, _default_value in info.prop_defaults.items():  # noqa: PERF102
            assert prop_name in info.prop_names

    def test_required_props(self):
        """Test identifying required props."""
        info = DashComponentInfo.from_component_cls(html.Div)

        # Should be a frozenset
        assert isinstance(info.required_props, frozenset)

        # All required props should be in prop_names
        for prop_name in info.required_props:
            assert prop_name in info.prop_names

        # Required props should not have defaults
        for prop_name in info.required_props:
            assert prop_name not in info.prop_defaults

    def test_prop_annotations(self):
        """Test extracting type annotations."""
        info = DashComponentInfo.from_component_cls(html.Div)

        # Should have annotations dict
        assert isinstance(info.prop_annotations, dict)

        # All annotated props should be in prop_names
        for prop_name in info.prop_annotations:
            assert prop_name in info.prop_names

    def test_immutable_frozen(self):
        """Test that DashComponentInfo is immutable (frozen)."""
        info = DashComponentInfo.from_component_cls(html.Div)

        # Cannot modify attributes on frozen dataclass
        with pytest.raises(AttributeError):
            info.component_cls = html.Button

        with pytest.raises(AttributeError):
            info.prop_names = ("test",)

    def test_immutable_collections(self):
        """Test that collections are immutable types."""
        info = DashComponentInfo.from_component_cls(html.Div)

        # prop_names should be tuple (immutable)
        assert isinstance(info.prop_names, tuple)

        # required_props should be frozenset (immutable)
        assert isinstance(info.required_props, frozenset)

    def test_slots(self):
        """Test that dataclass uses slots for memory efficiency."""
        info = DashComponentInfo.from_component_cls(html.Div)

        # Should have __slots__
        assert hasattr(DashComponentInfo, "__slots__")

        # Should not have __dict__ (slots prevent it)
        assert not hasattr(info, "__dict__")

    def test_repr(self):
        """Test clean repr."""
        info = DashComponentInfo.from_component_cls(html.Div)
        repr_str = repr(info)

        assert "DashComponentInfo" in repr_str
        assert "Div" in repr_str
        assert "props=" in repr_str

    def test_from_component_cls_preserves_order(self):
        """Test that property order is preserved."""
        info = DashComponentInfo.from_component_cls(html.Div)

        # Should have consistent order across calls
        info2 = DashComponentInfo.from_component_cls(html.Div)
        assert info.prop_names == info2.prop_names

    def test_from_component_cls_filters_special_params(self):
        """Test that self, *args, **kwargs are filtered out."""
        info = DashComponentInfo.from_component_cls(html.Div)

        # These should not be in prop_names
        assert "self" not in info.prop_names
        assert "args" not in info.prop_names
        assert "kwargs" not in info.prop_names


class TestGetComponentInfo:
    """Test get_component_info caching function."""

    def test_basic_usage(self):
        """Test basic usage."""
        info = get_component_info(html.Div)

        assert isinstance(info, DashComponentInfo)
        assert info.component_cls is html.Div

    def test_caching_same_component(self):
        """Test that results are cached."""
        clear_component_info_cache()

        info1 = get_component_info(html.Div)
        info2 = get_component_info(html.Div)

        # Same object (cached)
        assert info1 is info2

    def test_different_components_different_info(self):
        """Test different components get different info."""
        info_div = get_component_info(html.Div)
        info_btn = get_component_info(html.Button)

        assert info_div is not info_btn
        assert info_div.component_cls is html.Div
        assert info_btn.component_cls is html.Button
        assert info_div.prop_names != info_btn.prop_names

    def test_cache_clear(self):
        """Test cache clearing."""
        info1 = get_component_info(html.Div)

        # Clear cache
        clear_component_info_cache()

        info2 = get_component_info(html.Div)

        # Different objects after clear
        assert info1 is not info2

        # But same data
        assert info1.component_cls is info2.component_cls
        assert info1.prop_names == info2.prop_names

    def test_cache_with_multiple_components(self):
        """Test cache works with multiple component types."""
        clear_component_info_cache()

        # Cache several components
        info_div = get_component_info(html.Div)
        info_btn = get_component_info(html.Button)
        info_span = get_component_info(html.Span)

        # All should be cached independently
        assert get_component_info(html.Div) is info_div
        assert get_component_info(html.Button) is info_btn
        assert get_component_info(html.Span) is info_span

    def test_works_with_dcc_components(self):
        """Test with dash-core-components."""
        info = get_component_info(dcc.Dropdown)

        assert info.component_cls is dcc.Dropdown
        assert "options" in info.prop_names
        assert "value" in info.prop_names

    def test_works_with_dmc_components(self):
        """Test with dash-mantine-components."""
        info = get_component_info(dmc.Button)

        assert info.component_cls is dmc.Button
        assert "children" in info.prop_names

    def test_cache_info_available(self):
        """Test that cache info is available for inspection."""
        clear_component_info_cache()

        # Cache should start empty
        cache_info = get_component_info.cache_info()
        assert cache_info.hits == 0
        assert cache_info.misses == 0

        # First call is a miss
        get_component_info(html.Div)
        cache_info = get_component_info.cache_info()
        assert cache_info.misses == 1

        # Second call is a hit
        get_component_info(html.Div)
        cache_info = get_component_info.cache_info()
        assert cache_info.hits == 1


class TestClearComponentInfoCache:
    """Test clear_component_info_cache function."""

    def test_clears_cache(self):
        """Test that cache is cleared."""
        # Populate cache
        info1 = get_component_info(html.Div)

        # Clear
        clear_component_info_cache()

        # Cache info should be reset
        cache_info = get_component_info.cache_info()
        assert cache_info.hits == 0
        assert cache_info.misses == 0

        # Next call creates new object
        info2 = get_component_info(html.Div)
        assert info1 is not info2

    def test_multiple_clears(self):
        """Test multiple clears don't cause issues."""
        clear_component_info_cache()
        clear_component_info_cache()
        clear_component_info_cache()

        # Should still work fine
        info = get_component_info(html.Div)
        assert isinstance(info, DashComponentInfo)


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_component_with_minimal_props(self):
        """Test component with minimal properties."""
        # Even minimal components should work
        info = get_component_info(html.Hr)

        assert info.component_cls is html.Hr
        assert isinstance(info.prop_names, tuple)
        # Hr should have at least 'id'
        assert len(info.prop_names) >= 1

    def test_component_with_many_props(self):
        """Test component with many properties."""
        # Dropdown has many properties
        info = get_component_info(dcc.Dropdown)

        assert len(info.prop_names) > 10
        # Should have key properties
        assert "options" in info.prop_names
        assert "value" in info.prop_names
        assert "multi" in info.prop_names
