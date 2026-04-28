"""Component introspection and metadata management.

This module provides tools for extracting metadata from Dash component classes
through introspection. The main entry point is `get_component_info()`, which
returns a cached `DashComponentInfo` dataclass containing property names,
defaults, and type annotations.

Example:
    >>> from dash import html
    >>> info = get_component_info(html.Div)
    >>> 'className' in info.prop_names
    True
"""

from __future__ import annotations

import functools
import inspect
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, get_type_hints

if TYPE_CHECKING:
    from dash.development.base_component import Component


@dataclass(frozen=True, slots=True)
class DashComponentInfo:
    """Metadata about a Dash component class extracted via introspection.

    This is a frozen dataclass for immutability and performance (slots).
    Cached globally to avoid repeated introspection.

    Attributes
    ----------
        component_cls: The Dash component class (e.g., html.Div)
        prop_names: Ordered tuple of property names from __init__ signature
        prop_defaults: Default values for properties
        prop_annotations: Type annotations for properties
        required_props: Frozenset of required property names (no defaults)

    Example:
        >>> from dash import html
        >>> info = DashComponentInfo.from_component_cls(html.Div)
        >>> 'className' in info.prop_names
        True
        >>> 'className' in info.required_props
        False
    """

    component_cls: type[Component]
    prop_names: tuple[str, ...]
    prop_defaults: dict[str, Any] = field(default_factory=dict)
    prop_annotations: dict[str, Any] = field(default_factory=dict)
    required_props: frozenset[str] = field(default_factory=frozenset)

    @classmethod
    def from_component_cls(cls, component_cls: type[Component]) -> DashComponentInfo:
        """Introspect component class and extract metadata.

        Uses `inspect.signature()` to extract parameter information from the
        component's `__init__` method. Handles type hints properly using
        `get_type_hints()` for forward references.

        Args:
            component_cls: Dash component class to introspect

        Returns
        -------
            DashComponentInfo with extracted metadata

        Raises
        ------
            ValueError: If component class cannot be introspected

        Example:
            >>> from dash import html
            >>> info = DashComponentInfo.from_component_cls(html.Div)
            >>> info.component_cls is html.Div
            True
            >>> len(info.prop_names) > 0
            True
        """
        # Get signature
        try:
            sig = inspect.signature(component_cls.__init__)
        except (ValueError, TypeError) as e:
            msg = f"Cannot introspect {component_cls.__name__}.__init__: {e}"
            raise ValueError(
                msg,
            ) from e

        # Extract property info
        prop_names = []
        prop_defaults = {}
        prop_annotations = {}
        required_props = set()

        # Get type hints (handles string annotations)
        try:
            type_hints = get_type_hints(component_cls.__init__)
        except Exception:  # noqa: BLE001 - get_type_hints can raise many error types
            # Some components may not have proper type hints
            type_hints = {}

        for name, param in sig.parameters.items():
            # Skip self, *args, **kwargs
            if name in ("self", "args", "kwargs") or param.kind in (
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            ):
                continue

            prop_names.append(name)

            # Default value
            if param.default is not inspect.Parameter.empty:
                prop_defaults[name] = param.default
            else:
                required_props.add(name)

            # Type annotation
            if name in type_hints:
                prop_annotations[name] = type_hints[name]
            elif param.annotation is not inspect.Parameter.empty:
                prop_annotations[name] = param.annotation

        return cls(
            component_cls=component_cls,
            prop_names=tuple(prop_names),  # Immutable
            prop_defaults=prop_defaults,
            prop_annotations=prop_annotations,
            required_props=frozenset(required_props),  # Immutable
        )

    def __repr__(self) -> str:
        """Clean repr for debugging.

        Example:
            >>> from dash import html
            >>> info = DashComponentInfo.from_component_cls(html.Div)
            >>> 'Div' in repr(info)
            True
        """
        return (
            f"DashComponentInfo("
            f"component_cls={self.component_cls.__name__}, "
            f"props={len(self.prop_names)})"
        )


# Global cache with LRU eviction
@functools.cache
def get_component_info(component_cls: type[Component]) -> DashComponentInfo:
    """Get cached component info.

    This is the main entry point for component introspection.
    Results are cached indefinitely for performance.

    The cache size of 256 is more than sufficient for typical Dash apps,
    which rarely use more than 50-100 different component types.

    Args:
        component_cls: Dash component class

    Returns
    -------
        Cached DashComponentInfo instance

    Example:
        >>> from dash import html
        >>> info = get_component_info(html.Div)
        >>> 'className' in info.prop_names
        True
        >>> info2 = get_component_info(html.Div)
        >>> info is info2  # Same cached object
        True
    """
    return DashComponentInfo.from_component_cls(component_cls)


def clear_component_info_cache() -> None:
    """Clear the component info cache.

    Useful for testing or dynamic component modification scenarios.
    In normal usage, you should never need to call this.

    Example:
        >>> from dash import html
        >>> _ = get_component_info(html.Div)
        >>> clear_component_info_cache()
        >>> # Cache is cleared, next call will re-introspect
    """
    get_component_info.cache_clear()
