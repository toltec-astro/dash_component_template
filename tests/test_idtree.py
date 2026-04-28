"""Tests for IdTree automatic ID generation.

This test suite covers:
1. Basic ID generation and uniqueness
2. Hierarchical ID structure
3. Tree manipulation (parent changes, moving nodes)
4. Multiple inheritance and subclassing
5. Edge cases (None parent, root nodes, orphans)
6. anytree integration
"""

import pytest
from anytree import PreOrderIter, RenderTree

from dash_component_template.idtree import IdTree, reset_id_counters


@pytest.fixture(autouse=True)
def reset_counters():
    """Reset ID counters before each test for predictable IDs."""
    reset_id_counters()
    yield
    reset_id_counters()


class TestBasicIDGeneration:
    """Test basic ID generation and uniqueness."""

    def test_root_node_id(self):
        """Root nodes should have simple id_base as ID."""
        root = IdTree()
        assert root.id == "idtree0"
        assert root.id_base == "idtree0"

    def test_multiple_root_nodes_unique(self):
        """Multiple root nodes should have unique IDs."""
        root1 = IdTree()
        root2 = IdTree()
        root3 = IdTree()

        assert root1.id == "idtree0"
        assert root2.id == "idtree1"
        assert root3.id == "idtree2"

        # All should be unique
        ids = {root1.id, root2.id, root3.id}
        assert len(ids) == 3

    def test_child_node_id(self):
        """Child nodes should have hierarchical IDs."""
        root = IdTree()
        child = IdTree(parent=root)

        assert root.id == "idtree0"
        assert child.id == "idtree0-idtree1"
        assert child.id_base == "idtree1"

    def test_grandchild_node_id(self):
        """Grandchildren should have full hierarchical path."""
        root = IdTree()
        child = IdTree(parent=root)
        grandchild = IdTree(parent=child)

        assert root.id == "idtree0"
        assert child.id == "idtree0-idtree1"
        assert grandchild.id == "idtree0-idtree1-idtree2"

    def test_deep_hierarchy(self):
        """Test deep tree hierarchy (10 levels)."""
        nodes = []
        parent = None

        for _i in range(10):
            node = IdTree(parent=parent)
            nodes.append(node)
            parent = node

        # Check each level
        assert nodes[0].id == "idtree0"
        assert nodes[1].id == "idtree0-idtree1"
        assert nodes[2].id == "idtree0-idtree1-idtree2"
        assert (
            nodes[9].id
            == "idtree0-idtree1-idtree2-idtree3-idtree4-idtree5-idtree6-idtree7-idtree8-idtree9"  # noqa: E501
        )


class TestHierarchicalStructure:
    """Test hierarchical ID structure with complex trees."""

    def test_siblings_unique_ids(self):
        """Siblings should have unique IDs."""
        root = IdTree()
        child1 = IdTree(parent=root)
        child2 = IdTree(parent=root)
        child3 = IdTree(parent=root)

        assert child1.id == "idtree0-idtree1"
        assert child2.id == "idtree0-idtree2"
        assert child3.id == "idtree0-idtree3"

        # All should be unique
        ids = {child1.id, child2.id, child3.id}
        assert len(ids) == 3

    def test_complex_tree_structure(self):
        """Test complex tree with multiple branches."""
        #       root
        #      /    \
        #   child1  child2
        #    /  \      \
        #   gc1 gc2    gc3

        root = IdTree()
        child1 = IdTree(parent=root)
        child2 = IdTree(parent=root)
        gc1 = IdTree(parent=child1)
        gc2 = IdTree(parent=child1)
        gc3 = IdTree(parent=child2)

        assert root.id == "idtree0"
        assert child1.id == "idtree0-idtree1"
        assert child2.id == "idtree0-idtree2"
        assert gc1.id == "idtree0-idtree1-idtree3"
        assert gc2.id == "idtree0-idtree1-idtree4"
        assert gc3.id == "idtree0-idtree2-idtree5"

        # All IDs should be unique
        all_nodes = [root, child1, child2, gc1, gc2, gc3]
        ids = {node.id for node in all_nodes}
        assert len(ids) == 6


