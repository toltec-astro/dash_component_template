"""Comprehensive tests for IdTree cache invalidation.

This test suite specifically focuses on the caching behavior and cache
invalidation logic of the IdTree implementation. It ensures that:

1. IDs are properly cached after first access
2. Cache is correctly invalidated when tree structure changes
3. Cache invalidation propagates to all descendants
4. anytree lifecycle hooks (_post_attach, _post_detach) work correctly
5. Edge cases in cache invalidation are handled properly

These tests complement the existing functional tests (test_idtree.py) by
explicitly testing the caching infrastructure.
"""

import functools

import pytest
from anytree import PreOrderIter

from dash_component_template.idtree import IdTree, reset_id_counters


class TestCacheCreation:
    """Test that cache is created correctly on initialization."""

    def setup_method(self):
        """Reset counters before each test."""
        reset_id_counters()

    def test_cache_initialized_on_creation(self):
        """Cache should be created on first access (lazy)."""
        root = IdTree()

        # Cache should NOT be populated until first access (lazy)
        assert "_id_cached" not in root.__dict__

        # Access ID to populate cache
        assert root.id == "idtree0"

        # Now cache should be populated
        assert "_id_cached" in root.__dict__
        assert root.__dict__["_id_cached"] == "idtree0"

    def test_cache_initialized_with_parent(self):
        """Cache is now lazy - not populated until first access."""
        root = IdTree()
        child = IdTree(parent=root)

        # Cache is NOT populated during parent assignment anymore (lazy)
        assert "_id_cached" not in child.__dict__

        # But accessing ID populates it
        child_id = child.id
        assert "_id_cached" in child.__dict__
        assert child.__dict__["_id_cached"] == "idtree0-idtree1"
        assert child_id == "idtree0-idtree1"

    def test_cache_survives_multiple_accesses(self):
        """Cache should persist across multiple ID accesses."""
        root = IdTree()
        # First access populates cache
        _ = root.id
        original_cache = root.__dict__["_id_cached"]

        # Access ID multiple times
        for _ in range(100):
            _ = root.id

        # Cache object should be unchanged (same reference)
        assert root.__dict__["_id_cached"] is original_cache


class TestCacheInvalidation:
    """Test cache invalidation on structure changes."""

    def setup_method(self):
        """Reset counters before each test."""
        reset_id_counters()

    def test_attach_invalidates_cache(self):
        """Attaching a node should invalidate its cache."""
        root = IdTree()  # idtree0
        orphan = IdTree()  # idtree1

        original_id = orphan.id
        assert original_id == "idtree1"  # Orphan is root

        # Save cache reference
        original_cache = orphan.__dict__["_id_cached"]

        # Attach to root (changes ID)
        orphan.parent = root

        # Cache should be invalidated and recomputed
        assert orphan.id == "idtree0-idtree1"
        assert orphan.__dict__["_id_cached"] is not original_cache

    def test_detach_invalidates_cache(self):
        """Detaching a node should invalidate its cache."""
        root = IdTree()
        child = IdTree(parent=root)

        assert child.id == "idtree0-idtree1"
        original_cache = child.__dict__["_id_cached"]

        # Detach (becomes root)
        child.parent = None

        # Cache should be invalidated and recomputed
        assert child.id == "idtree1"
        assert child.__dict__["_id_cached"] is not original_cache

    def test_change_parent_invalidates_cache(self):
        """Changing parent should invalidate cache."""
        root1 = IdTree()
        root2 = IdTree()
        child = IdTree(parent=root1)

        assert child.id == "idtree0-idtree2"
        original_cache = child.__dict__["_id_cached"]

        # Change parent
        child.parent = root2

        # Cache should be invalidated and recomputed
        assert child.id == "idtree1-idtree2"
        assert child.__dict__["_id_cached"] is not original_cache

    def test_invalidation_propagates_to_children(self):
        """Cache invalidation should propagate to all descendants."""
        root = IdTree()
        child = IdTree(parent=root)
        grandchild = IdTree(parent=child)
        great_grandchild = IdTree(parent=grandchild)

        # Cache initial IDs
        assert grandchild.id == "idtree0-idtree1-idtree2"
        assert great_grandchild.id == "idtree0-idtree1-idtree2-idtree3"

        child_cache_before = child.__dict__["_id_cached"]
        grandchild_cache_before = grandchild.__dict__["_id_cached"]
        great_grandchild_cache_before = great_grandchild.__dict__["_id_cached"]

        # Detach subtree
        child.parent = None

        # All descendants should have invalidated caches
        assert child.__dict__["_id_cached"] is not child_cache_before
        assert grandchild.__dict__["_id_cached"] is not grandchild_cache_before
        assert (
            great_grandchild.__dict__["_id_cached"] is not great_grandchild_cache_before
        )

        # All IDs should be updated
        assert child.id == "idtree1"
        assert grandchild.id == "idtree1-idtree2"
        assert great_grandchild.id == "idtree1-idtree2-idtree3"

    def test_invalidation_does_not_affect_siblings(self):
        """Cache invalidation should not affect sibling branches."""
        root = IdTree()
        child1 = IdTree(parent=root)
        child2 = IdTree(parent=root)
        grandchild1 = IdTree(parent=child1)
        grandchild2 = IdTree(parent=child2)

        # Cache all IDs
        _ = grandchild1.id
        _ = grandchild2.id

        grandchild2_cache_before = grandchild2.__dict__["_id_cached"]

        # Detach child1 subtree
        child1.parent = None

        # grandchild2's cache should be unchanged (different branch)
        assert grandchild2.__dict__["_id_cached"] is grandchild2_cache_before
        assert grandchild2.id == "idtree0-idtree2-idtree4"


