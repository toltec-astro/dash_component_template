"""Tests for component_factory - dynamic LazyComponent subclass generation."""

import pytest
from dash import dcc, html
from dash_mantine_components import Alert, Button

from dash_component_template import LazyComponent
from dash_component_template.component_info import DashComponentInfo
from dash_component_template.lazy_component import _make_lazy_component_cls


class TestMakeComponentTemplateCls:
    """Tests for _make_lazy_component_cls() internal function."""

    def test_creates_subclass_of_component_template(self):
        """Should create a subclass of LazyComponent (not LazyComponent[T])."""
        subclass = _make_lazy_component_cls(html.Div)
        assert issubclass(subclass, LazyComponent)
        # Factory creates LazyComponent subclasses for runtime efficiency
        # LazyComponent[T] is for manual subclassing

    def test_generated_class_has_correct_name(self):
        """Should generate class name based on component namespace and name."""
        div_subclass = _make_lazy_component_cls(html.Div)
        assert div_subclass.__name__ == "LazyComponentHtmlDiv"

        button_subclass = _make_lazy_component_cls(dcc.Graph)
        assert button_subclass.__name__ == "LazyComponentDccGraph"

    def test_generated_class_has_component_cls_attribute(self):
        """Should set _component_cls as class attribute."""
        subclass = _make_lazy_component_cls(html.Div)
        assert hasattr(subclass, "_component_cls")
        assert subclass._component_cls is html.Div

    def test_generated_class_has_dash_component_info_attribute(self):
        """Should set _dash_component_info as class attribute (private, auto-generated)."""  # noqa: E501
        subclass = _make_lazy_component_cls(html.Div)
        assert hasattr(subclass, "_dash_component_info")
        assert isinstance(subclass._dash_component_info, DashComponentInfo)
        assert subclass._dash_component_info.component_cls is html.Div

    def test_generated_class_has_correct_module(self):
        """Should set __module__ to LazyComponent's module."""
        subclass = _make_lazy_component_cls(html.Div)
        assert subclass.__module__ == LazyComponent.__module__

    def test_different_components_create_different_subclasses(self):
        """Should create distinct subclasses for different components."""
        div_subclass = _make_lazy_component_cls(html.Div)
        button_subclass = _make_lazy_component_cls(html.Button)

        assert div_subclass is not button_subclass
        assert div_subclass.__name__ != button_subclass.__name__
        assert div_subclass._component_cls is not button_subclass._component_cls

    def test_caching_returns_same_subclass(self):
        """Should return cached subclass for same component class."""
        first_call = _make_lazy_component_cls(html.Div)
        second_call = _make_lazy_component_cls(html.Div)

        # Should be the exact same object (identity check)
        assert first_call is second_call

    def test_works_with_dcc_components(self):
        """Should work with dash-core-components."""
        graph_subclass = _make_lazy_component_cls(dcc.Graph)
        assert issubclass(graph_subclass, LazyComponent)
        assert graph_subclass._component_cls is dcc.Graph
        assert graph_subclass.__name__ == "LazyComponentDccGraph"

    def test_works_with_dmc_components(self):
        """Should work with dash-mantine-components."""
        alert_subclass = _make_lazy_component_cls(Alert)
        assert issubclass(alert_subclass, LazyComponent)
        assert alert_subclass._component_cls is Alert
        assert alert_subclass.__name__ == "LazyComponentDmcAlert"

    def test_dash_component_info_has_correct_prop_names(self):
        """Should extract correct property names from component."""
        subclass = _make_lazy_component_cls(html.Div)
        info = subclass._dash_component_info

        # html.Div has these standard props (among others)
        assert "children" in info.prop_names
        assert "id" in info.prop_names
        assert "className" in info.prop_names

    def test_subclass_instances_are_component_template_instances(self):
        """Should be able to instantiate subclass as LazyComponent."""
        subclass = _make_lazy_component_cls(html.Div)
        instance = subclass()

        assert isinstance(instance, LazyComponent)
        assert isinstance(instance, subclass)


class TestLRUCacheManagement:
    """Tests for lru_cache functionality."""

    def test_cache_clear_empties_cache(self):
        """Should clear all cached subclasses."""
        # Create some cached entries
        _make_lazy_component_cls(html.Div)
        _make_lazy_component_cls(html.Button)

        # Clear cache
        _make_lazy_component_cls.cache_clear()

        # Cache info should show 0 cached items
        info = _make_lazy_component_cls.cache_info()
        assert info.currsize == 0

    def test_after_clearing_creates_new_subclass(self):
        """Should create new subclass after clearing (not return old cached one)."""
        first_subclass = _make_lazy_component_cls(html.Div)
        _make_lazy_component_cls.cache_clear()
        second_subclass = _make_lazy_component_cls(html.Div)

        # Should be different objects (new creation)
        assert first_subclass is not second_subclass
        # But should have same structure
        assert first_subclass.__name__ == second_subclass.__name__
        assert first_subclass._component_cls is second_subclass._component_cls

    def test_cache_info_returns_correct_stats(self):
        """Should track cache hits and misses."""
        _make_lazy_component_cls.cache_clear()

        # First call is a miss
        _make_lazy_component_cls(html.Div)
        info = _make_lazy_component_cls.cache_info()
        assert info.misses == 1
        assert info.currsize == 1

        # Second call with same arg is a hit
        _make_lazy_component_cls(html.Div)
        info = _make_lazy_component_cls.cache_info()
        assert info.hits == 1
        assert info.currsize == 1

        # Different component is another miss
        _make_lazy_component_cls(html.Button)
        info = _make_lazy_component_cls.cache_info()
        assert info.misses == 2
        assert info.currsize == 2


