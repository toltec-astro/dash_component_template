"""Template base class with tree composition.

This module provides the Template base class that uses composition (not inheritance)
to integrate with IdTree for hierarchical ID generation. This provides clean
separation between tree structure and template logic.

Design Philosophy:
- Composition over inheritance
- Tree is internal implementation detail
- Only expose essential tree properties via proxies
- Keep template logic pure and focused
- Subclasses can customize IdTree behavior via _idtree_cls
"""

from __future__ import annotations

import itertools
import threading
from typing import TYPE_CHECKING, Any, ClassVar

# Import MATCH for callback_scope in register_callbacks
from dash import MATCH

from .template_idtree import TemplateIdTree

if TYPE_CHECKING:
    from dash.development.base_component import Component

    from .template_idtree import TemplateIdTree as TemplateIdTreeType

__all__ = ["Template"]


class callback_scope:
    """Context manager for controlling callback scope.

    Provides a user-friendly API for setting callback scope using template
    instances, template classes, or pattern-matching markers (MATCH, ALL).

    The scope controls which component IDs match in pattern-matching callbacks:
    - Instance scope: Match only one template instance
    - Class scope: Match all instances of a template class
    - Cross-template scope: Match components across different template classes

    Parameters
    ----------
    template : Template instance, MATCH, or ALL, optional
        Template instance to scope to, or MATCH/ALL for multiple instances.
        Internally converted to _template_id in the scope dict.
    template_cls : Template class type, MATCH, or ALL, optional
        Template class to scope to, or MATCH/ALL for multiple classes.
        Internally converted to _template_name in the scope dict.
    **extra_scope
        Additional key-value pairs to merge into component IDs

    Examples
    --------
    Instance-scoped callback (using template instance):

    >>> template = ButtonGroup()
    >>> with callback_scope(template=template):
    ...     @app.callback(
    ...         Output(template.display({"index": MATCH}), "children"),
    ...         Input(template.button({"index": MATCH}), "n_clicks")
    ...     )
    ...     def update(n):
    ...         return f"Clicked {n}"

    Class-scoped callback (using MATCH for all instances):

    >>> with callback_scope(template=MATCH, template_cls=ButtonGroup):
    ...     @app.callback(
    ...         Output(first.display({"index": MATCH}), "children"),
    ...         Input(first.button({"index": MATCH}), "n_clicks")
    ...     )
    ...     def update_all(n):
    ...         return f"Clicked {n} (any instance)"

    Aggregate callback with ALL:

    >>> with callback_scope(template=ALL, template_cls=ButtonGroup):
    ...     @app.callback(
    ...         Output("summary", "children"),
    ...         Input(first.button({"index": 0}), "n_clicks")
    ...     )
    ...     def aggregate(all_clicks):
    ...         return f"Total: {sum(c for c in all_clicks if c)}"

    Cross-template callback (match any template class):

    >>> with callback_scope(template=MATCH, template_cls=MATCH):
    ...     @app.callback(
    ...         Output("global-summary", "children"),
    ...         Input(first.button({"index": ALL}), "n_clicks")
    ...     )
    ...     def aggregate_all(all_clicks):
    ...         return f"Global total: {sum(c for c in all_clicks if c)}"

    Using raw keys (advanced):

    >>> with callback_scope(_template_name="ButtonGroup", _template_id=MATCH):
    ...     # Equivalent to: callback_scope(template=MATCH, template_cls=ButtonGroup)
    ...     pass

    Notes
    -----
    - Scopes are stackable - inner scopes override outer scopes
    - register_callbacks() automatically sets instance scope
    - Use this for class-level or cross-template callbacks
    - The scope dict is merged into IDs by LazyComponent.__call__()
    - Template names use __qualname__ to avoid cross-package collisions
    """

    def __init__(
        self,
        *,
        template: _Template | type[_Template] | Any = None,
        template_cls: type[_Template] | Any = None,
        **extra_scope: Any,
    ) -> None:
        """Initialize callback scope with template-based or raw parameters.

        Parameters
        ----------
        template : Template instance, MATCH, or ALL, optional
            Template instance to scope to, or MATCH/ALL for pattern-matching
        template_cls : Template class, MATCH, or ALL, optional
            Template class to scope to, or MATCH/ALL for pattern-matching
        **extra_scope
            Additional scope keys (can use _template_name, _template_id directly)
        """
        from .naming import get_template_cls_name

        scope: dict[str, Any] = {}

        # Handle template parameter (-> _template_id)
        if template is not None:
            if isinstance(template, _Template):
                # Template instance: use its ID
                scope["_template_id"] = template.id
            else:
                # MATCH, ALL, or other marker: use as-is
                scope["_template_id"] = template

        # Handle template_cls parameter (-> _template_name)
        if template_cls is not None:
            if isinstance(template_cls, type) and issubclass(template_cls, _Template):
                # Template class: use qualified name
                scope["_template_name"] = get_template_cls_name(template_cls)
            else:
                # MATCH, ALL, or other marker: use as-is
                scope["_template_name"] = template_cls

        # Merge extra scope keys (allows raw _template_name, _template_id, etc.)
        scope.update(extra_scope)

        self._scope = scope

    def __enter__(self) -> None:
        """Push scope onto thread-local stack."""
        # Initialize stack if needed
        if not hasattr(_Template._callback_scope, "stack"):
            _Template._callback_scope.stack = []

        # Push this scope onto stack
        _Template._callback_scope.stack.append(self._scope)

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:  # noqa: PYI036
        """Pop scope from thread-local stack."""
        if (
            hasattr(_Template._callback_scope, "stack")
            and _Template._callback_scope.stack
        ):
            _Template._callback_scope.stack.pop()


