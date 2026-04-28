"""Class-level callbacks vs instance-level callbacks.

This example demonstrates the two callback registration patterns:

1. **Instance-scoped** (``setup_callbacks``):
   Each ButtonGroup registers its own callback, applied only to that instance.
   With N instances, N callbacks are registered.

2. **Class-scoped** (``setup_class_callbacks``):
   Registered once per class per app. Uses MATCH/ALL pattern-matching to
   distinguish or aggregate across instances.

After the framework ensures all components within a Template share the same
``_template_id`` (the owning template instance's tree ID), both MATCH isolation
and ALL aggregation work correctly out of the box.

Run:
    uv run python examples/class_level_callbacks.py

Then visit http://localhost:8050
"""

from __future__ import annotations

from dash import ALL, MATCH, Dash, Input, Output, html

from dash_component_template import Template, callback_scope


class ButtonGroup(Template):
    """A labelled button group demonstrating instance-scoped and class-scoped callbacks.

    Components use explicit dict IDs so MATCH/ALL patterns can match them.
    The ``name`` key is the MATCH key (unique within a group, shared in pattern).

    Layout per instance::

        ┌─────────────────────────────┐
        │ [Instance Btn] [Class Btn]  │
        │ Instance counter: 0         │
        │ Class shared counter: 0     │
        └─────────────────────────────┘
    """

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

        # Wrap in a single container so layout() can be used in the app
        wrapper = self.child[html.Div](
            style={
                "border": "1px solid #aaa",
                "borderRadius": "6px",
                "padding": "14px",
                "margin": "10px",
                "minWidth": "260px",
            }
        )
        wrapper.child[html.H4](children=name, style={"margin": "0 0 8px"})

        row = wrapper.child[html.Div](
            style={"display": "flex", "gap": "8px", "marginBottom": "8px"}
        )

        # Every component that needs MATCH/ALL gets an explicit dict id.
        # The "name" key carries the ButtonGroup identity.
        self.instance_btn = row.child[html.Button](
            id={"type": "instance-btn", "name": name},
            children=f"{name}: Instance",
            n_clicks=0,
        )
        self.class_btn = row.child[html.Button](
            id={"type": "class-btn", "name": name},
            children=f"{name}: Class",
            n_clicks=0,
            style={"background": "#5dade2", "color": "white", "border": "none"},
        )

        self.instance_display = wrapper.child[html.Div](
            id={"type": "instance-display", "name": name},
            children=f"{name} instance counter: 0",
        )
        self.class_display = wrapper.child[html.Div](
            id={"type": "class-display", "name": name},
            children=f"{name} class counter: 0",
            style={"color": "#1a5276"},
        )

    # ------------------------------------------------------------------ #
    # Instance-scoped: one callback registered per ButtonGroup instance.
    # Each callback is locked to THIS instance via _template_id in the scope.
    # The MATCH on "name" links buttons to their corresponding display.
    # ------------------------------------------------------------------ #

    def setup_callbacks(self, app: Dash) -> None:
        """Instance-scoped callback: updates THIS group's instance display."""

        @app.callback(
            Output(self.instance_display({"name": MATCH}), "children"),
            Input(self.instance_btn({"name": MATCH}), "n_clicks"),
            prevent_initial_call=True,
        )
        def update_instance(n_clicks: int) -> str:
            return f"{self.name} instance counter: {n_clicks}"

    # ------------------------------------------------------------------ #
    # Class-scoped: registered ONCE per class per app.
    # The framework automatically sets scope to (template=MATCH, template_cls=cls),
    # so the MATCH callback requires no manual callback_scope wrapping.
    # For ALL aggregation an explicit override is needed.
    # ------------------------------------------------------------------ #

    @classmethod
    def setup_class_callbacks(cls, instance: ButtonGroup, app: Dash) -> None:
        """Class-scoped callbacks shared across all ButtonGroup instances.

        Parameters
        ----------
        instance : ButtonGroup
            Representative instance providing access to component structure.
        app : Dash
            Dash application.
        """

        # MATCH: fires when ANY group's class button is clicked.
        # Updates only the class_display of the SAME group (matching "name").
        # No callback_scope wrapper needed — framework sets MATCH scope automatically.
        @app.callback(
            Output(instance.class_display({"name": MATCH}), "children"),
            Input(instance.class_btn({"name": MATCH}), "n_clicks"),
            prevent_initial_call=True,
        )
        def update_class(n_clicks: int) -> str:
            return f"Class counter (any group): {n_clicks}"

        # ALL: fires when ANY group's class button is clicked.
        # Collects n_clicks from ALL groups into a list and computes a total.
        # Requires explicit ALL scope override.
        with callback_scope(template=ALL, template_cls=cls):

            @app.callback(
                Output("aggregate-display", "children"),
                Input(instance.class_btn({"name": ALL}), "n_clicks"),
                prevent_initial_call=True,
            )
            def aggregate(all_clicks: list[int | None]) -> str:
                total = sum(c for c in all_clicks if c)
                return f"Total class clicks (all groups): {total}"


# ---------------------------------------------------------------------- #
# App
# ---------------------------------------------------------------------- #


def create_app() -> Dash:
    """Build the Dash app."""
    app = Dash(__name__)

    # Reset counters so IDs are deterministic in each run
    ButtonGroup.reset_counter()

    group1 = ButtonGroup("Alpha")
    group2 = ButtonGroup("Beta")
    group3 = ButtonGroup("Gamma")

    app.layout = html.Div(
        [
            html.H1("Instance vs Class Callbacks"),
            html.H3("Instance-scoped buttons (blue border = class btn)"),
            html.P(
                "Click 'Instance' buttons — only that group's instance counter updates. "
                "Click 'Class' buttons — all groups' class counters update (one callback)."
            ),
            html.Div(
                [group1.layout(), group2.layout(), group3.layout()],
                style={"display": "flex", "flexWrap": "wrap"},
            ),
            html.Hr(),
            html.H3("Aggregate (ALL pattern)"),
            html.Div(
                id="aggregate-display",
                style={
                    "padding": "12px",
                    "background": "#d6eaf8",
                    "borderRadius": "4px",
                    "fontWeight": "bold",
                },
            ),
            html.Hr(),
            html.Div(
                [
                    html.H4("Callback count comparison"),
                    html.P(
                        [
                            "Instance callbacks registered: ",
                            html.Strong("3"),
                            " (one per group)",
                        ]
                    ),
                    html.P(
                        [
                            "Class callbacks registered: ",
                            html.Strong("1"),
                            " (shared — regardless of instance count)",
                        ]
                    ),
                ],
                style={"background": "#fdfefe", "padding": "10px"},
            ),
        ],
        style={
            "fontFamily": "Arial, sans-serif",
            "padding": "20px",
            "maxWidth": "900px",
        },
    )

    # register_callbacks on each root template:
    # - calls setup_callbacks for EACH instance (instance-scoped)
    # - calls setup_class_callbacks ONCE for the class (class-scoped) on first encounter
    group1.register_callbacks(app)
    group2.register_callbacks(app)
    group3.register_callbacks(app)

    return app


if __name__ == "__main__":
    app = create_app()
    print("\nStarting Dash app on http://localhost:8050/")
    print("Press Ctrl+C to stop\n")
    app.run(host="0.0.0.0", port=8050, debug=True)
