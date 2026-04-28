r"""Type stub (.pyi) generation for ComponentTemplate classes.

This module generates Python type stub files (.pyi) for dynamically created
ComponentTemplate subclasses. This enables full IDE autocomplete and type
checking for Dash component properties.

Type stubs are generated following PEP 484 conventions and best practices:
- Located in py.typed package or stubs/ directory
- Mirror the runtime module structure
- Provide complete type information for IDE/type checkers

Example:
    >>> from dash import html  # doctest: +SKIP
    >>> stub_content = generate_stub_for_component(html.Div)  # doctest: +SKIP
    >>> 'ComponentTemplateDiv' in stub_content  # doctest: +SKIP
    True

Usage:
    # Generate all stubs for dash.html namespace  # doctest: +SKIP
    >>> generate_stubs_for_namespace('dash.html')
    [PosixPath('stubs/html.pyi')]

    # Generate stub for single component  # doctest: +SKIP
    >>> write_stub_file(html.Div, 'stubs/')  # doctest: +SKIP
    PosixPath('stubs/Div.pyi')
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from dash.development.base_component import Component

from .component_info import get_component_info
from .naming import (
    get_lazy_component_cls_name,
    get_props_namespace_name,
)

if TYPE_CHECKING:
    from .component_info import DashComponentInfo

__all__ = [
    "format_type_annotation",
    "generate_stub_for_component",
    "generate_stubs_for_namespace",
    "write_stub_file",
]

# Magic value constants for type annotation complexity thresholds
_COMPLEX_TYPE_MAX_LEN = 50
_INNER_TYPE_MAX_LEN = 30
_UNION_TYPE_MAX_LEN = 50
_MIN_ARGV_ARGS = 2

# Set of simple built-in type names that need no transformation
_SIMPLE_TYPES = frozenset(
    {
        "str",
        "int",
        "float",
        "bool",
        "dict",
        "list",
        "tuple",
        "set",
        "frozenset",
        "bytes",
        "bytearray",
    }
)

# Maps namespace paths to (class_prefix, namespace_prefix) for template class naming
_NAMESPACE_PREFIX_MAP: dict[str, tuple[str, str]] = {
    "dash.html": ("LazyComponent", "Html"),
    "dash.dcc": ("LazyComponent", "Dcc"),
    "dash_mantine_components": ("LazyComponent", "Dmc"),
    "dash_bootstrap_components": ("ComponentTemplate", "Dbc"),
    "dash_table": ("ComponentTemplate", "DashTable"),
    "dash_ag_grid": ("ComponentTemplate", "DashAgGrid"),
    "dash_daq": ("ComponentTemplate", "Daq"),
}


def _handle_forwardref(annotation_str: str) -> str | None:
    """Handle ForwardRef('TypeName') annotation strings.

    Parameters
    ----------
    annotation_str : str
        String representation of the annotation.

    Returns
    -------
    str | None
        Formatted string for the stub, or None if not a ForwardRef.
    """
    if not (annotation_str.startswith("ForwardRef(") and annotation_str.endswith(")")):
        return None
    inner = annotation_str[11:-1]  # Remove ForwardRef( and )
    if inner.startswith("'") and inner.endswith("'"):
        return inner  # Keep the quotes
    return f'"{inner}"'


def _handle_complex_type(annotation_str: str) -> str | None:
    """Return 'Any' if the type is too complex for stub files.

    Parameters
    ----------
    annotation_str : str
        String representation of the annotation.

    Returns
    -------
    str | None
        'Any' if complex, or None if not complex.
    """
    if (
        len(annotation_str) > _COMPLEX_TYPE_MAX_LEN
        or "dash.development.base_component" in annotation_str
        or "Sequence[" in annotation_str
        or "Literal[" in annotation_str
        or "SupportsFloat" in annotation_str
        or "SupportsInt" in annotation_str
        or "SupportsComplex" in annotation_str
    ):
        return "Any"
    return None


def _handle_class_type(annotation_str: str) -> str | None:
    """Handle <class 'typename'> annotation strings.

    Parameters
    ----------
    annotation_str : str
        String representation of the annotation.

    Returns
    -------
    str | None
        Class name string or 'Any', or None if not a class type.
    """
    if not (annotation_str.startswith("<class '") and annotation_str.endswith("'>")):
        return None
    inner = annotation_str[8:-2]
    return inner if "." not in inner else "Any"


def _handle_optional(annotation_str: str) -> str | None:
    """Handle Optional[T] annotation strings.

    Parameters
    ----------
    annotation_str : str
        String representation of the annotation.

    Returns
    -------
    str | None
        'T | None' string or None if not Optional.
    """
    if not annotation_str.startswith("Optional["):
        return None
    inner = annotation_str[9:-1]
    if "ForwardRef(" in inner:
        return "Any | None"
    if len(inner) > _INNER_TYPE_MAX_LEN:
        return "Any"
    return f"{inner} | None"


def _handle_union(annotation_str: str) -> str | None:
    """Handle Union[A, B, ...] annotation strings.

    Parameters
    ----------
    annotation_str : str
        String representation of the annotation.

    Returns
    -------
    str | None
        Union string or None if not a Union.
    """
    if not annotation_str.startswith("Union["):
        return None
    union_content = annotation_str[6:-1]
    if "ForwardRef(" in union_content:
        return "Any"
    if len(union_content) > _UNION_TYPE_MAX_LEN:
        return "Any"
    return union_content.replace(", ", " | ")


def format_type_annotation(annotation: Any) -> str:
    """Format a type annotation for .pyi stub file.

    Converts Python type objects to their string representation suitable
    for type stub files. Handles common patterns:
    - None -> None
    - typing.Optional[T] -> T | None
    - typing.Union[A, B] -> A | B
    - typing.List[T] -> list[T]
    - Complex types -> Any

    Parameters
    ----------
    annotation : Any
        Type annotation from inspect or get_type_hints.

    Returns
    -------
    str
        String representation suitable for .pyi files.

    Examples
    --------
    >>> format_type_annotation(str)
    'str'
    >>> format_type_annotation(int | None)
    'int | None'
    >>> format_type_annotation(list[str])
    'Any'
    """
    if annotation is None or annotation is type(None):
        return "None"

    annotation_str = str(annotation).replace("NoneType", "None")

    # Handle ForwardRef and complex types before cleaning typing. prefix
    for handler in (_handle_forwardref, _handle_complex_type):
        result = handler(annotation_str)
        if result is not None:
            return result

    # Clean up typing module prefixes
    annotation_str = annotation_str.replace("typing.", "")

    # Handle class types, Optional, Union
    for handler in (_handle_class_type, _handle_optional, _handle_union):
        result = handler(annotation_str)
        if result is not None:
            return result

    if annotation_str in _SIMPLE_TYPES:
        return annotation_str
    if "<" in annotation_str or "[" in annotation_str or "." in annotation_str:
        return "Any"
    return annotation_str


def _format_prop_type(prop_name: str, info: DashComponentInfo) -> str:
    """Get formatted type string for a prop, ensuring it is nullable.

    Parameters
    ----------
    prop_name : str
        Name of the property.
    info : DashComponentInfo
        Component info containing annotations.

    Returns
    -------
    str
        Formatted type string with '| None' if needed.
    """
    if prop_name in info.prop_annotations:
        type_str = format_type_annotation(info.prop_annotations[prop_name])
    else:
        type_str = "Any"
    if type_str != "None" and " | None" not in type_str:
        type_str = f"{type_str} | None"
    return type_str


def _build_prop_attribute_lines(info: DashComponentInfo) -> list[str]:
    """Build typed attribute declaration lines for the props namespace class.

    Parameters
    ----------
    info : DashComponentInfo
        Component info with prop names and annotations.

    Returns
    -------
    list[str]
        Lines for the props namespace class body.
    """
    if not info.prop_names:
        return ["    pass"]
    return [
        f"    {prop_name}: {_format_prop_type(prop_name, info)}"
        for prop_name in info.prop_names
    ]


def _build_init_param_lines(info: DashComponentInfo) -> list[str]:
    """Build __init__ parameter lines for the component template stub class.

    Parameters
    ----------
    info : DashComponentInfo
        Component info with prop names and annotations.

    Returns
    -------
    list[str]
        Lines for the __init__ parameter list.
    """
    return [
        f"        {prop_name}: {_format_prop_type(prop_name, info)} = None,"
        for prop_name in info.prop_names
    ]


def generate_stub_for_component(
    _component_cls: type[Component],
    include_imports: bool = True,
    namespace: str | None = None,
) -> str:
    """Generate type stub content for a single component class.

    Creates a complete .pyi stub file content using two-layer architecture:
    - Import statements (if include_imports=True)
    - PropsNamespace class with attribute declarations only
    - ComponentTemplate subclass with props: PropsNamespace type hint
    - Full __init__ signature with all parameters

    The stub matches the actual _PropsNamespace implementation which only
    provides:
    - Attribute access via __getattr__/__setattr__
    - Dict-style access via __getitem__/__setitem__/__contains__
    - Iteration via __iter__/__len__

    Uses centralized naming utilities for consistent class names:
    - LazyComponentHtmlDiv (not ComponentTemplateDiv)
    - _PropsNamespaceHtmlDiv (not _DivPropsNamespace)

    Parameters
    ----------
    _component_cls : type[Component]
        Dash component class (e.g., html.Div).
    include_imports : bool, optional
        Whether to include import statements, by default True.
    namespace : str | None, optional
        DEPRECATED - Ignored, uses automatic naming from component.

    Returns
    -------
    str
        Complete .pyi stub file content as string.

    Examples
    --------
    >>> from dash import html
    >>> stub = generate_stub_for_component(html.Div)
    >>> 'class LazyComponentHtmlDiv' in stub
    True
    >>> 'class _PropsNamespaceHtmlDiv' in stub
    True
    """
    info: DashComponentInfo = get_component_info(_component_cls)

    class_name = get_lazy_component_cls_name(_component_cls)
    props_namespace_name = get_props_namespace_name(_component_cls)

    lines: list[str] = []

    if include_imports:
        lines.extend(
            [
                "from __future__ import annotations",
                "",
                "from typing import TYPE_CHECKING, Any",
                "",
                "if TYPE_CHECKING:",
                "    from dash_component_template.lazy_component import LazyComponent",
                "    from dash_component_template.template import _Template",
                "",
            ]
        )

    lines.append(f"class {props_namespace_name}:")
    lines.extend(_build_prop_attribute_lines(info))
    lines.extend(["", ""])

    lines.append(f"class {class_name}(LazyComponent):")
    lines.append("    ")
    lines.append("    @property")
    lines.append(
        f"    def props(self) -> {props_namespace_name}:  # type: ignore[override]"
    )
    lines.append("        ...")
    lines.append("    ")
    lines.append("    def __init__(  # type: ignore[no-untyped-def]")
    lines.append("        self,")
    lines.extend(_build_init_param_lines(info))
    lines.append("        *,")
    lines.append("        _parent: _Template | None = None,")
    lines.append("    ) -> None: ...")

    return "\n".join(lines) + "\n"


def write_stub_file(
    _component_cls: type[Component],
    output_dir: str | Path,
    namespace: str | None = None,
) -> Path:
    """Write type stub file for a component class.

    Creates the .pyi file in the appropriate location within output_dir,
    mirroring the component's module structure.

    Parameters
    ----------
    _component_cls : type[Component]
        Dash component class.
    output_dir : str | Path
        Base directory for stub files.
    namespace : str | None, optional
        Optional namespace prefix (e.g., 'html' for dash.html.Div).

    Returns
    -------
    Path
        Path to the created stub file.

    Examples
    --------
    >>> from dash import html
    >>> path = write_stub_file(html.Div, 'stubs/', namespace='html')
    >>> path.exists()
    True
    >>> path.name
    'html.pyi'
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    stub_content = generate_stub_for_component(_component_cls, include_imports=True)

    if namespace:
        stub_file = output_path / f"{namespace}.pyi"
    else:
        component_name = _component_cls.__name__
        stub_file = output_path / f"{component_name}.pyi"

    stub_file.write_text(stub_content)

    return stub_file