class TestTreeManipulation:
    """Test ID behavior when tree structure changes."""

    def test_change_parent_updates_id(self):
        """Changing parent should update ID dynamically."""
        root1 = IdTree()
        root2 = IdTree()
        child = IdTree(parent=root1)

        # Initially attached to root1
        assert child.id == "idtree0-idtree2"

        # Move to root2
        child.parent = root2
        assert child.id == "idtree1-idtree2"

    def test_detach_node_becomes_root(self):
        """Detaching a node makes it a root with simple ID."""
        root = IdTree()
        child = IdTree(parent=root)
        grandchild = IdTree(parent=child)

        # Initially part of tree
        assert grandchild.id == "idtree0-idtree1-idtree2"

        # Detach child (becomes new root)
        child.parent = None

        # Child is now root
        assert child.id == "idtree1"
        # Grandchild updates to reflect new parent ID
        assert grandchild.id == "idtree1-idtree2"

    def test_move_subtree(self):
        """Moving a subtree should update all descendant IDs."""
        #       root1        root2
        #       /              |
        #   child           (empty)
        #     /
        #   gc
        #
        # Move child (with gc) from root1 to root2

        root1 = IdTree()
        root2 = IdTree()
        child = IdTree(parent=root1)
        gc = IdTree(parent=child)

        # Initial state
        assert child.id == "idtree0-idtree2"
        assert gc.id == "idtree0-idtree2-idtree3"

        # Move child to root2
        child.parent = root2

        # IDs update for entire subtree
        assert child.id == "idtree1-idtree2"
        assert gc.id == "idtree1-idtree2-idtree3"

    def test_multiple_moves(self):
        """Test multiple moves of the same node."""
        roots = [IdTree() for _ in range(5)]
        child = IdTree(parent=roots[0])

        for i, root in enumerate(roots):
            child.parent = root
            expected_id = f"idtree{i}-idtree5"
            assert child.id == expected_id


class TestSubclassing:
    """Test IdTree with subclasses."""

    def test_subclass_has_own_counter(self):
        """Subclasses should have independent counters."""

        class MyNode(IdTree):
            pass

        class OtherNode(IdTree):
            pass

        # Create instances of different classes
        base1 = IdTree()
        base2 = IdTree()
        my1 = MyNode()
        my2 = MyNode()
        other1 = OtherNode()

        # Each class has its own counter
        assert base1.id == "idtree0"
        assert base2.id == "idtree1"
        assert my1.id == "mynode0"
        assert my2.id == "mynode1"
        assert other1.id == "othernode0"

    def test_subclass_hierarchy(self):
        """Test hierarchical IDs with mixed subclasses."""

        class Container(IdTree):
            pass

        class Item(IdTree):
            pass

        container = Container()
        item1 = Item(parent=container)
        item2 = Item(parent=container)

        assert container.id == "container0"
        assert item1.id == "container0-item0"
        assert item2.id == "container0-item1"

    def test_subclass_id_base(self):
        """Subclass id_base should use subclass name."""

        class SpecialNode(IdTree):
            pass

        node = SpecialNode()
        assert node.id_base == "specialnode0"
        assert node.id == "specialnode0"


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_none_parent_explicit(self):
        """Explicitly passing parent=None creates root."""
        node = IdTree(parent=None)
        assert node.id == "idtree0"
        assert node.parent is None
        assert node.is_root

    def test_orphan_node_id(self):
        """Orphaned node should have simple ID."""
        child = IdTree(parent=IdTree())
        # Detach
        child.parent = None
        assert child.id == child.id_base

    def test_empty_tree(self):
        """Test single node with no children."""
        root = IdTree()
        assert root.id == "idtree0"
        assert len(root.children) == 0
        assert root.is_leaf

    def test_id_stability_on_multiple_access(self):
        """ID should be consistent across multiple accesses."""
        root = IdTree()
        child = IdTree(parent=root)

        # Access ID multiple times
        ids = [child.id for _ in range(100)]

        # All should be identical
        assert len(set(ids)) == 1
        assert ids[0] == "idtree0-idtree1"


class TestAnytreeIntegration:
    """Test integration with anytree features."""

    def test_children_property(self):
        """Test anytree children property."""
        root = IdTree()
        child1 = IdTree(parent=root)
        child2 = IdTree(parent=root)

        assert len(root.children) == 2
        assert child1 in root.children
        assert child2 in root.children

    def test_descendants(self):
        """Test anytree descendants property."""
        root = IdTree()
        child = IdTree(parent=root)
        grandchild = IdTree(parent=child)

        # Root has 2 descendants
        descendants = list(root.descendants)
        assert len(descendants) == 2
        assert child in descendants
        assert grandchild in descendants

    def test_ancestors(self):
        """Test anytree ancestors property."""
        root = IdTree()
        child = IdTree(parent=root)
        grandchild = IdTree(parent=child)

        # Grandchild has 2 ancestors
        ancestors = grandchild.ancestors
        assert len(ancestors) == 2
        assert root in ancestors
        assert child in ancestors

    def test_is_root_property(self):
        """Test anytree is_root property."""
        root = IdTree()
        child = IdTree(parent=root)

        assert root.is_root
        assert not child.is_root

    def test_is_leaf_property(self):
        """Test anytree is_leaf property."""
        root = IdTree()
        child = IdTree(parent=root)
        grandchild = IdTree(parent=child)

        assert not root.is_leaf
        assert not child.is_leaf
        assert grandchild.is_leaf

    def test_root_property(self):
        """Test anytree root property."""
        root = IdTree()
        child = IdTree(parent=root)
        grandchild = IdTree(parent=child)

        assert root.root == root
        assert child.root == root
        assert grandchild.root == root

    def test_depth_property(self):
        """Test anytree depth property."""
        root = IdTree()
        child = IdTree(parent=root)
        grandchild = IdTree(parent=child)

        assert root.depth == 0
        assert child.depth == 1
        assert grandchild.depth == 2

    def test_preorder_iteration(self):
        """Test anytree PreOrderIter."""
        #       root
        #      /    \
        #   child1  child2
        #    /
        #   gc

        root = IdTree()
        child1 = IdTree(parent=root)
        child2 = IdTree(parent=root)
        gc = IdTree(parent=child1)

        nodes = list(PreOrderIter(root))
        assert len(nodes) == 4
        assert nodes[0] == root
        assert nodes[1] == child1
        assert nodes[2] == gc
        assert nodes[3] == child2

    def test_render_tree(self):
        """Test anytree RenderTree."""
        root = IdTree()
        child1 = IdTree(parent=root)
        child2 = IdTree(parent=root)
        gc = IdTree(parent=child1)

        # Should render without errors
        tree_str = str(RenderTree(root))
        assert "idtree0" in tree_str
        assert "idtree1" in tree_str
        assert "idtree2" in tree_str
        assert "idtree3" in tree_str