class TestCacheIsolation:
    """Tests for cache isolation and independence."""

    def test_cache_is_global(self):
        """Should maintain global cache across function calls."""
        _make_lazy_component_cls.cache_clear()

        # Create in one context
        _make_lazy_component_cls(html.Div)
        info1 = _make_lazy_component_cls.cache_info()

        # Access in another context
        _make_lazy_component_cls(html.Button)
        info2 = _make_lazy_component_cls.cache_info()

        assert info1.currsize == 1
        assert info2.currsize == 2

    def test_different_component_classes_dont_interfere(self):
        """Should keep different component classes separate in cache."""
        _make_lazy_component_cls.cache_clear()

        div_subclass = _make_lazy_component_cls(html.Div)
        button_subclass = _make_lazy_component_cls(html.Button)
        graph_subclass = _make_lazy_component_cls(dcc.Graph)

        # All should be distinct
        assert div_subclass is not button_subclass
        assert button_subclass is not graph_subclass
        assert div_subclass is not graph_subclass

        # But retrieving same component should return cached version
        div_subclass_again = _make_lazy_component_cls(html.Div)
        assert div_subclass is div_subclass_again


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_works_with_multiple_similar_components(self):
        """Should handle multiple components from same library."""
        _make_lazy_component_cls.cache_clear()

        subclasses = [
            _make_lazy_component_cls(html.Div),
            _make_lazy_component_cls(html.Span),
            _make_lazy_component_cls(html.P),
            _make_lazy_component_cls(html.H1),
            _make_lazy_component_cls(html.Button),
        ]

        # All should be distinct
        assert len(set(subclasses)) == 5
        info = _make_lazy_component_cls.cache_info()
        assert info.currsize == 5

    def test_repeated_clear_operations(self):
        """Should handle multiple clear operations safely."""
        _make_lazy_component_cls.cache_clear()
        info = _make_lazy_component_cls.cache_info()
        assert info.currsize == 0

        _make_lazy_component_cls.cache_clear()
        info = _make_lazy_component_cls.cache_info()
        assert info.currsize == 0

        _make_lazy_component_cls(html.Div)
        info = _make_lazy_component_cls.cache_info()
        assert info.currsize == 1

        _make_lazy_component_cls.cache_clear()
        _make_lazy_component_cls.cache_clear()
        info = _make_lazy_component_cls.cache_info()
        assert info.currsize == 0


class TestIntegrationWithComponentInfo:
    """Tests for integration with component_info module."""

    def test_component_info_is_from_get_component_info(self):
        """Should use get_component_info() for dash_component_info attribute."""
        from dash_component_template.component_info import get_component_info

        subclass = _make_lazy_component_cls(html.Div)
        expected_info = get_component_info(html.Div)

        # Should be the exact same cached object
        assert subclass._dash_component_info is expected_info

    def test_component_info_is_frozen_and_immutable(self):
        """Should have frozen immutable DashComponentInfo."""
        subclass = _make_lazy_component_cls(html.Div)
        info = subclass._dash_component_info

        # Should be frozen dataclass
        with pytest.raises((AttributeError, Exception)):
            info._component_cls = html.Button

    def test_component_info_prop_names_is_tuple(self):
        """Should have prop_names as immutable tuple."""
        subclass = _make_lazy_component_cls(html.Div)
        assert isinstance(subclass._dash_component_info.prop_names, tuple)

    def test_component_info_required_props_is_frozenset(self):
        """Should have required_props as immutable frozenset."""
        subclass = _make_lazy_component_cls(html.Div)
        assert isinstance(subclass._dash_component_info.required_props, frozenset)


class TestMultipleComponentLibraries:
    """Tests for working with multiple Dash component libraries."""

    def test_works_with_html_dcc_and_dmc(self):
        """Should work with html, dcc, and dmc components."""
        _make_lazy_component_cls.cache_clear()

        html_subclass = _make_lazy_component_cls(html.Div)
        dcc_subclass = _make_lazy_component_cls(dcc.Graph)
        dmc_subclass = _make_lazy_component_cls(Button)

        info = _make_lazy_component_cls.cache_info()
        assert info.currsize == 3
        assert html_subclass._component_cls is html.Div
        assert dcc_subclass._component_cls is dcc.Graph
        assert dmc_subclass._component_cls is Button

    def test_all_subclasses_are_component_template_subclasses(self):
        """All generated subclasses should inherit from LazyComponent."""
        _make_lazy_component_cls.cache_clear()

        subclasses = [
            _make_lazy_component_cls(html.Div),
            _make_lazy_component_cls(dcc.Graph),
            _make_lazy_component_cls(Button),
        ]

        for subclass in subclasses:
            assert issubclass(subclass, LazyComponent)


# Fixture to auto-clear lru_cache between tests
@pytest.fixture(autouse=True)
def auto_clear_cache():
    """Automatically clear lru_cache before each test."""
    _make_lazy_component_cls.cache_clear()
    yield
    # Optionally clean up after test as well
    _make_lazy_component_cls.cache_clear()
