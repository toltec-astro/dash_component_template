"""Tests for callback_scope context manager and scope mechanics.

These tests verify that callback_scope properly manages the scope stack,
merges nested scopes, and handles MATCH/ALL patterns correctly.
"""

from dash import ALL, MATCH

from dash_component_template import Template
from dash_component_template.template import _get_current_scope, callback_scope


class TestCallbackScopeBasics:
    """Test basic callback_scope functionality."""

    def test_empty_scope_when_no_context(self):
        """_get_current_scope should return empty dict when no scope active."""
        scope = _get_current_scope()
        assert scope == {}

    def test_basic_scope_with_template_name(self):
        """callback_scope should set _template_name."""
        with callback_scope(_template_name="MyTemplate"):
            scope = _get_current_scope()
            assert scope["_template_name"] == "MyTemplate"

    def test_basic_scope_with_template_id(self):
        """callback_scope should set _template_id."""
        with callback_scope(_template_id="MyTemplate_0"):
            scope = _get_current_scope()
            assert scope["_template_id"] == "MyTemplate_0"

    def test_basic_scope_with_both(self):
        """callback_scope should set both _template_name and _template_id."""
        with callback_scope(_template_name="MyTemplate", _template_id="MyTemplate_0"):
            scope = _get_current_scope()
            assert scope["_template_name"] == "MyTemplate"
            assert scope["_template_id"] == "MyTemplate_0"

    def test_scope_clears_after_exit(self):
        """Scope should be cleared after exiting context."""
        with callback_scope(_template_name="MyTemplate"):
            assert _get_current_scope() != {}

        # Should be empty after exit
        assert _get_current_scope() == {}

    def test_scope_clears_even_on_exception(self):
        """Scope should be cleared even if exception occurs."""
        try:
            with callback_scope(_template_name="MyTemplate"):
                assert _get_current_scope() != {}
                raise ValueError("test exception")  # noqa: TRY301
        except ValueError:
            pass

        # Should be empty after exception
        assert _get_current_scope() == {}


class TestCallbackScopeNesting:
    """Test nested callback_scope contexts."""

    def test_nested_scopes_merge(self):
        """Nested scopes should merge, with inner scope taking precedence."""
        with callback_scope(_template_name="Outer"):
            outer_scope = _get_current_scope()
            assert outer_scope["_template_name"] == "Outer"

            with callback_scope(_template_id="Inner_0"):
                inner_scope = _get_current_scope()
                # Should have both
                assert inner_scope["_template_name"] == "Outer"
                assert inner_scope["_template_id"] == "Inner_0"

            # Back to outer scope
            back_to_outer = _get_current_scope()
            assert back_to_outer["_template_name"] == "Outer"
            assert "_template_id" not in back_to_outer

    def test_nested_scope_overrides(self):
        """Inner scope should override outer scope for same key."""
        with callback_scope(_template_name="Outer", _template_id="Outer_0"):  # noqa: SIM117
            with callback_scope(_template_name="Inner"):
                scope = _get_current_scope()
                # Inner overrides _template_name
                assert scope["_template_name"] == "Inner"
                # But keeps _template_id from outer
                assert scope["_template_id"] == "Outer_0"

    def test_triple_nesting(self):
        """Test three levels of nesting."""
        with callback_scope(_template_name="L1"):
            assert _get_current_scope()["_template_name"] == "L1"

            with callback_scope(_template_id="L2_id"):
                scope2 = _get_current_scope()
                assert scope2["_template_name"] == "L1"
                assert scope2["_template_id"] == "L2_id"

                with callback_scope(_template_name="L3"):
                    scope3 = _get_current_scope()
                    # L3 overrides _template_name
                    assert scope3["_template_name"] == "L3"
                    # L2_id still present
                    assert scope3["_template_id"] == "L2_id"

                # Back to L2
                assert _get_current_scope()["_template_name"] == "L1"

            # Back to L1
            assert "_template_id" not in _get_current_scope()


class TestCallbackScopeWithMATCH:
    """Test callback_scope with MATCH pattern."""

    def test_scope_with_match_template_id(self):
        """callback_scope should support MATCH for _template_id."""
        with callback_scope(_template_id=MATCH):
            scope = _get_current_scope()
            assert scope["_template_id"] == MATCH

    def test_scope_with_match_template_name(self):
        """callback_scope should support MATCH for _template_name."""
        with callback_scope(_template_name=MATCH):
            scope = _get_current_scope()
            assert scope["_template_name"] == MATCH

    def test_scope_with_both_match(self):
        """callback_scope should support MATCH for both fields."""
        with callback_scope(_template_name=MATCH, _template_id=MATCH):
            scope = _get_current_scope()
            assert scope["_template_name"] == MATCH
            assert scope["_template_id"] == MATCH


class TestCallbackScopeWithALL:
    """Test callback_scope with ALL pattern."""

    def test_scope_with_all_template_id(self):
        """callback_scope should support ALL for _template_id."""
        with callback_scope(_template_id=ALL):
            scope = _get_current_scope()
            assert scope["_template_id"] == ALL

    def test_scope_with_all_template_name(self):
        """callback_scope should support ALL for _template_name."""
        with callback_scope(_template_name=ALL):
            scope = _get_current_scope()
            assert scope["_template_name"] == ALL

    def test_scope_with_mixed_match_all(self):
        """callback_scope should support mixing MATCH and ALL."""
        with callback_scope(_template_name=MATCH, _template_id=ALL):
            scope = _get_current_scope()
            assert scope["_template_name"] == MATCH
            assert scope["_template_id"] == ALL


