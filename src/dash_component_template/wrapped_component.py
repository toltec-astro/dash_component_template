"""WrappedComponent: Integrate existing Dash components into template tree.

WrappedComponent allows you to take an existing Dash component instance
and make it part of the template hierarchy. This is useful when:
- Integrating existing components
- Wrapping third-party components
- Creating template wrappers around existing component instances

The wrapper generates a hierarchical ID based on the wrapped component's
class name (e.g., 'button0' for html.Button, 'div0' for html.Div).

Examples
--------
Wrap existing component:
    >>> from dash import html
    >>> button = html.Button(id="existing-btn", children="Click")
    >>> wrapped = WrappedComponent(button)
    >>> wrapped.id  # doctest: +ELLIPSIS
    'button...'
    >>> wrapped.component.id
    'existing-btn'

Use in custom template:
    >>> class MyWidget(ComponentTemplate):  # doctest: +SKIP
    ...     def __init__(self, existing_button, _parent=None):
    ...         super().__init__(_parent=parent)
    ...         self.wrapped = WrappedComponent(existing_button, _parent=self)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast, override

from .template import _Template
from .template_idtree import TemplateIdTree

if TYPE_CHECKING:
    from dash.development.base_component import Component


class _WrappedComponentIdTree(TemplateIdTree):
    """IdTree for WrappedComponent that uses wrapped component class name for id_stem."""  # noqa: E501

    def _id_stem(self) -> str:
        """Get ID stem from wrapped component class name.

        Returns lowercase component class name (e.g., 'div', 'button').
        """
        owner = cast("WrappedComponent", self._owner)
        assert owner._materialized is not None, "WrappedComponent not initialized"
        return owner._materialized[0].__class__.__name__.lower()


class WrappedComponent(_Template):
    """Wrapper that integrates existing Dash components into template tree.

    WrappedComponent creates a tree node for an existing component instance,
    allowing it to participate in the template hierarchy without modifying
    the original component.

    The wrapped component retains its original ID and properties. The
    WrappedComponent node gets a hierarchical tree ID that can be used
    for organizing and referencing the component within the template system.

    The component is stored in _materialized for consistency with other templates.

    Attributes
    ----------
        component: Property that returns the wrapped Dash component (read-only)
        tree_id: Hierarchical tree ID for this wrapper node
    """

    # Use custom IdTree that gets id_stem from wrapped component class name
    _idtree_cls = _WrappedComponentIdTree

    def __init__(
        self,
        component: Component,
        _parent: _Template | None = None,
    ) -> None:
        """Initialize wrapped component.

        Args:
            component: The Dash component to wrap
            _parent: Optional parent node for the ID tree
        """
        super().__init__(_parent=_parent)
        self._materialized = [component]

    @property
    def component(self) -> Component:
        """Get the wrapped component.

        Returns
        -------
            Component: The wrapped Dash component instance
        """
        assert self._materialized is not None, (
            "WrappedComponent not properly initialized"
        )
        return self._materialized[0]

    @override
    def materialize(self) -> list[Component]:
        """Return the wrapped component.

        Returns the component already stored in _materialized.
        This allows consistent handling where all templates contribute
        a list of children.

        Returns
        -------
            list[Component]: List containing the wrapped component instance
        """
        assert self._materialized is not None, (
            "WrappedComponent not properly initialized"
        )
        return self._materialized

    def __repr__(self) -> str:
        """Concise representation showing tree ID and wrapped component.

        Examples
        --------
            Wrapped(id='div0', Button())
            Wrapped(id='button0', Button('Click me'))
        """
        return f"Wrapped(id='{self.id}', {self.component!r})"
