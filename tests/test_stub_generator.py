"""Tests for type stub generation.

This module tests the stub_generator functionality to ensure
type stubs are generated correctly for Dash components.
"""

import tempfile
from pathlib import Path

import pytest
from dash import html

from dash_component_template.stub_generator import (
    format_type_annotation,
    generate_stub_for_component,
    generate_stubs_for_namespace,
    write_stub_file,
)


class TestFormatTypeAnnotation:
    """Test type annotation formatting."""

    def test_simple_types(self):
        """Simple types should be preserved."""
        assert format_type_annotation(str) == "str"
        assert format_type_annotation(int) == "int"
        assert format_type_annotation(bool) == "bool"
        assert format_type_annotation(dict) == "dict"
        assert format_type_annotation(list) == "list"

    def test_none_type(self):
        """None type should be formatted as 'None'."""
        assert format_type_annotation(None) == "None"
        assert format_type_annotation(type(None)) == "None"

    def test_complex_types_become_any(self):
        """Complex types should be simplified to Any."""
        # Long type strings
        long_type = "Sequence[str | int | float | Component | None]"
        assert format_type_annotation(long_type) == "Any"

        # Dash internal types
        dash_type = "dash.development.base_component.Component"
        assert format_type_annotation(dash_type) == "Any"


class TestGenerateStubForComponent:
    """Test stub generation for individual components."""

    def test_generate_div_stub(self):
        """Should generate valid stub for html.Div."""
        stub = generate_stub_for_component(html.Div)

        # Check structure (now includes namespace prefix)
        assert "class LazyComponentHtmlDiv(LazyComponent):" in stub
        assert "def __init__(" in stub
        assert "className:" in stub
        assert "style:" in stub
        assert "children:" in stub

        # Check imports (when include_imports=True)
        assert "from __future__ import annotations" in stub
        assert "from typing import" in stub and "Any" in stub
        assert (
            "from dash_component_template.component_template import LazyComponent"
            in stub
            or "TYPE_CHECKING" in stub
        )

    def test_generate_button_stub(self):
        """Should generate valid stub for html.Button."""
        stub = generate_stub_for_component(html.Button)

        assert "class LazyComponentHtmlButton(LazyComponent):" in stub
        assert "children:" in stub
        assert "n_clicks:" in stub

    def test_without_imports(self):
        """Should generate stub without imports when requested."""
        stub = generate_stub_for_component(html.Div, include_imports=False)

        assert "from __future__ import annotations" not in stub
        assert "from typing import Any" not in stub
        assert "class LazyComponentHtmlDiv(LazyComponent):" in stub

    def test_reserved_names_encoded(self):
        """Property names should be used directly (no encoding needed)."""
        stub = generate_stub_for_component(html.Div)

        # Properties use direct names (instance attributes don't shadow builtins)
        assert "id:" in stub
        assert "children:" in stub

    def test_all_properties_optional(self):
        """All properties should be optional (| None)."""
        stub = generate_stub_for_component(html.Div)

        # Check that properties have | None
        assert "className: str | None" in stub or "className: Any | None" in stub
        assert "= None" in stub  # Default values


class TestWriteStubFile:
    """Test writing stub files to disk."""

    def test_write_stub_file(self):
        """Should write stub file to specified directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = write_stub_file(html.Div, tmpdir, namespace="html")

            # Check file exists
            assert path.exists()
            assert path.name == "html.pyi"

            # Check content (now includes namespace prefix)
            content = path.read_text()
            assert "class LazyComponentHtmlDiv(LazyComponent):" in content

    def test_write_multiple_stubs(self):
        """Should be able to write multiple stub files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path1 = write_stub_file(html.Div, tmpdir, namespace="div")
            path2 = write_stub_file(html.Button, tmpdir, namespace="button")

            assert path1.exists() and path1.name == "div.pyi"
            assert path2.exists() and path2.name == "button.pyi"
            assert path1 != path2