def generate_stubs_for_namespace(
    namespace_path: str,
    output_dir: str | Path = "stubs",
) -> list[Path]:
    """Generate type stubs for all components in a namespace.

    Discovers all Dash component classes in the given namespace module
    and generates a single .pyi file containing all stubs.

    Parameters
    ----------
    namespace_path : str
        Module path (e.g., 'dash.html').
    output_dir : str | Path, optional
        Directory to write stub files, by default 'stubs'.

    Returns
    -------
    list[Path]
        List of paths to created stub files.

    Examples
    --------
    >>> paths = generate_stubs_for_namespace('dash.html', 'stubs/')
    >>> len(paths) > 0
    True
    >>> any('html.pyi' in str(p) for p in paths)
    True
    """
    import importlib

    try:
        module = importlib.import_module(namespace_path)
    except ImportError as e:
        msg = f"Cannot import namespace {namespace_path}: {e}"
        raise ValueError(msg) from e

    components = []
    for name in dir(module):
        obj = getattr(module, name)
        if (
            isinstance(obj, type)
            and issubclass(obj, Component)
            and obj is not Component
        ):
            components.append((name, obj))

    if not components:
        msg = f"No Component subclasses found in {namespace_path}"
        raise ValueError(msg)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    namespace_name = namespace_path.rsplit(".", maxsplit=1)[-1]

    lines: list[str] = []

    lines.extend(
        [
            f'"""Type stubs for {namespace_path} ComponentTemplate classes.',
            "",
            "This file provides IDE autocomplete and type checking for all",
            f"{namespace_name} component templates with props namespace pattern.",
            "",
            "Auto-generated - do not edit manually.",
            '"""',
            "",
            "from __future__ import annotations",
            "",
            "import datetime",
            "from collections.abc import Sequence",
            "from typing import Any",
            "",
            "from dash_component_template.lazy_component import LazyComponent",
            "from dash_component_template.template import _Template",
            "",
            "",
        ]
    )

    for _component_name, _component_cls in sorted(components, key=lambda x: x[0]):
        stub = generate_stub_for_component(
            _component_cls,
            include_imports=False,
            namespace=namespace_name,
        )
        lines.append(stub)
        lines.append("")

    stub_file = output_path / f"{namespace_name}.pyi"
    stub_file.write_text("\n".join(lines))

    return [stub_file]