class TestRepr:
    """Test string representation."""

    def test_repr_root(self):
        """Test __repr__ for root node."""
        root = IdTree()
        assert repr(root) == "IdTree('idtree0')"

    def test_repr_child(self):
        """Test __repr__ for child node."""
        root = IdTree()
        child = IdTree(parent=root)
        assert repr(child) == "IdTree('idtree0-idtree1')"

    def test_repr_subclass(self):
        """Test __repr__ for subclass."""

        class MyNode(IdTree):
            pass

        node = MyNode()
        assert repr(node) == "MyNode('mynode0')"


class TestResetCounters:
    """Test counter reset functionality."""

    def test_reset_counters(self):
        """Test that reset_id_counters() works."""
        # Create some nodes
        node1 = IdTree()
        assert node1.id == "idtree0"

        # Reset
        reset_id_counters()

        # Counter should start at 0 again
        node2 = IdTree()
        assert node2.id == "idtree0"

    def test_reset_affects_subclasses(self):
        """Test that reset affects all classes."""

        class MyNode(IdTree):
            pass

        node1 = MyNode()
        assert node1.id == "mynode0"

        reset_id_counters()

        node2 = MyNode()
        assert node2.id == "mynode0"


class TestConcurrentTrees:
    """Test multiple independent trees."""

    def test_multiple_trees_independent(self):
        """Test that multiple trees can coexist."""
        # Tree 1
        root1 = IdTree()
        child1a = IdTree(parent=root1)
        child1b = IdTree(parent=root1)

        # Tree 2
        root2 = IdTree()
        child2a = IdTree(parent=root2)

        # Tree 3
        root3 = IdTree()

        # All should have unique IDs
        all_nodes = [root1, child1a, child1b, root2, child2a, root3]
        ids = {node.id for node in all_nodes}
        assert len(ids) == 6

    def test_merge_trees(self):
        """Test merging two independent trees."""
        # Create two independent trees
        tree1_root = IdTree()
        tree1_child = IdTree(parent=tree1_root)

        tree2_root = IdTree()
        tree2_child = IdTree(parent=tree2_root)

        # Initial IDs
        assert tree1_child.id == "idtree0-idtree1"
        assert tree2_child.id == "idtree2-idtree3"

        # Merge: attach tree2_root to tree1_root
        tree2_root.parent = tree1_root

        # IDs update to reflect new structure
        assert tree2_root.id == "idtree0-idtree2"
        assert tree2_child.id == "idtree0-idtree2-idtree3"


class TestLargeScale:
    """Test with large numbers of nodes."""

    def test_100_siblings(self):
        """Test tree with 100 siblings."""
        root = IdTree()
        children = [IdTree(parent=root) for _ in range(100)]

        # All should have unique IDs
        ids = {child.id for child in children}
        assert len(ids) == 100

        # Check a few specific IDs
        assert children[0].id == "idtree0-idtree1"
        assert children[50].id == "idtree0-idtree51"
        assert children[99].id == "idtree0-idtree100"

    def test_wide_and_deep_tree(self):
        """Test tree with both width and depth."""
        # Create tree: 10 levels, 5 children per node
        root = IdTree()

        def create_subtree(parent, depth, breadth):
            if depth == 0:
                return
            for _ in range(breadth):
                child = IdTree(parent=parent)
                create_subtree(child, depth - 1, breadth)

        create_subtree(root, depth=3, breadth=5)

        # Count all nodes
        all_nodes = list(PreOrderIter(root))
        # 1 + 5 + 25 + 125 = 156 nodes
        assert len(all_nodes) == 1 + 5 + 25 + 125

        # All IDs should be unique
        ids = {node.id for node in all_nodes}
        assert len(ids) == len(all_nodes)