class TestCallbackScopeConvenienceMethods:
    """Test convenience parameters for callback_scope."""

    def test_template_parameter(self):
        """template parameter should set _template_id from template.id."""
        template = Template()

        with callback_scope(template=template):
            scope = _get_current_scope()
            assert scope["_template_id"] == template.id

    def test_template_parameter_with_match(self):
        """template=MATCH should set _template_id=MATCH."""
        with callback_scope(template=MATCH):
            scope = _get_current_scope()
            assert scope["_template_id"] == MATCH

    def test_template_cls_parameter(self):
        """template_cls parameter should set _template_name from class."""

        class MyTemplate(Template):
            pass

        with callback_scope(template_cls=MyTemplate):
            scope = _get_current_scope()
            # Uses __qualname__ which includes nested path
            assert (
                scope["_template_name"]
                == "TestCallbackScopeConvenienceMethods.test_template_cls_parameter.<locals>.MyTemplate"  # noqa: E501
            )

    def test_template_cls_parameter_with_match(self):
        """template_cls=MATCH should set _template_name=MATCH."""
        with callback_scope(template_cls=MATCH):
            scope = _get_current_scope()
            assert scope["_template_name"] == MATCH

    def test_both_convenience_parameters(self):
        """Both template and template_cls should work together."""

        class MyTemplate(Template):
            pass

        template = MyTemplate()

        with callback_scope(template=template, template_cls=MyTemplate):
            scope = _get_current_scope()
            assert scope["_template_id"] == template.id
            # Uses __qualname__ which includes nested path
            assert (
                scope["_template_name"]
                == "TestCallbackScopeConvenienceMethods.test_both_convenience_parameters.<locals>.MyTemplate"  # noqa: E501
            )

    def test_convenience_overrides_direct(self):
        """Direct _template_* parameters should override convenience parameters."""

        class MyTemplate(Template):
            pass

        template = MyTemplate()

        # Direct parameters take precedence
        with callback_scope(
            template=template,
            template_cls=MyTemplate,
            _template_id="custom_id",
            _template_name="CustomName",
        ):
            scope = _get_current_scope()
            assert scope["_template_id"] == "custom_id"
            assert scope["_template_name"] == "CustomName"


class TestCallbackScopeEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_scope_context(self):
        """Empty callback_scope should not add anything."""
        with callback_scope():
            scope = _get_current_scope()
            assert scope == {}

    def test_arbitrary_keys_allowed(self):
        """callback_scope should allow arbitrary keys (for extensibility)."""
        with callback_scope(custom_key="custom_value", another=42):
            scope = _get_current_scope()
            assert scope["custom_key"] == "custom_value"
            assert scope["another"] == 42

    def test_multiple_context_managers_same_level(self):
        """Multiple scope contexts at same level should work independently."""
        # First context
        with callback_scope(_template_name="First"):
            assert _get_current_scope()["_template_name"] == "First"

        # Second context (independent)
        with callback_scope(_template_name="Second"):
            assert _get_current_scope()["_template_name"] == "Second"

        # Both should be cleared
        assert _get_current_scope() == {}

    def test_scope_with_none_value(self):
        """callback_scope should handle None values."""
        with callback_scope(_template_name=None):
            scope = _get_current_scope()
            assert scope["_template_name"] is None


class TestCallbackScopeIntegration:
    """Test callback_scope integration with LazyComponent."""

    def test_scope_affects_component_id_creation(self):
        """callback_scope should affect dict ID creation in components."""
        from dash import html

        from dash_component_template.lazy_component import _make_lazy_component_cls

        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate(id={"type": "btn", "index": 0})

        # Without scope - uses defaults
        template.materialize()
        default_id = template.materialized.id
        assert "_template_name" in default_id
        assert "_template_id" in default_id

        # Reset for next test
        template._materialized = None

        # With scope - should override defaults
        with callback_scope(_template_name="OverrideName", _template_id="override_123"):
            template.materialize()
            scoped_id = template.materialized.id
            assert scoped_id["_template_name"] == "OverrideName"
            assert scoped_id["_template_id"] == "override_123"

    def test_scope_affects_call_operator(self):
        """callback_scope should affect __call__() ID generation."""
        from dash import MATCH, html

        from dash_component_template.lazy_component import _make_lazy_component_cls

        DivTemplate = _make_lazy_component_cls(html.Div)
        template = DivTemplate(id={"type": "btn", "index": 0})
        template.materialize()

        # Without scope
        result1 = template({"index": MATCH})
        assert "_template_name" in result1
        assert "_template_id" in result1

        # With scope - should override
        with callback_scope(_template_name="ScopedName", _template_id=MATCH):
            result2 = template({"index": MATCH})
            assert result2["_template_name"] == "ScopedName"
            assert result2["_template_id"] == MATCH


class TestThreadSafety:
    """Test thread-local behavior of callback_scope."""

    def test_scope_is_thread_local(self):
        """Each thread should have independent scope stack."""
        import threading

        results = {}

        def thread1_work():
            with callback_scope(_template_name="Thread1"):
                # Sleep to ensure overlap
                import time

                time.sleep(0.01)
                results["thread1"] = _get_current_scope()

        def thread2_work():
            with callback_scope(_template_name="Thread2"):
                # Sleep to ensure overlap
                import time

                time.sleep(0.01)
                results["thread2"] = _get_current_scope()

        t1 = threading.Thread(target=thread1_work)
        t2 = threading.Thread(target=thread2_work)

        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # Each thread should see its own scope
        assert results["thread1"]["_template_name"] == "Thread1"
        assert results["thread2"]["_template_name"] == "Thread2"

        # Main thread should have empty scope
        assert _get_current_scope() == {}