def _get_template_class_name(namespace: str, component_name: str) -> str:
    """Get template class name for a component in a given namespace.

    Parameters
    ----------
    namespace : str
        Component namespace (e.g., 'dash.html', 'dash_mantine_components').
    component_name : str
        Component class name (e.g., 'Div', 'Button').

    Returns
    -------
    str
        Template class name for use in type stubs.
    """
    if namespace in _NAMESPACE_PREFIX_MAP:
        cls_prefix, ns_prefix = _NAMESPACE_PREFIX_MAP[namespace]
        return f"{cls_prefix}{ns_prefix}{component_name}"
    prefix = "".join(word.capitalize() for word in namespace.split("_"))
    return f"ComponentTemplate{prefix}{component_name}"


def _collect_namespace_components(
    generated_namespaces: list[str],
    lines: list[str],
) -> dict[str, Any]:
    """Collect component info for each namespace to generate factory stubs.

    Parameters
    ----------
    generated_namespaces : list[str]
        List of namespace paths to process.
    lines : list[str]
        Lines list to append namespace summary to (mutated in place).

    Returns
    -------
    dict[str, Any]
        Mapping of namespace to component info dicts.
    """
    import importlib

    namespace_components: dict[str, Any] = {}
    for namespace in sorted(generated_namespaces):
        try:
            if namespace.startswith("dash."):
                module_name = namespace
                stub_name = namespace.split(".")[-1]
            else:
                module_name = namespace
                stub_name = namespace

            module = importlib.import_module(module_name)

            component_names = (
                module.__all__
                if hasattr(module, "__all__")
                else [name for name in dir(module) if not name.startswith("_")]
            )

            components = []
            for attr_name in component_names:
                try:
                    attr = getattr(module, attr_name)
                    if (
                        isinstance(attr, type)
                        and hasattr(attr, "__module__")
                        and hasattr(attr, "__name__")
                        and not attr_name.startswith("_")
                        and any(
                            hasattr(attr, prop)
                            for prop in [
                                "_prop_names",
                                "_valid_wildcard_attributes",
                                "_type",
                            ]
                        )
                    ):
                        components.append(attr_name)
                except (AttributeError, TypeError):
                    continue

            if components:
                namespace_components[namespace] = {
                    "module_name": module_name,
                    "stub_name": stub_name,
                    "components": sorted(components),
                }
                lines.append(f"- {namespace} ({len(components)} components)")

        except (ImportError, AttributeError):
            continue

    return namespace_components


