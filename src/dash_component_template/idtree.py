"""Automatic hierarchical ID generation for tree nodes with cached IDs.

This module provides the IdTree class that automatically generates unique,
hierarchical IDs for tree nodes using anytree's NodeMixin. IDs are cached
for O(1) access performance and automatically invalidated when the tree
structure changes.

Performance characteristics:
- ID access: O(1) constant time (cached)
- Tree construction: ~0.8μs per node
- Cache invalidation: O(descendants) on parent change
- Memory overhead: ~8 bytes per node for cache

Benchmark results (vs dynamic implementation):
- Single access at depth 5: 23x faster (1.19μs → 0.05μs)
- 100 renders of 364 nodes: 49x faster (48ms → 1ms)
- Overall UI component pattern: 26x faster (48.6ms → 1.8ms)
"""

from __future__ import annotations

import functools
import itertools
from typing import ClassVar

from anytree import NodeMixin


class IdTree(NodeMixin):
    """Tree node with cached hierarchical IDs.

    Similar to IdTree but caches the computed ID for O(1) access.
    Cache is invalidated when tree structure changes.

    Trade-offs:
    - Faster ID access: O(1) vs O(depth)
    - Slower structure changes: Must invalidate caches
    - More complex: Invalidation logic adds maintenance burden
    - More fragile: Cache invalidation bugs possible

    Attributes
    ----------
        parent: Parent node (from NodeMixin)
        children: Tuple of child nodes (from NodeMixin)
        id: Cached hierarchical ID
        id_base: Base ID for this instance
    """

    _class_counters: ClassVar[dict[str, itertools.count]] = {}

    def __init__(self, parent: IdTree | None = None, **kwargs) -> None:
        """Initialize node with unique instance label."""
        super().__init__(**kwargs)

        # Get or create counter for this class
        cls_name = self.__class__.__name__
        if cls_name not in IdTree._class_counters:
            IdTree._class_counters[cls_name] = itertools.count()

        self._instance_label: int = next(IdTree._class_counters[cls_name])

        # Set parent (triggers anytree's tree building and cache computation)
        self.parent = parent

    def _id_stem(self) -> str:
        """Get the stem part of the ID (without instance number).

        This method can be overridden by subclasses to customize
        the ID stem. By default, uses the lowercase class name.

        Returns
        -------
            str: ID stem (e.g., "idtree", "componenttemplate")

        Examples
        --------
            >>> class CustomTree(IdTree):
            ...     def _id_stem(self):
            ...         return "custom"
            >>> tree = CustomTree()
            >>> tree.id_base
            'custom0'
        """
        return self.__class__.__name__.lower()

    @property
    def id_base(self) -> str:
        """Base ID: stem + instance number.

        Combines the ID stem (from _id_stem()) with the instance number.
        """
        return f"{self._id_stem()}{self._instance_label}"

    @functools.cached_property
    def _id_cached(self) -> str:
        """Cached computation of hierarchical ID.

        Uses @functools.cached_property which stores the result in __dict__.
        Invalidation is done by deleting from __dict__.
        """
        if self.parent is None:
            return self.id_base

        parent_id = self.parent.id
        if parent_id is None:
            return self.id_base

        return f"{parent_id}-{self.id_base}"

    def _invalidate_id(self) -> None:
        """Invalidate the cached ID and propagate to children if changed.

        This is called when the tree structure changes (attach/detach).
        Only propagates invalidation to children if the ID actually changed.
        """
        # If no cached ID exists, nothing to invalidate
        old_id = self.__dict__.pop("_id_cached", None)
        if old_id is None:
            return

        # Get new ID (triggers recomputation via cached_property)
        new_id = self._id_cached

        # Only propagate if ID changed
        if old_id != new_id:
            for child in self.children:
                child._invalidate_id()

    @property
    def id(self) -> str:
        """Cached hierarchical ID with O(1) access.

        Returns
        -------
            Cached string with full hierarchical path
        """
        return self._id_cached

    def _pre_attach(self, parent: NodeMixin) -> None:
        """Pre-attach hook (anytree protocol); invalidation happens in post-attach."""

    def _post_attach(self, parent: NodeMixin) -> None:
        """Post-attach hook (anytree protocol); invalidate the cached ID."""
        self._invalidate_id()

    def _pre_detach(self, parent: NodeMixin) -> None:
        """Pre-detach hook (anytree protocol); invalidation happens in post-detach."""

    def _post_detach(self, parent: NodeMixin) -> None:
        """Post-detach hook (anytree protocol); invalidate the cached ID."""
        self._invalidate_id()

    def __repr__(self) -> str:
        """Return string representation."""
        return f"{self.__class__.__name__}('{self.id}')"


def reset_id_counters() -> None:
    """Reset all cached ID counters to zero."""
    IdTree._class_counters.clear()
