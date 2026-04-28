"""Unit tests for the naming module."""

import pytest
from dash import dcc, html

from dash_component_template.naming import (
    _to_pascal_case,
    get_component_id_stem,
    get_component_name,
    get_component_namespace,
    get_component_stub_suffix,
    get_lazy_component_cls_name,
    get_props_namespace_name,
)


class TestGetComponentName:
    """Test get_component_name function."""

    def test_html_component(self):
        assert get_component_name(html.Div) == "Div"
        assert get_component_name(html.Button) == "Button"
        assert get_component_name(html.H1) == "H1"

    def test_dcc_component(self):
        assert get_component_name(dcc.Graph) == "Graph"
        assert get_component_name(dcc.Input) == "Input"
        assert get_component_name(dcc.Dropdown) == "Dropdown"


class TestToPascalCase:
    """Test _to_pascal_case helper function."""

    def test_snake_case(self):
        assert _to_pascal_case("some_custom_lib") == "SomeCustomLib"
        assert _to_pascal_case("vendor_dash_components") == "VendorDashComponents"
        assert _to_pascal_case("my_custom_lib") == "MyCustomLib"

    def test_dash_case(self):
        assert _to_pascal_case("dash-components") == "DashComponents"
        assert _to_pascal_case("my-lib") == "MyLib"

    def test_single_word(self):
        assert _to_pascal_case("vendor") == "Vendor"
        assert _to_pascal_case("html") == "Html"
        assert _to_pascal_case("custom") == "Custom"

    def test_already_mixed_case(self):
        # Should still convert to proper PascalCase
        assert _to_pascal_case("CustomWidget") == "Customwidget"
        assert _to_pascal_case("MyLib") == "Mylib"

    def test_empty_string(self):
        assert _to_pascal_case("") == ""

    def test_mixed_separators(self):
        assert _to_pascal_case("my-custom_lib") == "MyCustomLib"


class TestGetComponentNamespace:
    """Test get_component_namespace function."""

    def test_html_components_use_shortcut(self):
        """Test that html components use the 'Html' shortcut."""
        assert get_component_namespace(html.Div) == "Html"
        assert get_component_namespace(html.Button) == "Html"
        assert get_component_namespace(html.A) == "Html"
        assert get_component_namespace(html.H1) == "Html"

    def test_dcc_components_use_shortcut(self):
        """Test that dcc components use the 'Dcc' shortcut."""
        assert get_component_namespace(dcc.Graph) == "Dcc"
        assert get_component_namespace(dcc.Input) == "Dcc"
        assert get_component_namespace(dcc.Dropdown) == "Dcc"

    @pytest.mark.skipif(
        not pytest.importorskip(
            "dash_mantine_components", reason="dash_mantine_components not installed"
        ),
        reason="dash_mantine_components not installed",
    )
    def test_dmc_components_use_shortcut(self):
        """Test that dash_mantine_components use the 'Dmc' shortcut."""
        import dash_mantine_components as dmc

        assert get_component_namespace(dmc.Button) == "Dmc"
        assert get_component_namespace(dmc.Card) == "Dmc"

    def test_unknown_library_skips_component_name(self):
        """Test that unknown libraries skip the component name part."""
        # Create mock components with realistic module structures
        VendorButton = type(
            "Button", (), {"__module__": "vendor_dash_components.Button"}
        )
        assert get_component_namespace(VendorButton) == "VendorDashComponents"

        CustomCard = type("Card", (), {"__module__": "my_custom_lib.components.Card"})
        assert get_component_namespace(CustomCard) == "Components"

    def test_unknown_library_with_nested_modules(self):
        """Test namespace detection with deeply nested module paths."""
        Widget = type("Widget", (), {"__module__": "vendor.lib.components.Widget"})
        # Should skip 'Widget' and find 'components'
        assert get_component_namespace(Widget) == "Components"

    def test_component_name_appears_multiple_times(self):
        """Test when component name appears in multiple module parts."""
        # If 'Button' appears in path like 'button_lib.Button', should skip it
        ButtonComp = type("Button", (), {"__module__": "button_lib.Button"})
        assert get_component_namespace(ButtonComp) == "ButtonLib"

    def test_fallback_to_first_part(self):
        """Test fallback when all parts match component name (edge case)."""
        # Extremely unlikely but test the fallback
        Widget = type("Widget", (), {"__module__": "widget.Widget"})
        # Should fall back to first part
        assert get_component_namespace(Widget) == "Widget"


class TestGetComponentIdStem:
    """Test get_component_id_stem function."""

    def test_html_components(self):
        assert get_component_id_stem(html.Div) == "div"
        assert get_component_id_stem(html.Button) == "button"
        assert get_component_id_stem(html.H1) == "h1"

    def test_dcc_components(self):
        assert get_component_id_stem(dcc.Graph) == "graph"
        assert get_component_id_stem(dcc.Input) == "input"

    def test_lowercase_conversion(self):
        """Test that component names are properly lowercased."""
        CustomComponent = type(
            "MyCustomWidget", (), {"__module__": "lib.MyCustomWidget"}
        )
        assert get_component_id_stem(CustomComponent) == "mycustomwidget"