def generate_factory_stub(
    output_dir: str | Path = "stubs",
    generated_namespaces: list[str] | None = None,
) -> Path:
    """Generate _component_template_factory.pyi stub file with overloads.

    Creates overloads for _LazyComponentFactory.__getitem__ that map
    component classes to their corresponding stub classes.

    Parameters
    ----------
    output_dir : str | Path, optional
        Directory containing the component stub files, by default 'stubs'.
    generated_namespaces : list[str] | None, optional
        List of namespaces for which stubs were generated.
        If None, autodiscovers from existing .pyi files.

    Returns
    -------
    Path
        Path to the generated _component_template_factory.pyi file.
    """
    output_dir = Path(output_dir)

    if generated_namespaces is None:
        generated_namespaces = []
        for stub_file in output_dir.glob("*.pyi"):
            if stub_file.stem not in ["__init__", "_component_template_factory"]:
                name = stub_file.stem
                if name in ["html", "dcc"]:
                    generated_namespaces.append(f"dash.{name}")
                else:
                    generated_namespaces.append(name)

    lines: list[str] = []
    lines.append('"""Type stubs for _LazyComponentFactory.__getitem__ method.')
    lines.append("")
    lines.append(
        "This file provides overloads for _LazyComponentFactory.__getitem__ to enable"
    )
    lines.append("IDE autocomplete for the .child[ComponentType](...) pattern.")
    lines.append("")
    lines.append("Currently supports:")

    namespace_components = _collect_namespace_components(generated_namespaces, lines)

    lines.append("")
    lines.append("Auto-generated - do not edit manually.")
    lines.append('"""')
    lines.append("")
    lines.append("from __future__ import annotations")
    lines.append("")
    lines.append("from typing import Callable, overload")
    lines.append("")

    for namespace, info in namespace_components.items():
        if namespace.startswith("dash."):
            lines.append(f"from dash import {info['stub_name']}")
        else:
            lines.append(f"import {namespace}")

    lines.append("")
    lines.append("from dash_component_template.lazy_component import LazyComponent")
    lines.append("")
    lines.append("# Import all component template stub classes")
    lines.extend(
        f"from dash_component_template.stubs.{info['stub_name']} import *"
        for info in namespace_components.values()
    )

    lines.extend(
        [
            "",
            "",
            "class _LazyComponentFactory:",
            '    """Factory for creating typed child LazyComponent instances.',
            "    ",
            "    This stub provides overloads for __getitem__ to map Dash component",
            "    classes to their corresponding LazyComponent stub classes.",
            '    """',
            "    ",
        ]
    )

    for namespace, info in namespace_components.items():
        stub_name = info["stub_name"]

        for component_name in info["components"]:
            component_path = (
                f"{stub_name}.{component_name}"
                if namespace.startswith("dash.")
                else f"{namespace}.{component_name}"
            )
            template_class = _get_template_class_name(namespace, component_name)

            lines.append("    @overload")
            lines.append(
                f"    def __getitem__("
                f"self, component_cls: type[{component_path}]"
                f") -> Callable[..., {template_class}]: ..."
            )
            lines.append("    ")

    lines.append("    # Fallback for any other component type")
    lines.append(
        "    def __getitem__("
        "self, component_cls: type) -> Callable[..., LazyComponent]: ..."
    )
    lines.append("")

    factory_stub_path = output_dir / "_component_template_factory.pyi"
    factory_stub_path.write_text("\n".join(lines))

    return factory_stub_path


