"""Naming utilities for Dash components and LazyComponents.

This module provides consistent naming transformations used throughout the codebase:
- Component class to namespace name (html.Div -> "Html")
- Component class to ID stem (html.Div -> "div")
- Component class to stub class names (html.Div -> "HtmlDiv")

All naming logic is centralized here to ensure consistency across:
- LazyComponent subclass names
- PropsNamespace class names
- ChildFactory class names (future)
- ID stem generation
- Stub file generation
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from dash.development.base_component import Component

__all__ = [
    "get_component_cls_slug",
    "get_component_id_stem",
    "get_component_name",
    "get_component_namespace",
    "get_component_stub_suffix",
    "get_lazy_component_cls_name",
    "get_props_namespace_name",
    "get_template_cls_name",
]


# Mapping for known component library module names to their short names
# This keeps naming consistent and concise
_NAMESPACE_SHORTCUTS = {
    "html": "Html",
    "dcc": "Dcc",
    "dash_table": "DashTable",
    "dash_mantine_components": "Dmc",
    "dash_bootstrap_components": "Dbc",
    "dash_ag_grid": "DashAgGrid",
    "dash_daq": "Daq",
}


def get_component_cls_slug(component_cls: type[Component]) -> str:
    """Get a human-readable slug for a component class.

    Returns the format: namespace.ComponentName (e.g., 'html.Div', 'dcc.Graph').
    Used for string representations and debugging output.

    Parameters
    ----------
    component_cls : type[Component]
        The Dash component class

    Returns
    -------
    str
        Format: 'namespace.ComponentName'

    Examples
    --------
    >>> from dash import html, dcc
    >>> get_component_cls_slug(html.Div)
    'html.Div'
    >>> get_component_cls_slug(dcc.Graph)
    'dcc.Graph'
    """
    namespace = get_component_namespace(component_cls, lowercase=True)
    name = component_cls.__name__
    return f"{namespace}.{name}"


def get_component_name(component_cls: type[Component]) -> str:
    """Get the component class name.

    Simply returns component_cls.__name__ for consistency.
    This is the base building block for other naming functions.

    Args:
        component_cls: Dash component class

    Returns
    -------
        Component class name

    Examples
    --------
        >>> from dash import html
        >>> get_component_name(html.Div)
        'Div'
        >>> get_component_name(html.A)
        'A'
        >>> get_component_name(html.H1)
        'H1'
    """
    return component_cls.__name__


def get_component_namespace(component_cls: Any, lowercase: bool = False) -> str:
    """Get the namespace for a component (e.g., 'Html', 'Dcc', 'Dmc').

    Traverses module parts backwards to find the first meaningful namespace that:
    1. Matches a shortcut (preferred), or
    2. Doesn't repeat the component name (fallback)

    Args:
        component_cls: The component class
        lowercase: If True, return lowercase snake_case (e.g., 'html', 'dcc')
                  If False (default), return PascalCase (e.g., 'Html', 'Dcc')

    Returns
    -------
        str: Namespace string (e.g., 'Html', 'Dcc', 'Dmc', 'Dbc', 'Daq', 'DashAgGrid')
             or lowercase (e.g., 'html', 'dcc', 'dmc', 'dbc', 'daq', 'dash_ag_grid')

    Examples
    --------
        >>> from dash import html, dcc
        >>> get_component_namespace(html.Div)
        'Html'
        >>> get_component_namespace(html.Div, lowercase=True)
        'html'
        >>> get_component_namespace(dcc.Graph)
        'Dcc'
        >>> get_component_namespace(dcc.Graph, lowercase=True)
        'dcc'
    """
    module_parts = component_cls.__module__.split(".")
    component_name = component_cls.__name__

    # First pass: check if any module part matches a shortcut
    for part in module_parts:
        if part in _NAMESPACE_SHORTCUTS:
            namespace = _NAMESPACE_SHORTCUTS[part]
            if lowercase:
                # Convert PascalCase to snake_case
                return _to_snake_case(namespace)
            return namespace

    # Second pass: traverse backwards to find first part that doesn't repeat component name  # noqa: E501
    for part in reversed(module_parts):
        # Skip parts that are just the component name (case-insensitive)
        if part.lower() != component_name.lower():
            # Convert snake_case or dash-case to PascalCase
            namespace = _to_pascal_case(part)
            if lowercase:
                return _to_snake_case(namespace)
            return namespace

    # Fallback: use the first part (should rarely happen)
    namespace = _to_pascal_case(module_parts[0]) if module_parts else "Unknown"
    if lowercase:
        return _to_snake_case(namespace)
    return namespace


def _to_pascal_case(s: str) -> str:
    """Convert a string to PascalCase.

    Handles snake_case, dash-case, and regular strings.

    Examples
    --------
        >>> _to_pascal_case('some_custom_lib')
        'SomeCustomLib'
        >>> _to_pascal_case('dash-components')
        'DashComponents'
        >>> _to_pascal_case('vendor')
        'Vendor'
    """
    # Replace dashes with underscores for consistent processing
    s = s.replace("-", "_")

    # Split on underscores and capitalize each part
    parts = s.split("_")
    return "".join(part.capitalize() for part in parts if part)


def _to_snake_case(s: str) -> str:
    """Convert PascalCase to snake_case.

    Examples
    --------
        >>> _to_snake_case('Html')
        'html'
        >>> _to_snake_case('DashAgGrid')
        'dash_ag_grid'
        >>> _to_snake_case('Dmc')
        'dmc'
    """
    import re

    # Insert underscore before uppercase letters that follow lowercase letters
    s = re.sub("([a-z])([A-Z])", r"\1_\2", s)
    return s.lower()


def get_component_id_stem(component_cls: type[Component]) -> str:
    """Get lowercase ID stem from component class.

    Uses the component's __name__ and lowercases it.
    This is used for auto-generating IDs like "div0", "button1", etc.

    Args:
        component_cls: Dash component class

    Returns
    -------
        Lowercase component name suitable for ID stem

    Examples
    --------
        >>> from dash import html
        >>> get_component_id_stem(html.Div)
        'div'
        >>> get_component_id_stem(html.Button)
        'button'
        >>> get_component_id_stem(html.H1)
        'h1'
        >>> get_component_id_stem(html.A)
        'a'

    Notes
    -----
        - html.Div -> "div"
        - html.Button -> "button"
        - html.A -> "a" (not "aa")
        - dmc.Container -> "container"
    """
    return get_component_name(component_cls).lower()


def get_component_stub_suffix(component_cls: type[Component]) -> str:
    """Get stub class name suffix from component class.

    Combines namespace and component name for stub class names.
    This creates unique, readable names for stub classes.

    Args:
        component_cls: Dash component class

    Returns
    -------
        Combined namespace + component name (e.g., "HtmlDiv", "DccGraph")

    Examples
    --------
        >>> from dash import html
        >>> get_component_stub_suffix(html.Div)
        'HtmlDiv'
        >>> get_component_stub_suffix(html.Button)
        'HtmlButton'
        >>> get_component_stub_suffix(html.A)
        'HtmlA'
        >>> get_component_stub_suffix(html.H1)
        'HtmlH1'

    Notes
    -----
        - html.Div -> "HtmlDiv"
        - html.Button -> "HtmlButton"
        - html.A -> "HtmlA" (not "HtmlAA")
        - dcc.Graph -> "DccGraph"
        - dmc.Button -> "DmcButton" (not "DashMantineComponentsButton")
        - dbc.Card -> "DbcCard"
        - daq.Slider -> "DaqSlider"
    """
    namespace = get_component_namespace(component_cls)
    component_name = get_component_name(component_cls)
    return f"{namespace}{component_name}"


def get_props_namespace_name(component_cls: type[Component]) -> str:
    """Get PropsNamespace class name for component.

    Creates a private class name for the props namespace stub.

    Args:
        component_cls: Dash component class

    Returns
    -------
        PropsNamespace class name (e.g., "_PropsNamespaceHtmlDiv")

    Examples
    --------
        >>> from dash import html
        >>> get_props_namespace_name(html.Div)
        '_PropsNamespaceHtmlDiv'
        >>> get_props_namespace_name(html.A)
        '_PropsNamespaceHtmlA'

    Notes
    -----
        Pattern: _PropsNamespace{Namespace}{ComponentName}
    """
    stub_suffix = get_component_stub_suffix(component_cls)
    return f"_PropsNamespace{stub_suffix}"


def get_lazy_component_cls_name(component_cls: type[Component]) -> str:
    """Get LazyComponent class name for component.

    Creates the main stub class name for LazyComponent subclasses.

    Args:
        component_cls: Dash component class

    Returns
    -------
        LazyComponent class name (e.g., "LazyComponentHtmlDiv")

    Examples
    --------
        >>> from dash import html
        >>> get_lazy_component_cls_name(html.Div)
        'LazyComponentHtmlDiv'
        >>> get_lazy_component_cls_name(html.A)
        'LazyComponentHtmlA'
        >>> get_lazy_component_cls_name(html.H1)
        'LazyComponentHtmlH1'

    Notes
    -----
        Pattern: LazyComponent{Namespace}{ComponentName}
    """
    stub_suffix = get_component_stub_suffix(component_cls)
    return f"LazyComponent{stub_suffix}"


def get_template_cls_name(template_cls: type) -> str:
    """Get qualified name for a template class.

    Uses __qualname__ to provide module-scoped name that avoids collisions
    between templates with the same name in different modules/packages.

    This is safer than using __name__ alone because:
    - __name__ = "ButtonGroup" (ambiguous across modules)
    - __qualname__ = "myapp.components.ButtonGroup" (unique within module)

    Parameters
    ----------
    template_cls : type
        Template class (typically a Template subclass)

    Returns
    -------
    str
        Qualified class name from __qualname__

    Examples
    --------
    >>> class ButtonGroup(Template):
    ...     pass
    >>> get_template_cls_name(ButtonGroup)
    'ButtonGroup'

    >>> # Nested class
    >>> class App:
    ...     class Header(Template):
    ...         pass
    >>> get_template_cls_name(App.Header)
    'App.Header'

    Notes
    -----
    __qualname__ includes the nested class path (e.g., 'Outer.Inner')
    but does NOT include the module path. This is intentional:
    - Scopes template names within a module/package
    - Avoids clashes with identically-named templates in other packages
    - Keeps names readable and not overly verbose

    For cross-module uniqueness, users should ensure template class names
    are unique within their application codebase.
    """
    return template_cls.__qualname__
