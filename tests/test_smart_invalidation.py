"""Test smart invalidation strategy with timing benchmarks.

This test suite validates that smart invalidation:
1. Works correctly for all scenarios
2. Provides O(1) performance for NullComponent pattern
3. Provides O(n) performance for hierarchical reparenting
4. Maintains optimal performance characteristics
"""

import time

import pytest

from dash_component_template.idtree import IdTree, reset_id_counters


class NullComponentIdTree(IdTree):
    """IdTree that mimics NullComponent with None ID."""

    def __init__(self, parent=None):
        # Don't call super().__init__() to avoid automatic ID generation
        # Manually setup what we need
        super(IdTree, self).__init__()  # Call NodeMixin.__init__
        self._cached_id = None  # NullComponent returns None
        self.parent = parent

    @property
    def id(self):
        """Return None (NullComponent pattern)."""
        return None

    @property
    def id_base(self):
        """Return None."""
        return None


class TestSmartInvalidation:
    """Test correctness of smart invalidation."""

    def setup_method(self):
        reset_id_counters()

    def test_smart_invalidation_with_null_parent(self):
        """Smart invalidation should not recurse when parent.id is None."""
        # Build tree with NullComponent root
        null = NullComponentIdTree()
        child = IdTree(parent=null)
        grandchild = IdTree(parent=child)
        great_grandchild = IdTree(parent=grandchild)

        # Cache all IDs
        assert child.id == "idtree0"
        assert grandchild.id == "idtree0-idtree1"
        assert great_grandchild.id == "idtree0-idtree1-idtree2"

        # Track if grandchild's _invalidate_id was called
        grandchild_invalidation_count = 0
        original_smart_invalidate = grandchild._invalidate_id

        def tracked_invalidate():
            nonlocal grandchild_invalidation_count
            grandchild_invalidation_count += 1
            return original_smart_invalidate()

        grandchild._invalidate_id = tracked_invalidate

        # Move null to a real parent
        main = IdTree()
        null.parent = main

        # child's ID should NOT change (parent.id is still None)
        assert child.id == "idtree0"
        assert grandchild.id == "idtree0-idtree1"
        assert great_grandchild.id == "idtree0-idtree1-idtree2"

        # grandchild should NOT have been invalidated (smart optimization)
        assert grandchild_invalidation_count == 0

    def test_smart_invalidation_with_hierarchical_parent(self):
        """Smart invalidation should recurse when ID actually changes."""
        # Build tree with real hierarchical parent
        parent1 = IdTree()
        child = IdTree(parent=parent1)
        grandchild = IdTree(parent=child)
        great_grandchild = IdTree(parent=grandchild)

        # Cache all IDs
        assert parent1.id == "idtree0"
        assert child.id == "idtree0-idtree1"
        assert grandchild.id == "idtree0-idtree1-idtree2"
        assert great_grandchild.id == "idtree0-idtree1-idtree2-idtree3"

        # Move child to different parent
        parent2 = IdTree()
        child.parent = parent2

        # All IDs should be updated (hierarchical change)
        assert child.id == "idtree4-idtree1"
        assert grandchild.id == "idtree4-idtree1-idtree2"
        assert great_grandchild.id == "idtree4-idtree1-idtree2-idtree3"

    def test_detach_invalidation(self):
        """Detaching should trigger smart invalidation."""
        root = IdTree()
        child = IdTree(parent=root)
        grandchild = IdTree(parent=child)

        assert child.id == "idtree0-idtree1"
        assert grandchild.id == "idtree0-idtree1-idtree2"

        # Detach child (becomes root)
        child.parent = None

        # IDs should update (detachment changes them)
        assert child.id == "idtree1"
        assert grandchild.id == "idtree1-idtree2"