def generate_all_common_stubs(
    output_dir: str | Path = "stubs",
) -> dict[str, list[Path]]:
    """Generate stubs for all common Dash namespaces.

    Generates type stubs for all namespaces defined in naming._NAMESPACE_SHORTCUTS:
    - dash.html (HTML components)
    - dash.dcc (Dash Core Components)
    - dash_table (DataTable)
    - dash_mantine_components (DMC)
    - dash_bootstrap_components (DBC)
    - dash_ag_grid (AG Grid)
    - dash_daq (DAQ components)

    Skips any namespaces that are not installed.

    Parameters
    ----------
    output_dir : str | Path, optional
        Directory to write stub files, by default 'stubs'.

    Returns
    -------
    dict[str, list[Path]]
        Dict mapping namespace to list of generated stub file paths.

    Examples
    --------
    >>> stubs = generate_all_common_stubs('stubs/')  # doctest: +SKIP
    >>> 'dash.html' in stubs  # doctest: +SKIP
    True
    """
    from .naming import _NAMESPACE_SHORTCUTS

    namespaces = [
        "dash.html",
        "dash.dcc",
    ]
    namespaces.extend(
        package_name
        for package_name in _NAMESPACE_SHORTCUTS
        if package_name not in ["html", "dcc"]
    )

    results = {}
    for namespace in namespaces:
        try:
            paths = generate_stubs_for_namespace(namespace, output_dir)
            results[namespace] = paths
        except (ImportError, ValueError):
            pass

    return results


# CLI interface for convenience
def main() -> None:
    """CLI entry point for stub generation.

    Usage:
        python -m dash_component_template.stub_generator
    """
    import sys

    if len(sys.argv) == 1:
        package_dir = Path(__file__).parent
        stubs_dir = package_dir / "stubs"

        results = generate_all_common_stubs(stubs_dir)

        generated_namespaces = list(results.keys())
        generate_factory_stub(stubs_dir, generated_namespaces)

    elif len(sys.argv) == _MIN_ARGV_ARGS:
        namespace = sys.argv[1]
        generate_stubs_for_namespace(namespace)

    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