def _get_current_scope() -> dict[str, Any]:
    """Get the current callback scope by merging all scopes in the stack.

    Returns the merged scope dict from all active callback_scope contexts.
    Outer scopes are applied first, inner scopes override.

    Returns
    -------
    dict[str, Any]
        Merged scope dict from all active contexts
    """
    if (
        not hasattr(_Template._callback_scope, "stack")
        or not _Template._callback_scope.stack
    ):
        return {}

    # Merge all scopes in stack order (later scopes override earlier)
    merged = {}
    for scope in _Template._callback_scope.stack:
        merged.update(scope)

    return merged


class _Template:
    """Abstract base class for Dash component templates with hierarchical IDs.

    _Template provides the core tree-based organization for Dash components with
    automatic hierarchical ID generation. It is the foundation for concrete template
    implementations like Template (transparent container) and ComponentTemplate
    (single component proxy).

    This class handles:
    - Automatic hierarchical ID generation (e.g., 'parent-child-grandchild')
    - Parent-child relationships with automatic ID updates on reparenting
    - Counter reset for testing and multi-app scenarios

    Subclasses must implement their own materialize() method with appropriate
    return types for their use case.
    """

    # Private class variable: IdTree subclass to use for this template type
    _idtree_cls: ClassVar[type[TemplateIdTreeType]] = TemplateIdTree

    # Class-level callback registration cache (per app)
    # Maps app_id -> set of template classes that have registered class callbacks
    # This prevents duplicate registration of class-level callbacks
    _class_callbacks_registered: ClassVar[dict[int, set[type]]] = {}
    _class_callbacks_registration_lock: ClassVar[threading.Lock] = threading.Lock()

    # Thread-local storage for callback scope stack
    # Each level is a dict that gets merged into component IDs
    _callback_scope: ClassVar[threading.local] = threading.local()

    def __init__(self, _parent: _Template | None = None) -> None:
        """Initialize template with tree composition.

        Parameters
        ----------
        _parent : Template, optional
            Parent template for tree hierarchy (internal parameter)
        """
        # Create tree node using the class's _idtree_cls
        # This allows subclasses to customize IdTree behavior
        parent_tree = _parent._tree if _parent else None
        self._tree = self._idtree_cls(owner=self, parent=parent_tree)

        # Initialize materialization state
        self._materialized: list[Component] | None = None

    @classmethod
    def reset_counter(cls) -> None:
        """Reset instance counter for this specific template class.

        This is useful for testing to ensure predictable IDs.
        Only resets the counter for this class, not all classes.

        Examples
        --------
        >>> t1 = Template()
        >>> t2 = Template()
        >>> Template.reset_counter()
        >>> t3 = Template()  # Starts from 0 again
        """
        from .idtree import IdTree

        # Reset counter for the IdTree class this template uses
        # The counter is keyed by the IdTree class name, not the template class name
        idtree_cls_name = cls._idtree_cls.__name__
        IdTree._class_counters[idtree_cls_name] = itertools.count()

    @classmethod
    def reset_class_state(cls, app: Any = None) -> None:
        """Reset all class-level state for templates.

        This is a convenience method that resets:
        - Instance counters (for predictable IDs)
        - Callback registration cache
        - Callback scope stack (current thread)

        Useful for testing and hot reload scenarios.

        Parameters
        ----------
        app : Dash, optional
            If provided, only reset callback registry for this specific app.
            If None, reset callback registry for all apps.

        Examples
        --------
        Reset everything for testing:

        >>> _Template.reset_class_state()

        Reset for specific app (hot reload):

        >>> _Template.reset_class_state(app)

        Notes
        -----
        - Calls reset_counter(), reset_callback_registry(app),
          and reset_callback_scope()
        - Thread-safe for callback registry operations
        - Callback scope reset only affects current thread
        """
        cls.reset_counter()
        cls.reset_callback_registry(app)
        cls.reset_callback_scope()

    @classmethod
    def reset_callback_registry(cls, app: Any = None) -> None:
        """Reset class-level callback registration cache.

        This is useful for hot reload scenarios where callback registration
        should be repeated with the new code.

        Parameters
        ----------
        app : Dash, optional
            If provided, only reset cache for this specific app.
            If None, reset cache for all apps.

        Examples
        --------
        Reset for specific app:

        >>> _Template.reset_callback_registry(app)

        Reset for all apps (hot reload scenario):

        >>> _Template.reset_callback_registry()

        Notes
        -----
        - Called automatically is typically not needed in normal usage
        - Useful when using Dash dev tools with hot reload
        - Thread-safe operation
        """
        with cls._class_callbacks_registration_lock:
            if app is None:
                # Reset all apps
                cls._class_callbacks_registered.clear()
            else:
                # Reset specific app
                app_id = id(app)
                cls._class_callbacks_registered.pop(app_id, None)

    @classmethod
    def reset_callback_scope(cls) -> None:
        """Reset callback scope stack for current thread.

        This clears the thread-local callback scope stack. Useful for testing
        or when recovering from errors that may have left the stack in an
        inconsistent state.

        Examples
        --------
        >>> _Template.reset_callback_scope()

        Notes
        -----
        - Only affects the current thread
        - Automatically called on exception in callback_scope.__exit__
        - Rarely needed in normal usage
        """
        if hasattr(cls._callback_scope, "stack"):
            cls._callback_scope.stack.clear()

    @property
    def id(self) -> str:
        """Get hierarchical ID from tree.

        Returns
        -------
        str
            Hierarchical ID like "parent-child-grandchild"

        Examples
        --------
        >>> template = Template()
        >>> template.id  # doctest: +ELLIPSIS
        'template...'
        >>> child = Template(_parent=template)
        >>> child.id  # doctest: +ELLIPSIS
        'template...-template...'

        Notes
        -----
        This is a proxy to self._tree.id for clean API.
        """
        return self._tree.id

    @property
    def children(self) -> tuple[_Template, ...]:
        """Get tuple of child templates.

        Returns
        -------
        tuple[_Template, ...]
            Tuple of child templates attached to this template

        Examples
        --------
        >>> parent = Template()
        >>> child1 = Template(_parent=parent)
        >>> child2 = Template(_parent=parent)
        >>> len(parent.children)
        2
        >>> child1 in parent.children
        True

        Notes
        -----
        This traverses the tree structure and returns templates, not tree nodes.
        """
        return tuple(
            child._owner for child in self._tree.children if hasattr(child, "_owner")
        )

    @property
    def parent(self) -> _Template | None:
        """Get parent template in tree.

        Returns
        -------
        _Template or None
            Parent template or None for root templates

        Examples
        --------
        >>> parent = Template()
        >>> child = Template(_parent=parent)
        >>> child.parent is parent
        True
        >>> parent.parent is None
        True
        """
        tree_parent = self._tree.parent
        if tree_parent and hasattr(tree_parent, "_owner"):
            return tree_parent._owner
        return None

    @parent.setter
    def parent(self, value: _Template | None) -> None:
        """Set parent template in tree (reparenting).

        This provides a simple semantic for moving templates in the tree.
        Setting parent automatically updates the tree structure.

        Parameters
        ----------
        value : _Template or None
            New parent template or None to make this a root

        Examples
        --------
        >>> parent1 = Template()
        >>> parent2 = Template()
        >>> child = Template(_parent=parent1)
        >>> child.parent is parent1
        True
        >>> child.parent = parent2  # Reparent
        >>> child.parent is parent2
        True
        >>> child.id  # ID updates automatically
        'template1-template2'
        """
        self._tree.parent = value._tree if value else None

    @property
    def child(self):
        """Get child component factory.

        Returns factory object that supports template.child[Type](...) syntax.
        The factory creates LazyComponent instances with parent pre-bound.

        Returns
        -------
        _LazyComponentFactory
            Factory for creating child component templates
        """
        from .lazy_component import _LazyComponentFactory

        return _LazyComponentFactory(owner=self)

    def materialize(self) -> list[Component]:
        """Create Dash component(s) from template.

        Default implementation: recursively materializes all children and flattens
        results into a single list. Subclasses can override for specialized behavior
        (e.g., LazyComponent creates actual Dash components).

        All templates return a list representing the children they contribute.
        Virtual templates (no component) naturally return empty list or their
        children's components, flattened.

        Returns
        -------
        list[Component]
            List of materialized Dash components (empty list if no output)

        Examples
        --------
        >>> from dash import html
        >>> from dash_component_template import Template
        >>> # Virtual template flattens children
        >>> root = Template()
        >>> div1 = root.child[html.Div](children="First")
        >>> div2 = root.child[html.Div](children="Second")
        >>> components = root.materialize()
        >>> len(components)
        2
        >>> [c.children for c in components]
        [['First'], ['Second']]
        """
        if not self.children:
            self._materialized = []
            return []

        # Collect all materialized children
        materialized: list[Component] = []
        for child in self.children:
            result = child.materialize()
            # All children return list[Component], so extend
            materialized.extend(result)

        # Store for debugging/introspection
        self._materialized = materialized
        return materialized

    @property
    def materialized(self) -> list[Component] | None:
        """Get the result from the most recent materialize() call.

        Returns None if materialize() has never been called on this template.
        Useful for debugging, introspection, and walking the materialized
        component tree.

        Returns
        -------
        list[Component] | None
            List of materialized Dash components from the last materialize() call,
            or None if materialize() has not been called yet

        Examples
        --------
        >>> from dash import html
        >>> from dash_component_template import Template
        >>> root = Template()
        >>> div = root.child[html.Div](children="Test")
        >>> root.materialized is None  # Before materialization
        True
        >>> components = root.materialize()
        >>> root.materialized is not None  # After materialization
        True
        >>> len(root.materialized)
        1

        Notes
        -----
        This property stores the LAST materialization result. If you call
        materialize() multiple times, this will reflect the most recent call.
        """
        return self._materialized

    def layout(self) -> Component:
        """Return single Dash component suitable for app.layout.

        Materializes the template tree to create Dash components, then
        unwraps the result
        into a single component suitable for assignment to app.layout.

        This method creates fresh components each time it's called, making it compatible
        with Dash hot reload when used with a function:
        ``app.layout = lambda: template.layout()``

        Returns
        -------
        Component
            Single Dash component suitable for app.layout

        Raises
        ------
        ValueError
            If materialize() returns empty list or more than one component

        Examples
        --------
        >>> from dash import html
        >>> from dash_component_template import Template
        >>> root = Template()
        >>> div = root.child[html.Div]()
        >>> component = div.layout()
        >>> type(component).__name__
        'Div'

        Notes
        -----
        This is a convenience method for getting a component to assign to app.layout:
            app.layout = my_template.layout()

        The method ensures that exactly one component is returned. If your template
        materializes to multiple components or no components, you'll get a ValueError.

        Template construction should happen in __init__:
            class MyTemplate(Template):
                def __init__(self):
                    super().__init__()
                    self.div = self.child[html.Div](children="Hello")
        """
        result = self.materialize()

        if len(result) == 0:
            msg = (
                f"Cannot create layout: {self.__class__.__name__}.materialize() returned empty list. "  # noqa: E501
                "The layout() method requires exactly one component for app.layout assignment."  # noqa: E501
            )
            raise ValueError(
                msg,
            )
        if len(result) > 1:
            msg = (
                f"Cannot create layout: {self.__class__.__name__}.materialize() returned {len(result)} components. "  # noqa: E501
                "The layout() method requires exactly one component for app.layout assignment. "  # noqa: E501
                "Consider wrapping multiple components in a container (e.g., html.Div)."
            )
            raise ValueError(
                msg,
            )

        return result[0]

    def setup_callbacks(self, app: Any) -> None:
        """Override this method to define Dash callbacks for this template.

        This method is called by register_callbacks() and provides full access
        to self and all component IDs with IDE autocomplete support.

        Use standard @app.callback decorator to define callbacks. Separate
        business logic into testable methods.

        Parameters
        ----------
        app : Dash
            The Dash application instance

        Examples
        --------
        >>> from dash import html, Input, Output
        >>> from dash_component_template import Template
        >>> class CounterTemplate(Template):
        ...     def __init__(self, factor=2.0):
        ...         super().__init__()
        ...         self._factor = factor
        ...         self.button = self.child[html.Button](children="Click", n_clicks=0)
        ...         self.display = self.child[html.Div]()
        ...
        ...     def update_counter(self, n_clicks):
        ...         return f"Count: {n_clicks * self._factor}"
        ...
        ...     def setup_callbacks(self, app):
        ...         @app.callback(
        ...             Output(self.display.id, "children"),
        ...             Input(self.button.id, "n_clicks")
        ...         )
        ...         def callback(n_clicks):
        ...             return self.update_counter(n_clicks)

        Notes
        -----
        - Override this method in your template subclass
        - Use standard @app.callback decorator - no special wrappers needed
        - Access component IDs via self.component_name.id (full type safety!)
        - Separate business logic into testable methods
        - Called automatically by register_callbacks(app)
        """
        # Subclasses override to define callbacks

    @classmethod
    def setup_class_callbacks(cls, instance: _Template, app: Any) -> None:
        """Override this method to define class-level callbacks across all instances.

        This method is called once per template class during callback registration
        and allows you to define callbacks that work across multiple instances of
        the same template class using pattern-matching.

        The callback_scope is AUTOMATICALLY set to (template=MATCH, template_cls=cls),
        so you can directly define callbacks without wrapping them
        for the MATCH pattern.
        Only use callback_scope() explicitly if you need the ALL pattern.

        Parameters
        ----------
        instance : _Template
            An instance of this template class, used to access component structure
        app : Dash
            The Dash application instance

        Examples
        --------
        Class-scoped callback (automatic MATCH scope, no wrapper needed):

        >>> from dash import html, Input, Output, MATCH
        >>> from dash_component_template import Template
        >>> class ButtonGroup(Template):
        ...     def __init__(self):
        ...         super().__init__()
        ...         self.button = self.child[html.Button](children="Click")
        ...         self.display = self.child[html.Div]()
        ...
        ...     @classmethod
        ...     def setup_class_callbacks(cls, instance, app):
        ...         # No callback_scope needed! Automatically set to MATCH
        ...         @app.callback(
        ...             Output(instance.display({"index": MATCH}), "children"),
        ...             Input(instance.button({"index": MATCH}), "n_clicks")
        ...         )
        ...         def update_all_instances(n):
        ...             return f"Clicked {n} times (any instance)"

        Aggregate callback using ALL pattern (explicit scope override):

        >>> @classmethod
        ... def setup_class_callbacks(cls, instance, app):
        ...     # For ALL pattern, override with callback_scope explicitly
        ...     from dash_component_template import callback_scope
        ...     from dash import ALL
        ...     with callback_scope(template=ALL, template_cls=cls):
        ...         @app.callback(
        ...             Output("total-display", "children"),
        ...             Input(instance.button({"index": ALL}), "n_clicks")
        ...         )
        ...         def aggregate(all_clicks):
        ...             return f"Total: {sum(all_clicks)}"

        Notes
        -----
        - Override this method in your template subclass
        - Called once per class per app during register_callbacks()
        - Callback scope AUTOMATICALLY set to (template=MATCH, template_cls=cls)
        - For MATCH pattern: define callbacks directly (no wrapper needed)
        - For ALL pattern: use callback_scope(template=ALL, template_cls=cls)
        - The instance parameter provides access to component structure
        - First instance encountered triggers class callback registration
        """
        # Subclasses override to define class-level callbacks

    def register_callbacks(self, app: Any) -> None:
        """Register all callbacks for this template and its children.

        This is the public API for callback registration. It:
        1. Calls setup_callbacks() for this template (instance-level)
        2. Calls setup_class_callbacks() once per template class (class-level)
        3. Recursively registers callbacks for all child templates

        Class-level callbacks are registered once per class (on first instance
        encountered), using the first instance for component structure access.

        This method automatically sets instance-level callback scope, so that
        LazyComponent.__call__() injects _template_name and _template_id to ensure
        callbacks are scoped to the template instance that defines them.

        Parameters
        ----------
        app : Dash
            The Dash application instance

        Examples
        --------
        >>> from dash import Dash, html
        >>> from dash_component_template import Template
        >>> app = Dash(__name__)
        >>> template = CounterTemplate(factor=2.0)
        >>> app.layout = html.Div([template.layout()])
        >>> template.register_callbacks(app)
        >>> app.run(debug=True)

        Notes
        -----
        - Call this AFTER adding the template to app.layout
        - Automatically handles nested templates with callbacks
        - Automatically sets instance-level scope for callbacks
        - Class-level callbacks are registered once per class per app
        - Registration cache is thread-safe and stored in _Template class
        - For hot reload: use _Template.reset_callback_registry(app)
        - Use callback_scope() context manager for custom scoping
        """
        # Set instance-level callback scope automatically using new API
        # This is equivalent to: callback_scope(_template_name=..., _template_id=...)
        # but uses the user-friendly template/template_cls parameters
        with callback_scope(template=self, template_cls=type(self)):
            # Setup callbacks for this template
            self.setup_callbacks(app)

        # Setup class-level callbacks once per template class per app
        # Use class variable with thread-safe access instead of polluting app object
        template_cls = type(self)
        app_id = id(app)

        with _Template._class_callbacks_registration_lock:
            # Get or create the set of registered classes for this app
            if app_id not in _Template._class_callbacks_registered:
                _Template._class_callbacks_registered[app_id] = set()

            registered_classes = _Template._class_callbacks_registered[app_id]

            if template_cls not in registered_classes:
                registered_classes.add(template_cls)
                # Release lock before calling setup_class_callbacks
                # (callbacks may take time and don't need lock protection)
                should_register = True
            else:
                should_register = False

        if should_register:
            # Automatically set class-level scope for setup_class_callbacks
            # Users don't need to manually wrap with callback_scope()
            with callback_scope(template=MATCH, template_cls=template_cls):
                # Call with this instance for component structure access
                template_cls.setup_class_callbacks(self, app)

        # Recursively register callbacks for all child templates
        # Each child will set its own scope when its register_callbacks is called
        for child in self.children:
            child.register_callbacks(app)

    def __repr__(self) -> str:
        """Return string representation.

        Returns
        -------
        str
            Representation showing class name and tree ID

        Examples
        --------
        >>> template = Template()
        >>> repr(template)  # doctest: +ELLIPSIS
        "Template('template...')"
        """
        return f"{self.__class__.__name__}('{self.id}')"


class Template(_Template):
    """Virtual template for organizing layout structure and callbacks.

    Template is a "virtual" node in the template tree - it has no component
    class and materializes only its children. Use this when you need to:

    1. Organize related components into a logical group
    2. Define reusable callback patterns
    3. Create a root container for your layout tree

    Templates are transparent during materialization - they pass through their
    children's components without adding an extra wrapper layer.

    Examples
    --------
    >>> from dash import html
    >>> from dash_component_template import Template
    >>> # Virtual template as logical grouping
    >>> class NavBar(Template):
    ...     def __init__(self):
    ...         super().__init__()
    ...         self.child[html.Div](children="Logo", className="logo")
    ...         self.child[html.Div](children="Menu", className="menu")
    >>> navbar = NavBar()
    >>> components = navbar.materialize()
    >>> len(components)  # Two divs, no wrapper
    2

    Notes
    -----
    Template inherits the default materialize() implementation from _Template,
    which recursively flattens all children. No override needed.

    Custom templates should define their structure in __init__:
        class MyTemplate(Template):
            def __init__(self, title: str = "Default"):
                super().__init__()
                self.header = self.child[html.H1](children=title)
    """