class TestAnytreeHooks:
    """Test anytree lifecycle hooks for cache invalidation."""

    def setup_method(self):
        """Reset counters before each test."""
        reset_id_counters()

    def test_post_attach_hook_called(self):
        """_post_attach should be called when parent is set."""

        class TrackedIdTree(IdTree):
            def __init__(self, *args, **kwargs):
                self.post_attach_called = False
                super().__init__(*args, **kwargs)

            def _post_attach(self, parent):
                self.post_attach_called = True
                super()._post_attach(parent)

        root = IdTree()
        child = TrackedIdTree()

        # Hook not called yet
        assert not child.post_attach_called

        # Attach to parent
        child.parent = root

        # Hook should have been called
        assert child.post_attach_called

    def test_post_detach_hook_called(self):
        """_post_detach should be called when parent is removed."""

        class TrackedIdTree(IdTree):
            def __init__(self, *args, **kwargs):
                self.post_detach_called = False
                super().__init__(*args, **kwargs)

            def _post_detach(self, parent):
                self.post_detach_called = True
                super()._post_detach(parent)

        root = IdTree()
        child = TrackedIdTree(parent=root)

        # Hook not called yet
        assert not child.post_detach_called

        # Detach from parent
        child.parent = None

        # Hook should have been called
        assert child.post_detach_called

    def test_hooks_maintain_id_consistency(self):
        """Hooks should ensure IDs are always consistent with structure."""
        root = IdTree()
        child = IdTree(parent=root)
        grandchild = IdTree(parent=child)

        # Initial state
        assert child.id == "idtree0-idtree1"
        assert grandchild.id == "idtree0-idtree1-idtree2"

        # Move child to different parent
        new_root = IdTree()
        child.parent = new_root

        # IDs should be immediately consistent (hooks worked)
        assert child.id == "idtree3-idtree1"
        assert grandchild.id == "idtree3-idtree1-idtree2"


class TestCachePerformance:
    """Test that caching actually provides performance benefit."""

    def setup_method(self):
        """Reset counters before each test."""
        reset_id_counters()

    def test_cached_access_is_constant_time(self):
        """Accessing cached ID should be O(1) regardless of depth."""
        import time

        # Create deep tree
        root = IdTree()
        current = root
        for _ in range(100):
            current = IdTree(parent=current)

        leaf = current

        # First access (cache already populated in __init__)
        _ = leaf.id

        # Time many accesses
        iterations = 10000
        start = time.perf_counter()
        for _ in range(iterations):
            _ = leaf.id
        elapsed = time.perf_counter() - start

        avg_time_us = (elapsed / iterations) * 1_000_000

        # Should be very fast (< 0.1μs on modern hardware)
        assert avg_time_us < 0.2, f"Cached access too slow: {avg_time_us:.3f}μs"

    def test_cache_reduces_computation(self):
        """Cache should prevent repeated access to cached_property."""

        class ComputeTrackingIdTree(IdTree):
            compute_count = 0

            @functools.cached_property
            def _id_cached(self) -> str:
                ComputeTrackingIdTree.compute_count += 1
                return super()._id_cached

        # Reset counter
        ComputeTrackingIdTree.compute_count = 0

        # Create tree
        root = ComputeTrackingIdTree()
        child = ComputeTrackingIdTree(parent=root)
        grandchild = ComputeTrackingIdTree(parent=child)

        # IDs are lazy now - not computed during __init__
        assert ComputeTrackingIdTree.compute_count == 0

        # First access computes IDs (3 nodes = 3 computes)
        _ = root.id
        _ = child.id
        _ = grandchild.id
        assert ComputeTrackingIdTree.compute_count == 3

        # Access IDs many more times
        for _ in range(100):
            _ = root.id
            _ = child.id
            _ = grandchild.id

        # Compute count should not increase (using cache)
        assert ComputeTrackingIdTree.compute_count == 3