class TestGenerateStubsForNamespace:
    """Test generating stubs for entire namespaces."""

    def test_generate_html_namespace(self):
        """Should generate stubs for dash.html namespace."""
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = generate_stubs_for_namespace("dash.html", tmpdir)

            # Should create one file
            assert len(paths) == 1
            assert paths[0].name == "html.pyi"

            # Check content
            content = paths[0].read_text()

            # Should contain multiple component classes (with Html namespace prefix)
            assert "class LazyComponentHtmlDiv(LazyComponent):" in content
            assert "class LazyComponentHtmlButton(LazyComponent):" in content
            assert "class LazyComponentHtmlA(LazyComponent):" in content

            # Should have proper header
            assert "Type stubs for dash.html" in content
            assert "Auto-generated" in content

    def test_generate_dcc_namespace(self):
        """Should generate stubs for dash.dcc namespace."""
        with tempfile.TemporaryDirectory() as tmpdir:
            paths = generate_stubs_for_namespace("dash.dcc", tmpdir)

            # Should create one file
            assert len(paths) == 1
            assert paths[0].name == "dcc.pyi"

            # Check content
            content = paths[0].read_text()
            assert "class LazyComponentDccDropdown(LazyComponent):" in content
            assert "class LazyComponentDccGraph(LazyComponent):" in content

    def test_invalid_namespace(self):
        """Should raise error for invalid namespace."""
        with tempfile.TemporaryDirectory() as tmpdir:  # noqa: SIM117
            with pytest.raises(ValueError, match="Cannot import"):
                generate_stubs_for_namespace("nonexistent.module", tmpdir)

    def test_namespace_without_components(self):
        """Should raise error for namespace without components."""
        with tempfile.TemporaryDirectory() as tmpdir:  # noqa: SIM117
            with pytest.raises(ValueError, match="No Component subclasses"):
                # os module has no Dash components
                generate_stubs_for_namespace("os", tmpdir)


class TestStubFileStructure:
    """Test the actual generated stub files in the package."""

    def test_html_stub_exists(self):
        """html.pyi stub file should exist."""
        from dash_component_template import stub_generator

        stubs_dir = Path(stub_generator.__file__).parent / "stubs"
        html_stub = stubs_dir / "html.pyi"

        assert html_stub.exists(), "html.pyi not found - run stub generator"

    def test_dcc_stub_exists(self):
        """dcc.pyi stub file should exist."""
        from dash_component_template import stub_generator

        stubs_dir = Path(stub_generator.__file__).parent / "stubs"
        dcc_stub = stubs_dir / "dcc.pyi"

        assert dcc_stub.exists(), "dcc.pyi not found - run stub generator"

    def test_py_typed_exists(self):
        """py.typed marker file should exist for PEP 561 compliance."""
        from dash_component_template import stub_generator

        package_dir = Path(stub_generator.__file__).parent
        py_typed = package_dir / "py.typed"

        assert py_typed.exists(), "py.typed marker not found"

    def test_html_stub_completeness(self):
        """html.pyi should contain all major HTML components."""
        from dash_component_template import stub_generator

        stubs_dir = Path(stub_generator.__file__).parent / "stubs"
        html_stub = stubs_dir / "html.pyi"

        if not html_stub.exists():
            pytest.skip("html.pyi not generated yet")

        content = html_stub.read_text()

        # Check for common components (with Html namespace prefix)
        assert "LazyComponentHtmlDiv" in content
        assert "LazyComponentHtmlButton" in content
        assert "LazyComponentHtmlA" in content  # <a> tag
        assert "LazyComponentHtmlForm" in content
        assert "LazyComponentHtmlTable" in content

    def test_dcc_stub_completeness(self):
        """dcc.pyi should contain all major DCC components."""
        from dash_component_template import stub_generator

        stubs_dir = Path(stub_generator.__file__).parent / "stubs"
        dcc_stub = stubs_dir / "dcc.pyi"

        if not dcc_stub.exists():
            pytest.skip("dcc.pyi not generated yet")

        content = dcc_stub.read_text()

        # Check for common components (with Dcc namespace prefix)
        assert "LazyComponentDccDropdown" in content
        assert "LazyComponentDccGraph" in content
        assert "LazyComponentDccSlider" in content
        assert "LazyComponentDccInput" in content


class TestStubUsability:
    """Test that stubs work as expected for IDEs."""

    def test_stub_matches_runtime(self):
        """Stub should match runtime class properties."""
        from dash_component_template.lazy_component import _make_lazy_component_cls

        # Create runtime class
        DivTemplate = _make_lazy_component_cls(html.Div)

        # Generate stub
        stub = generate_stub_for_component(html.Div)

        # Check that stub contains runtime properties
        instance = DivTemplate()

        # In v3.0, properties are accessed via .props namespace
        assert hasattr(instance, "props"), "Runtime missing props namespace"

        # These properties should exist in stub
        for prop in ["className", "style", "id", "children"]:
            # Stub check - should be in the generated stub
            assert f"{prop}:" in stub, f"Stub missing {prop}"
