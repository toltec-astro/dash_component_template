"""Tests for LazyComponent - Core component template functionality.

Testing philosophy:
- Test the two-layer architecture (_Template + Template)
- Test IdTree integration and two-stage API
- Focus on core functionality and edge cases
"""

from __future__ import annotations

import pytest
from dash import html

from dash_component_template.idtree import IdTree
from dash_component_template.lazy_component import (
    LazyComponent,
    _make_lazy_component_cls,
)


@pytest.fixture(autouse=True)
def reset_counters():
    """Reset IdTree counters before each test."""
    IdTree._class_counters.clear()
    yield
    IdTree._class_counters.clear()


class TestBasicInstantiation:
    """Test basic LazyComponent creation and IdTree integration."""

    def test_creates_with_auto_id(self):
        """Template auto-generates ID from class name."""
        template = LazyComponent()
        assert template.id == "lazycomponent0"
        assert template.id == "lazycomponent0"  # Alias

    def test_creates_with_parent(self):
        """Child template gets hierarchical ID."""
        root = LazyComponent()
        child = LazyComponent(_parent=root)

        assert root.id == "lazycomponent0"
        assert child.id == "lazycomponent0-lazycomponent1"
        assert child.parent is root

    def test_creates_nested_hierarchy(self):
        """Deep nesting creates proper hierarchical IDs."""
        root = LazyComponent()
        child = LazyComponent(_parent=root)
        grandchild = LazyComponent(_parent=child)

        assert root.id == "lazycomponent0"
        assert child.id == "lazycomponent0-lazycomponent1"
        assert grandchild.id == "lazycomponent0-lazycomponent1-lazycomponent2"

    def test_stores_props(self):
        """Template stores props in descriptors for later materialization."""
        # Must use a generated subclass with _component_cls to have property descriptors
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate(className="my-class", style={"color": "red"})

        # Props are now stored in _PropsNamespace, access via _data
        assert template._props._data == {
            "className": "my-class",
            "style": {"color": "red"},
        }

    def test_initial_state(self):
        """New template has correct initial state."""
        template = LazyComponent()

        # Children are managed via the tree structure, not a separate list
        assert len(template.children) == 0


class TestTreeManipulation:
    """Test tree structure manipulation (key v2.2 feature!)."""

    def test_reparenting_updates_ids(self):
        """Reparenting a node updates its ID and descendants."""
        root1 = LazyComponent()
        root2 = LazyComponent()
        child = LazyComponent(_parent=root1)

        assert child.id == "lazycomponent0-lazycomponent2"

        # Reparent to root2
        child.parent = root2

        assert child.id == "lazycomponent1-lazycomponent2"

    def test_reparenting_with_grandchildren(self):
        """Reparenting updates entire subtree IDs."""
        root1 = LazyComponent()
        root2 = LazyComponent()
        child = LazyComponent(_parent=root1)
        grandchild = LazyComponent(_parent=child)

        original_grandchild_id = grandchild.id
        assert "lazycomponent0" in original_grandchild_id

        # Reparent child to root2
        child.parent = root2

        # Grandchild ID should update
        assert "lazycomponent1" in grandchild.id
        assert grandchild.id != original_grandchild_id


