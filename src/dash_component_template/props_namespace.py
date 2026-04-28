"""Props namespace for isolating Dash component properties.

This module provides the PropsNamespace class that isolates all Dash component
properties in a separate namespace, preventing conflicts with user attributes
and enabling wildcard property support (data-*, aria-*).
"""

from collections.abc import Iterator
from typing import Any


def _deep_merge(base: dict[str, Any], updates: dict[str, Any]) -> None:
    """Recursively merge updates into base dict (in-place).

    For nested dicts, merges recursively. For other values, replaces.

    Args:
        base: Dictionary to update (modified in-place)
        updates: Dictionary with updates to apply
    """
    for key, value in updates.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


class _PropsNamespace:
    """Namespace for Dash component properties.

    Minimal dict-like interface that avoids method name conflicts with Dash properties.
    Only uses dunder methods and delegates batch operations to template methods.

    For batch updates, use:
        - template.props_update() for shallow merge
        - template.props_rupdate() for deep recursive merge
        - template.props_dict() to get all props as dict

    Properties are stored in an internal dict for simplicity and clarity.

    Important: None is a valid property value. To check if a property is set,
    use the 'in' operator, not a None check:
        if "className" in props:  # Correct
        if props["className"] is not None:  # Wrong - className could be explicitly None

    Examples
    --------
        # Attribute-style access
        props.className = "container"
        props.style = {"padding": "10px"}
        props.disabled = None  # None is a valid value

        # Dict-style access (required for wildcards)
        props["data-testid"] = "my-component"
        props["aria-label"] = "Interactive element"

        # Delete properties
        del props.className  # Attribute-style deletion
        del props["data-testid"]  # Dict-style deletion

        # Check if property is set (use 'in', not None check)
        if "className" in props:
            print(props["className"])  # Could be None!

        # Accessing missing property raises error
        try:
            value = props.missing_key  # Raises AttributeError
        except AttributeError:
            value = "default"

        # Iterate over set properties
        for key in props:  # Iterate over keys
            print(f"{key}: {props[key]}")
    """

    __slots__ = ("_data",)

    def __init__(self, **props: Any) -> None:
        """Initialize props namespace.

        Args:
            **props: Initial properties to set
        """
        self._data = props

    def __setattr__(self, name: str, value: Any) -> None:
        """Set property via attribute access.

        Args:
            name: Property name (e.g., 'className')
            value: Property value
        """
        if name == "_data":
            object.__setattr__(self, name, value)
        else:
            self._data[name] = value

    def __getattr__(self, name: str) -> Any:
        """Get property via attribute access.

        Args:
            name: Property name (e.g., 'className')

        Returns
        -------
            Property value (can be None if explicitly set to None)

        Raises
        ------
        AttributeError
            If property has not been set
        """
        if name not in self._data:
            raise AttributeError(
                f"Property '{name}' has not been set. "
                f"Use 'in' to check if a property exists: if '{name}' in props"
            )
        return self._data[name]

    def __delattr__(self, name: str) -> None:
        """Delete property via attribute access.

        Args:
            name: Property name (e.g., 'className')

        Raises
        ------
        AttributeError
            If property has not been set
        """
        if name == "_data":
            raise AttributeError("Cannot delete internal _data attribute")
        if name not in self._data:
            raise AttributeError(
                f"Property '{name}' has not been set. "
                f"Cannot delete a property that doesn't exist."
            )
        del self._data[name]

    def __setitem__(self, key: str, value: Any) -> None:
        """Set property via dict-style access.

        This is the only way to set wildcard properties like 'data-testid'.

        Args:
            key: Property name (can include hyphens)
            value: Property value
        """
        self._data[key] = value

    def __getitem__(self, key: str) -> Any:
        """Get property via dict-style access.

        Args:
            key: Property name (can include hyphens)

        Returns
        -------
            Property value (can be None if explicitly set to None)

        Raises
        ------
        KeyError
            If property has not been set
        """
        if key not in self._data:
            raise KeyError(
                f"Property '{key}' has not been set. "
                f"Use 'in' to check if a property exists: if '{key}' in props"
            )
        return self._data[key]

    def __delitem__(self, key: str) -> None:
        """Delete property via dict-style access.

        Args:
            key: Property name (can include hyphens)

        Raises
        ------
        KeyError
            If property has not been set
        """
        if key not in self._data:
            raise KeyError(
                f"Property '{key}' has not been set. "
                f"Cannot delete a property that doesn't exist."
            )
        del self._data[key]

    def __contains__(self, key: str) -> bool:
        """Check if property is set.

        Args:
            key: Property name

        Returns
        -------
            True if property has been set (even if None)
        """
        return key in self._data

    def __iter__(self) -> Iterator[str]:
        """Iterate over property names.

        Yields
        ------
            Property names
        """
        return iter(self._data)

    def __len__(self) -> int:
        """Get number of set properties.

        Returns
        -------
            Count of properties that have been set
        """
        return len(self._data)

    def __repr__(self) -> str:
        """Get string representation.

        Returns
        -------
            String showing all set properties
        """
        items = ", ".join(f"{k}={v!r}" for k, v in self._data.items())
        return f"_PropsNamespace({{{items}}})"