class TestEdgeCases:
    """Test edge cases in cache invalidation."""

    def setup_method(self):
        """Reset counters before each test."""
        reset_id_counters()

    def test_null_cache_on_access(self):
        """Cached property handles missing cache automatically."""
        root = IdTree()

        # First access populates cache
        _ = root.id
        assert "_id_cached" in root.__dict__

        # Delete cache from __dict__ (simulate invalidation)
        del root.__dict__["_id_cached"]
        assert "_id_cached" not in root.__dict__

        # Access should recompute via cached_property
        assert root.id == "idtree0"
        assert "_id_cached" in root.__dict__

    def test_move_to_same_parent(self):
        """Moving to same parent invalidates but recomputes to same value."""
        root = IdTree()
        child = IdTree(parent=root)

        _ = child.id  # Populate cache
        original_cache = child.__dict__["_id_cached"]
        original_id = child.id

        # "Move" to same parent (smart invalidation detects no change)
        child.parent = root

        # ID should be same value (though cache may be different object)
        assert child.id == original_id

    def test_deep_invalidation_chain(self):
        """Very deep trees should handle invalidation correctly."""
        # Create deep tree (depth 50)
        root = IdTree()
        current = root
        nodes = [root]

        for _ in range(49):
            current = IdTree(parent=current)
            nodes.append(current)

        # Cache all IDs
        for node in nodes:
            _ = node.id

        # Detach from middle
        middle = nodes[25]
        middle.parent = None

        # All descendants of middle should have updated IDs
        for i in range(26, 50):
            id_parts = nodes[i].id.split("-")
            # Should have 26 parts (middle + 24 descendants)
            assert len(id_parts) == (i - 25 + 1)

    def test_circular_prevention(self):
        """anytree prevents cycles, cache should handle gracefully."""
        root = IdTree()
        child = IdTree(parent=root)

        # anytree should prevent this
        with pytest.raises(Exception):  # noqa: B017  # anytree raises LoopError
            root.parent = child


class TestCacheWithSubclasses:
    """Test cache behavior with subclassed IdTree."""

    def setup_method(self):
        """Reset counters before each test."""
        reset_id_counters()

    def test_subclass_cache_works(self):
        """Subclasses should have working cache."""

        class MyNode(IdTree):
            pass

        root = MyNode()
        child = MyNode(parent=root)

        # Cache is lazy - not populated until access
        assert "_id_cached" not in child.__dict__

        # Accessing ID populates cache
        assert child.id == "mynode0-mynode1"
        assert "_id_cached" in child.__dict__

    def test_mixed_hierarchy_cache(self):
        """Cache should work in mixed IdTree/subclass hierarchy."""

        class NodeA(IdTree):
            pass

        class NodeB(IdTree):
            pass

        root = IdTree()
        child_a = NodeA(parent=root)
        child_b = NodeB(parent=root)
        grandchild = IdTree(parent=child_a)

        # All should have working caches
        assert child_a.id == "idtree0-nodea0"
        assert child_b.id == "idtree0-nodeb0"
        assert grandchild.id == "idtree0-nodea0-idtree1"


class TestCacheConsistency:
    """Test that cache always remains consistent with tree structure."""

    def setup_method(self):
        """Reset counters before each test."""
        reset_id_counters()

    def test_id_matches_structure_after_moves(self):
        """ID should always match actual tree structure."""
        root1 = IdTree()
        root2 = IdTree()
        child = IdTree(parent=root1)
        grandchild = IdTree(parent=child)

        # Move child around multiple times
        child.parent = root2
        assert grandchild.id.startswith(root2.id)

        child.parent = None
        assert not grandchild.id.startswith(root1.id)
        assert not grandchild.id.startswith(root2.id)

        child.parent = root1
        assert grandchild.id.startswith(root1.id)

    def test_parallel_modifications(self):
        """Multiple simultaneous modifications should maintain consistency."""
        root = IdTree()
        children = [IdTree(parent=root) for _ in range(10)]
        grandchildren = [[IdTree(parent=child) for _ in range(3)] for child in children]

        # Move multiple children simultaneously
        new_root = IdTree()
        for child in children[:5]:
            child.parent = new_root

        # All moved grandchildren should have consistent IDs
        for i in range(5):
            for gc in grandchildren[i]:
                assert gc.id.startswith(new_root.id)

        # Unmoved grandchildren should still reference old root
        for i in range(5, 10):
            for gc in grandchildren[i]:
                assert gc.id.startswith(root.id)

    def test_cache_after_complex_restructuring(self):
        """Cache should remain valid after complex tree reorganization."""
        # Build initial tree
        root = IdTree()
        level1 = [IdTree(parent=root) for _ in range(3)]
        level2 = [[IdTree(parent=node) for _ in range(2)] for node in level1]

        # Complex reorganization
        # Move first level1 node to be child of last level1 node
        level1[0].parent = level1[2]

        # Move all level2[1] nodes to level2[0]
        for nodes in level2:
            if len(nodes) > 1:
                nodes[1].parent = level2[0][0]

        # Verify all IDs are consistent
        all_nodes = list(PreOrderIter(root))
        for node in all_nodes:
            id_parts = node.id.split("-")

            # Verify path matches ID
            path_nodes = [node]
            current = node.parent
            while current is not None:
                path_nodes.insert(0, current)
                current = current.parent

            # ID should match path
            expected_id = "-".join(n.id_base for n in path_nodes)
            assert node.id == expected_id, (
                f"Inconsistent ID: {node.id} vs {expected_id}"
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