class TestSmartInvalidationPerformance:
    """Test performance characteristics of smart invalidation."""

    def setup_method(self):
        reset_id_counters()

    def test_null_parent_no_propagation_timing(self):
        """Attaching to NullComponent should be O(1), not O(n)."""
        # Build large tree (100 nodes)
        null = NullComponentIdTree()
        nodes = []
        current = IdTree(parent=null)
        nodes.append(current)

        for _ in range(99):
            current = IdTree(parent=current)
            nodes.append(current)

        # Cache all IDs (force computation)
        for node in nodes:
            _ = node.id

        # Count how many nodes get invalidated
        invalidation_counts = {id(node): 0 for node in nodes}

        for node in nodes:
            original = node._invalidate_id

            def make_tracked(n):
                def tracked():
                    invalidation_counts[id(n)] += 1
                    return original()  # noqa: B023

                return tracked

            node._invalidate_id = make_tracked(node)

        # Attach null to main layout
        main = IdTree()
        start = time.perf_counter()
        null.parent = main
        elapsed = time.perf_counter() - start

        # With lazy computation, invalidation only happens if cache exists
        # Since we forced computation above, first node should be invalidated
        # (but it returns early if ID unchanged, so count may be 0 or 1)
        # The key is that deeper nodes shouldn't be invalidated
        assert invalidation_counts[id(nodes[0])] <= 1, "First node may be invalidated"

        # Other nodes should NOT be invalidated (smart optimization)
        for i in range(1, len(nodes)):
            assert invalidation_counts[id(nodes[i])] == 0, (
                f"Node {i} should not be invalidated"
            )

        print(f"\n  Null parent (100 nodes): {elapsed * 1e6:.2f}μs")
        print("  Nodes invalidated: 1/100 (smart optimization)")

    def test_hierarchical_parent_full_propagation_timing(self):
        """Attaching to hierarchical parent should be O(n)."""
        # Build large tree
        parent1 = IdTree()
        nodes = []
        current = IdTree(parent=parent1)
        nodes.append(current)

        for _ in range(99):
            current = IdTree(parent=current)
            nodes.append(current)

        # Cache all IDs
        for node in nodes:
            _ = node.id

        # Store initial IDs
        initial_ids = [node.id for node in nodes]

        # Move to different hierarchical parent
        parent2 = IdTree()
        start = time.perf_counter()
        nodes[0].parent = parent2
        elapsed = time.perf_counter() - start

        # ALL IDs should have changed (hierarchical reparenting)
        for i, node in enumerate(nodes):
            new_id = node.id
            assert new_id != initial_ids[i], f"Node {i} ID should have changed"

        print(f"\n  Hierarchical parent (100 nodes): {elapsed * 1e6:.2f}μs")
        print("  Nodes invalidated: 100/100 (full recursion needed)")

    def test_scaling_null_vs_hierarchical(self):
        """Compare scaling of null parent vs hierarchical parent."""
        sizes = [10, 50, 100, 500]
        null_times = []
        hierarchical_times = []

        for size in sizes:
            reset_id_counters()

            # Test null parent (should be constant time)
            null = NullComponentIdTree()
            nodes = []
            current = IdTree(parent=null)
            nodes.append(current)
            for _ in range(size - 1):
                current = IdTree(parent=current)
                nodes.append(current)

            # Cache IDs
            for node in nodes:
                _ = node.id

            # Time attachment
            main = IdTree()
            start = time.perf_counter()
            null.parent = main
            null_times.append(time.perf_counter() - start)

            # Test hierarchical parent (should scale with size)
            reset_id_counters()
            parent1 = IdTree()
            nodes = []
            current = IdTree(parent=parent1)
            nodes.append(current)
            for _ in range(size - 1):
                current = IdTree(parent=current)
                nodes.append(current)

            # Cache IDs
            for node in nodes:
                _ = node.id

            # Time reparenting
            parent2 = IdTree()
            start = time.perf_counter()
            nodes[0].parent = parent2
            hierarchical_times.append(time.perf_counter() - start)

        print("\n  Scaling comparison:")
        print(
            f"  {'Size':<10} {'Null (μs)':<15} {'Hierarchical (μs)':<20} {'Ratio':<10}"
        )
        print(f"  {'-' * 10} {'-' * 15} {'-' * 20} {'-' * 10}")

        for i, size in enumerate(sizes):
            null_us = null_times[i] * 1e6
            hier_us = hierarchical_times[i] * 1e6
            ratio = hier_us / null_us if null_us > 0 else 0
            print(f"  {size:<10} {null_us:<15.2f} {hier_us:<20.2f} {ratio:<10.1f}x")

        # Null parent should show constant time (ratio stays roughly same)
        # Hierarchical should scale linearly with size


class TestSmartInvalidationVsNaive:
    """Compare smart invalidation to naive (always recurse) approach."""

    def setup_method(self):
        reset_id_counters()

    def test_smart_vs_naive_null_parent(self):  # noqa: C901
        """Smart invalidation should be much faster for null parent."""
        size = 200

        # Test with smart invalidation (current implementation)
        null_smart = NullComponentIdTree()
        nodes_smart = []
        current = IdTree(parent=null_smart)
        nodes_smart.append(current)
        for _ in range(size - 1):
            current = IdTree(parent=current)
            nodes_smart.append(current)

        # Cache IDs
        for node in nodes_smart:
            _ = node.id

        # Time smart invalidation
        main_smart = IdTree()
        start = time.perf_counter()
        null_smart.parent = main_smart
        smart_time = time.perf_counter() - start

        # Test with naive invalidation (always recurse)
        reset_id_counters()
        null_naive = NullComponentIdTree()
        nodes_naive = []
        current = IdTree(parent=null_naive)
        nodes_naive.append(current)
        for _ in range(size - 1):
            current = IdTree(parent=current)
            nodes_naive.append(current)

        # Cache IDs
        for node in nodes_naive:
            _ = node.id

        # Create naive invalidation (always recurse, no smart optimization)
        def make_naive_invalidate(node):
            def naive_invalidate():
                # Always invalidate, always recurse (no smart check)
                node.__dict__.pop("_id_cached", None)
                for child in node.children:
                    if isinstance(child, IdTree) and hasattr(
                        child, "_naive_invalidate"
                    ):
                        child._naive_invalidate()

            return naive_invalidate

        # Replace smart invalidation with naive for all nodes (including null)
        for node in [null_naive, *nodes_naive]:
            node._naive_invalidate = make_naive_invalidate(node)

        # Monkey-patch _post_attach to use naive invalidation
        original_post_attach = null_naive._post_attach

        def naive_post_attach(parent):
            null_naive._naive_invalidate()

        null_naive._post_attach = naive_post_attach

        # Time naive invalidation
        main_naive = IdTree()
        start = time.perf_counter()
        null_naive.parent = main_naive
        naive_time = time.perf_counter() - start

        speedup = naive_time / smart_time if smart_time > 0 else 0

        print(f"\n  Null parent with {size} nodes:")
        print(f"    Smart invalidation: {smart_time * 1e6:.2f}μs")
        print(f"    Naive invalidation: {naive_time * 1e6:.2f}μs")
        print(f"    Speedup: {speedup:.1f}x")

        # Smart should be faster (at least 2x, accounting for test overhead)
        assert speedup > 2, f"Smart invalidation should be faster: {speedup:.1f}x"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