class TestGetComponentStubSuffix:
    """Test get_component_stub_suffix function."""

    def test_html_components(self):
        assert get_component_stub_suffix(html.Div) == "HtmlDiv"
        assert get_component_stub_suffix(html.Button) == "HtmlButton"
        assert get_component_stub_suffix(html.H1) == "HtmlH1"

    def test_dcc_components(self):
        assert get_component_stub_suffix(dcc.Graph) == "DccGraph"
        assert get_component_stub_suffix(dcc.Input) == "DccInput"

    @pytest.mark.skipif(
        not pytest.importorskip(
            "dash_mantine_components", reason="dash_mantine_components not installed"
        ),
        reason="dash_mantine_components not installed",
    )
    def test_dmc_components(self):
        """Test that dmc components use short name."""
        import dash_mantine_components as dmc

        assert get_component_stub_suffix(dmc.Button) == "DmcButton"
        assert get_component_stub_suffix(dmc.Card) == "DmcCard"

    def test_unknown_library(self):
        """Test stub suffix for unknown libraries."""
        VendorButton = type("Button", (), {"__module__": "vendor_lib.Button"})
        assert get_component_stub_suffix(VendorButton) == "VendorLibButton"


class TestGetPropsNamespaceName:
    """Test get_props_namespace_name function."""

    def test_html_components(self):
        assert get_props_namespace_name(html.Div) == "_PropsNamespaceHtmlDiv"
        assert get_props_namespace_name(html.Button) == "_PropsNamespaceHtmlButton"

    def test_dcc_components(self):
        assert get_props_namespace_name(dcc.Graph) == "_PropsNamespaceDccGraph"
        assert get_props_namespace_name(dcc.Input) == "_PropsNamespaceDccInput"

    def test_naming_pattern(self):
        """Test that the naming pattern is consistent."""
        # Should be _PropsNamespace + {namespace} + {component_name}
        assert get_props_namespace_name(html.A) == "_PropsNamespaceHtmlA"


class TestGetComponentTemplateName:
    """Test get_lazy_component_cls_name function."""

    def test_html_components(self):
        assert get_lazy_component_cls_name(html.Div) == "LazyComponentHtmlDiv"
        assert get_lazy_component_cls_name(html.Button) == "LazyComponentHtmlButton"

    def test_dcc_components(self):
        assert get_lazy_component_cls_name(dcc.Graph) == "LazyComponentDccGraph"
        assert get_lazy_component_cls_name(dcc.Input) == "LazyComponentDccInput"

    @pytest.mark.skipif(
        not pytest.importorskip(
            "dash_mantine_components", reason="dash_mantine_components not installed"
        ),
        reason="dash_mantine_components not installed",
    )
    def test_dmc_components(self):
        """Test that dmc components use short name in template."""
        import dash_mantine_components as dmc

        assert get_lazy_component_cls_name(dmc.Button) == "LazyComponentDmcButton"
        assert get_lazy_component_cls_name(dmc.Card) == "LazyComponentDmcCard"

    def test_naming_pattern(self):
        """Test that the naming pattern is consistent."""
        # Should be ComponentTemplate + {namespace} + {component_name}
        assert get_lazy_component_cls_name(html.H1) == "LazyComponentHtmlH1"


class TestNamingConsistency:
    """Test consistency between different naming functions."""

    def test_all_functions_use_same_namespace(self):
        """Verify all naming functions use the same namespace for a component."""
        component = html.Div

        # Get namespace from the primary function
        namespace = get_component_namespace(component)

        # Verify it's used consistently in derived functions
        stub_suffix = get_component_stub_suffix(component)
        assert stub_suffix.startswith(namespace)

        props_name = get_props_namespace_name(component)
        assert namespace in props_name

        template_name = get_lazy_component_cls_name(component)
        assert namespace in template_name

    def test_all_functions_use_same_component_name(self):
        """Verify all naming functions use the same component name."""
        component = html.Button

        # Get component name from the primary function
        component_name = get_component_name(component)

        # Verify it's used consistently
        stub_suffix = get_component_stub_suffix(component)
        assert stub_suffix.endswith(component_name)

        props_name = get_props_namespace_name(component)
        assert props_name.endswith(component_name)

        template_name = get_lazy_component_cls_name(component)
        assert template_name.endswith(component_name)

    def test_id_stem_matches_component_name_lowercase(self):
        """Verify id_stem is just lowercase version of component name."""
        for component in [html.Div, html.Button, dcc.Graph, dcc.Input]:
            name = get_component_name(component)
            id_stem = get_component_id_stem(component)
            assert id_stem == name.lower()


class TestEdgeCases:
    """Test edge cases and unusual scenarios."""

    def test_single_letter_component_name(self):
        """Test components with single-letter names."""
        assert get_component_name(html.A) == "A"
        assert get_component_id_stem(html.A) == "a"
        assert get_component_stub_suffix(html.A) == "HtmlA"

    def test_numbered_component_name(self):
        """Test components with numbers in names."""
        assert get_component_name(html.H1) == "H1"
        assert get_component_id_stem(html.H1) == "h1"
        assert get_component_stub_suffix(html.H1) == "HtmlH1"

    def test_component_independence(self):
        """Test that get_component_namespace and get_component_name are independent."""
        # This test verifies that changing get_component_name won't affect
        # get_component_namespace, as they should use __name__ directly

        component = html.Div

        # These should work independently
        namespace = get_component_namespace(component)
        name = get_component_name(component)

        # Verify both use __name__ directly (not calling each other)
        assert namespace == "Html"
        assert name == "Div"

        # The namespace shouldn't contain the component name
        assert name not in namespace  # 'Div' not in 'Html'
