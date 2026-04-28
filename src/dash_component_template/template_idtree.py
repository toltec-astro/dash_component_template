"""TemplateIdTree - IdTree subclass for Template composition pattern.

This module provides TemplateIdTree, which extends IdTree with template-specific
features needed for the composition pattern:

1. Owner management: Bidirectional link between tree and template
2. Owner-based id_base: Uses owner's class name instead of tree's class name
3. Clean initialization: Sets up owner relationship in __init__

Design Philosophy:
- Extend IdTree without modifying it
- Template owns the tree, tree knows its owner
- id_base computation uses owner's class for clarity
- Specialized subclasses (NullIdTree) handle custom ID behaviors
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .idtree import IdTree

if TYPE_CHECKING:
    from .template import _Template

__all__ = ["TemplateIdTree"]


class TemplateIdTree(IdTree):
    """IdTree subclass designed for Template composition pattern.

    TemplateIdTree extends IdTree to support the composition pattern where
    Template owns an IdTree but wants the tree's id_base to use the Template's
    class name rather than "idtree".

    Key Features:
    - Bidirectional owner link: tree._owner → _Template instance
    - Owner-based id_base: Uses owner.__class__.__name__ for clarity
    - Clean API: Owner set in __init__, no manual setup needed

    Parameters
    ----------
    owner : _Template
        The template instance that owns this tree node
    parent : TemplateIdTree, optional
        Parent tree node (should be owner.parent._tree if owner has parent)

    Examples
    --------
    >>> from dash_component_template.template import Template
    >>> class MyTemplate(Template):
    ...     pass
    >>> template = MyTemplate()
    >>> template._tree.id_base  # doctest: +ELLIPSIS
    'mytemplate...'
    >>> template._tree._owner is template
    True

    Notes
    -----
    This class is internal implementation detail. Users interact with Template,
    which creates and manages TemplateIdTree instances automatically.
    """

    def __init__(
        self,
        owner: _Template,
        parent: TemplateIdTree | None = None,
    ) -> None:
        """Initialize tree node with owner relationship.

        Parameters
        ----------
        owner : _Template
            The template instance that owns this tree node
        parent : TemplateIdTree, optional
            Parent tree node in hierarchy
        """
        # Store owner reference (bidirectional link)
        self._owner: _Template = owner

        # Initialize IdTree with parent (IdTree uses parent= parameter)
        super().__init__(parent=parent)

    def _id_stem(self) -> str:
        """Get ID stem from owner's class name.

        Unlike IdTree which uses its own class name, TemplateIdTree uses
        the owner's class name. This ensures that different template types
        get different ID stems even though they all use TemplateIdTree.

        Returns
        -------
            str: ID stem from owner's class name (lowercase)

        Examples
        --------
            >>> from dash_component_template.template import Template
            >>> class MyTemplate(Template): pass
            >>> t = MyTemplate()
            >>> t._tree._id_stem()  # Uses owner class name
            'mytemplate'
            >>> t.id  # doctest: +ELLIPSIS
            'mytemplate...'
        """
        return self._owner.__class__.__name__.lower()

    @property
    def owner(self) -> _Template:
        """Get the template that owns this tree node.

        Returns
        -------
        Template
            The owning template instance

        Examples
        --------
        >>> from dash_component_template import Template
        >>> from dash import html
        >>> template = Template()
        >>> div = template.child[html.Div]()
        >>> div._tree.owner is div
        True
        """
        return self._owner