class TestTwoStageAPI:
    """Test the materialize workflow."""

    def test_materialize_creates_root_component(self):
        """materialize() creates _root_component if _component_cls is set."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate()

        result = template.materialize()

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 1
        component = result[0]
        assert getattr(component, "id", None) == template.id

    def test_materialize_without_component_cls(self):
        """materialize() raises TypeError if no _component_cls."""
        template = LazyComponent()
        # _component_cls is None by default

        with pytest.raises(TypeError, match="Cannot materialize template"):
            template.materialize()

    def test_materialize_not_idempotent(self):
        """materialize() creates new components each time (not idempotent)."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate()

        result1 = template.materialize()
        result2 = template.materialize()

        # Each call creates a new component instance
        assert result1[0] is not result2[0]
        assert len(result1) == 1
        assert len(result2) == 1

    def test_layout_combines_both_stages(self):
        """layout() calls setup_layout() then materialize()."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate()

        result = template.layout()

        assert template.materialized is not None
        assert isinstance(result, html.Div)
        assert result is template.materialized

    def test_layout_creates_fresh_components(self):
        """Calling layout() multiple times creates new components (not cached)."""
        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate()

        result1 = template.layout()
        result2 = template.layout()

        # Each call creates a new component instance
        assert result1 is not result2
        assert isinstance(result1, html.Div)
        assert isinstance(result2, html.Div)


class TestCustomSubclass:
    """Test creating custom LazyComponent subclasses."""

    def test_custom_component_cls(self):
        """Subclass can override _component_cls."""

        class MyTemplate(LazyComponent):
            _component_cls = html.Div

        template = MyTemplate()
        result = template.materialize()

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 1
        component = result[0]
        # Check it's a Div (implementation detail: check type name)
        assert type(component).__name__ == "Div"

    def test_custom_setup_layout(self):
        """Subclass can override setup_layout()."""
        DivTemplate = _make_lazy_component_cls(html.Div)

        class MyTemplate(LazyComponent):
            _component_cls = html.Div

            def setup_layout(self):
                self.child1 = DivTemplate(_parent=self)
                self.child2 = DivTemplate(_parent=self)
                return self

        template = MyTemplate()
        template.setup_layout()

        assert hasattr(template, "child1")
        assert hasattr(template, "child2")
        assert len(template.children) == 2


class TestCallbackRegistration:
    """Test callback registration system."""

    def test_callbacks_default_implementation(self):
        """Default callbacks() does nothing."""
        template = LazyComponent()

        # Should not raise
        template.callbacks(None)  # type: ignore  # noqa: PGH003

    def test_register_calls_callbacks(self):
        """register() calls callbacks() method."""
        called = []

        class MyTemplate(LazyComponent):
            _component_cls = html.Div

            def callbacks(self, app):
                called.append(True)

        template = MyTemplate()
        template.register(None)  # type: ignore  # noqa: PGH003

        assert called == [True]

    def test_register_is_recursive(self):
        """register() recursively registers children."""
        calls = []

        class MyTemplate(LazyComponent):
            _component_cls = html.Div

            def callbacks(self, app):
                calls.append(self.id)

        root = MyTemplate()
        child1 = MyTemplate(_parent=root)
        child2 = MyTemplate(_parent=root)

        root.register(None)  # type: ignore  # noqa: PGH003

        # Children registered before parent (depth-first)
        assert len(calls) == 3
        assert calls[0] in [child1.id, child2.id]
        assert calls[1] in [child1.id, child2.id]
        assert calls[2] == root.id


class TestResetCounter:
    """Test reset_counter() class method."""

    def test_reset_clears_counter_for_specific_class(self):
        """reset_counter() clears counter for this class only."""
        t1 = LazyComponent()
        assert t1.id == "lazycomponent0"

        t2 = LazyComponent()
        assert t2.id == "lazycomponent1"

        LazyComponent.reset_counter()

        t3 = LazyComponent()
        assert t3.id == "lazycomponent0"  # Counter resets


class TestIntegrationWithIdTree:
    """Test that LazyComponent properly integrates with IdTree."""

    def test_inherits_idtree_properties(self):
        """LazyComponent has all essential tree properties."""
        template = LazyComponent()

        # Check key tree properties exist (exposed via Template)
        assert hasattr(template, "id")
        assert hasattr(template, "parent")
        assert hasattr(template, "children")

    def test_id_is_cached(self):
        """ID property uses caching from IdTree."""
        template = LazyComponent()

        # Access ID multiple times
        id1 = template.id
        id2 = template.id

        # Should be same object (cached)
        assert id1 is id2

    def test_id_cache_invalidates_on_reparent(self):
        """ID cache invalidates when tree structure changes."""
        root1 = LazyComponent()
        root2 = LazyComponent()
        child = LazyComponent(_parent=root1)

        old_id = child.id

        # Reparent
        child.parent = root2

        new_id = child.id
        assert new_id != old_id
