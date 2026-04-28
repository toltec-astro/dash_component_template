"""Comprehensive dash_component_template v5.0.2 Demo.

All four key API patterns in one tabbed application, with the root layout
itself defined as a Template — no manual html.Div([...]) assembly required.
A single register_callbacks(app) call propagates to all sub-templates.

  Tab 1 — Basic Callbacks:       setup_callbacks() with instance-scoped callbacks
  Tab 2 — Template Composition:  all three .child() patterns
  Tab 3 — Pattern Matching:      MATCH/ALL with automatic scope injection
  Tab 4 — Class Callbacks:       setup_class_callbacks() shared across instances

Run:
    uv run python examples/app.py
    # or from examples/ directory:
    python app.py

Then open http://localhost:8050/ in your browser.
"""

from dash import ALL, MATCH, Dash, Input, Output, dcc, html

from dash_component_template import Template, callback_scope

# ── Tab 1: Basic Callbacks ────────────────────────────────────────────────────


class CounterTemplate(Template):
    """Counter demonstrating setup_callbacks() and business-logic separation."""

    def __init__(self, factor: float = 1.0, label: str = "Count"):
        super().__init__()
        self._factor = factor
        self._label = label
        container = self.child[html.Div](
            style={
                "border": "1px solid #ccc",
                "borderRadius": "8px",
                "padding": "15px",
                "margin": "10px",
                "minWidth": "200px",
            }
        )
        container.child[html.H4](children=label, style={"margin": "0 0 10px 0"})
        self.button = container.child[html.Button](
            children="Increment", n_clicks=0, style={"marginBottom": "10px"}
        )
        self.display = container.child[html.Div](
            children=f"{label}: 0.0",
            style={"fontSize": "18px", "fontWeight": "bold"},
        )

    def calculate(self, n_clicks: int) -> str:
        """Pure business logic — testable without Dash."""
        n = n_clicks or 0
        return f"{self._label}: {n * self._factor:.1f}"

    def setup_callbacks(self, app) -> None:
        @app.callback(
            Output(self.display(), "children"),
            Input(self.button(), "n_clicks"),
        )
        def _update(n_clicks):
            return self.calculate(n_clicks)


# ── Tab 2: Template Composition ───────────────────────────────────────────────


class InfoCard(Template):
    """Reusable card — used in CompositionDemo as a composed sub-template."""

    def __init__(self, title: str, color: str = "#fff"):
        super().__init__()
        card = self.child[html.Div](
            style={
                "border": "1px solid #ddd",
                "borderRadius": "8px",
                "padding": "15px",
                "margin": "10px",
                "backgroundColor": color,
            }
        )
        card.child[html.H4](children=title, style={"margin": "0 0 8px 0"})
        self.body = card.child[html.Div]()


class CompositionDemo(Template):
    """Demonstrates all three .child() patterns in one template."""

    def __init__(self):
        super().__init__()
        wrapper = self.child[html.Div]()

        # ── Pattern 3: .child(template_instance) ──────────────────────────────
        card1 = InfoCard("Pattern 1: .child[Type](props)", color="#e8f5e9")
        wrapper.child(card1)
        card1.body.child[html.Code](
            children="btn = self.child[html.Button](children='Click')"
        )
        card1.body.child[html.P](
            children=(
                "Factory pattern. IDE autocomplete for all component props "
                "is provided by generated .pyi stub files."
            )
        )

        # ── Pattern 2: .child(existing_component) ─────────────────────────────
        existing = html.Div(
            [
                html.Strong("Pattern 2: .child(existing_component)"),
                html.Br(),
                html.Code("root.child(html.Div('Already created'))"),
                html.P(
                    "Wraps any existing Dash component instance inside the template tree.",
                    style={"margin": "4px 0 0 0"},
                ),
            ],
            style={
                "border": "1px solid #ddd",
                "borderRadius": "8px",
                "padding": "15px",
                "margin": "10px",
                "backgroundColor": "#fff3e0",
            },
        )
        wrapper.child(existing)

        # ── Pattern 3: .child(template_instance) ──────────────────────────────
        card3 = InfoCard("Pattern 3: .child(template_instance)", color="#e3f2fd")
        wrapper.child(card3)
        card3.body.child[html.Code](children="root.child(NavTemplate())")
        card3.body.child[html.P](
            children=(
                "Compose Template subclasses hierarchically. "
                "Callbacks defined in each sub-template are registered automatically."
            )
        )


# ── Tab 3: Pattern Matching ───────────────────────────────────────────────────


class CounterGroup(Template):
    """Multiple counters sharing one MATCH-scoped callback per instance."""

    def __init__(self, num_counters: int = 3, name: str = "Group"):
        super().__init__()
        outer = self.child[html.Div](
            style={
                "border": "1px solid #ccc",
                "borderRadius": "8px",
                "padding": "15px",
                "margin": "10px",
                "minWidth": "200px",
            }
        )
        outer.child[html.H4](children=name, style={"margin": "0 0 10px 0"})
        self.buttons: list = []
        self.displays: list = []
        for i in range(num_counters):
            row = outer.child[html.Div](
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "marginBottom": "6px",
                }
            )
            btn = row.child[html.Button](
                id={"type": "pm-btn", "index": i},
                children=f"Button {i}",
                n_clicks=0,
                style={"marginRight": "10px", "minWidth": "80px"},
            )
            disp = row.child[html.Span](
                id={"type": "pm-disp", "index": i},
                children="0 clicks",
            )
            self.buttons.append(btn)
            self.displays.append(disp)

    def setup_callbacks(self, app) -> None:
        # One callback for ALL buttons in this group.
        # MATCH matches any index; _template_id scopes this to this instance only.
        @app.callback(
            Output(self.displays[0]({"index": MATCH}), "children"),
            Input(self.buttons[0]({"index": MATCH}), "n_clicks"),
        )
        def _update(n_clicks):
            return f"{n_clicks or 0} clicks"


# ── Tab 4: Class-Level Callbacks ──────────────────────────────────────────────


class ButtonGroup(Template):
    """Instance vs class-level callback registration."""

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        container = self.child[html.Div](
            style={
                "border": "1px solid #ddd",
                "borderRadius": "4px",
                "padding": "10px",
                "marginBottom": "8px",
            }
        )
        container.child[html.Strong](children=f"{name}:")
        self.inst_btn = container.child[html.Button](
            id={"type": "bg-inst-btn", "name": name},
            children="Instance",
            n_clicks=0,
            style={"margin": "0 8px"},
        )
        self.inst_disp = container.child[html.Span](
            id={"type": "bg-inst-disp", "name": name},
            children="0",
            style={"marginRight": "20px"},
        )
        self.cls_btn = container.child[html.Button](
            id={"type": "bg-cls-btn", "name": name},
            children="Class",
            n_clicks=0,
            style={"margin": "0 8px"},
        )
        self.cls_disp = container.child[html.Span](
            id={"type": "bg-cls-disp", "name": name},
            children="0",
        )

    def setup_callbacks(self, app) -> None:
        """Registered once per instance — scoped to this instance's _template_id."""

        @app.callback(
            Output(self.inst_disp({"name": MATCH}), "children"),
            Input(self.inst_btn({"name": MATCH}), "n_clicks"),
            prevent_initial_call=True,
        )
        def _update_inst(n_clicks):
            return str(n_clicks)

    @classmethod
    def setup_class_callbacks(cls, instance, app) -> None:
        """Registered once per class — automatic MATCH scope, no wrapper needed."""

        # MATCH scope is automatically set for _template_id by register_callbacks().
        # This callback is triggered by any ButtonGroup instance's cls_btn.
        @app.callback(
            Output(instance.cls_disp({"name": MATCH}), "children"),
            Input(instance.cls_btn({"name": MATCH}), "n_clicks"),
            prevent_initial_call=True,
        )
        def _update_cls(n_clicks):
            return str(n_clicks or 0)

        # ALL pattern: aggregate across ALL instances — needs explicit scope override.
        with callback_scope(template=ALL, template_cls=cls):

            @app.callback(
                Output("bg-total", "children"),
                Input(instance.cls_btn({"name": ALL}), "n_clicks"),
                prevent_initial_call=True,
            )
            def _aggregate(all_clicks):
                total = sum(c for c in all_clicks if c)
                return f"Total class clicks across all groups: {total}"


# ── Root App Template ─────────────────────────────────────────────────────────


class AppTemplate(Template):
    """Root application template — builds the entire app layout as a template tree.

    Demonstrates that even the top-level layout needs no manual html.Div([...])
    assembly. All sub-templates are composed via .child() patterns.
    A single register_callbacks(app) call propagates to every sub-template.
    """

    def __init__(self) -> None:
        super().__init__()

        root = self.child[html.Div](
            style={
                "fontFamily": "Arial, sans-serif",
                "maxWidth": "1100px",
                "margin": "0 auto",
                "padding": "20px",
            }
        )
        root.child[html.H1](
            children="dash_component_template v5.0.2",
            style={"borderBottom": "2px solid #333", "paddingBottom": "10px"},
        )
        root.child[html.P](
            children=[
                "Feature demo covering all major API patterns. See ",
                html.Code("design/architecture.md"),
                " for complete documentation.",
            ]
        )

        tabs = root.child[dcc.Tabs](value="tab-1")

        self._build_tab1(tabs)
        self._build_tab2(tabs)
        self._build_tab3(tabs)
        self._build_tab4(tabs)

    # ── Tab builders ──────────────────────────────────────────────────────────

    def _build_tab1(self, tabs) -> None:
        """Tab 1: Basic Callbacks."""
        tab = tabs.child[dcc.Tab](label="1. Basic Callbacks", value="tab-1")
        tab.child[html.H3](children="Counter with setup_callbacks() Pattern")
        tab.child[html.P](
            children=(
                "Three independent instances — each has its own auto-generated ID "
                "namespace and separate callback wiring."
            )
        )

        counters_row = tab.child[html.Div](
            style={"display": "flex", "flexWrap": "wrap"}
        )
        self.c1 = CounterTemplate(1.0, "Normal ×1")
        self.c2 = CounterTemplate(2.0, "Doubled ×2")
        self.c3 = CounterTemplate(0.5, "Halved ×0.5")
        counters_row.child(self.c1)
        counters_row.child(self.c2)
        counters_row.child(self.c3)

        tab.child(
            html.Div(
                [
                    html.H4("How it works", style={"marginTop": "0"}),
                    html.Ul(
                        [
                            html.Li(
                                [
                                    html.Code("setup_callbacks(app)"),
                                    " — define @app.callback using the standard Dash API",
                                ]
                            ),
                            html.Li(
                                [
                                    html.Code("self.button()"),
                                    " and ",
                                    html.Code("self.display()"),
                                    " — return auto-scoped component IDs",
                                ]
                            ),
                            html.Li(
                                [
                                    html.Code("register_callbacks(app)"),
                                    " — walks the template tree, calls setup_callbacks() on all nodes",
                                ]
                            ),
                            html.Li(
                                "Business logic in calculate() is pure Python — testable without Dash"
                            ),
                        ]
                    ),
                ],
                style={
                    "backgroundColor": "#f5f5f5",
                    "padding": "15px",
                    "borderRadius": "4px",
                    "marginTop": "15px",
                },
            )
        )

    def _build_tab2(self, tabs) -> None:
        """Tab 2: Template Composition — all three .child() patterns."""
        tab = tabs.child[dcc.Tab](label="2. Composition", value="tab-2")
        tab.child[html.H3](children="Three .child() Patterns")

        self.comp_demo = CompositionDemo()
        tab.child(self.comp_demo)

        tab.child(
            html.Div(
                [
                    html.H4("Pattern summary", style={"marginTop": "0"}),
                    html.Ul(
                        [
                            html.Li(
                                [
                                    html.Code(
                                        "self.child[html.Button](children='Click')"
                                    ),
                                    " — factory, IDE autocomplete via .pyi stubs",
                                ]
                            ),
                            html.Li(
                                [
                                    html.Code("self.child(existing_component)"),
                                    " — wrap any Dash component instance",
                                ]
                            ),
                            html.Li(
                                [
                                    html.Code("self.child(MyTemplate())"),
                                    " — compose Template subclasses hierarchically",
                                ]
                            ),
                        ]
                    ),
                ],
                style={
                    "backgroundColor": "#f5f5f5",
                    "padding": "15px",
                    "borderRadius": "4px",
                    "marginTop": "15px",
                },
            )
        )

    def _build_tab3(self, tabs) -> None:
        """Tab 3: Pattern-Matching Callbacks with Automatic Scope Injection."""
        tab = tabs.child[dcc.Tab](label="3. Pattern Matching", value="tab-3")
        tab.child[html.H3](
            children="Pattern-Matching Callbacks with Automatic Scope Injection"
        )
        tab.child[html.P](
            children=[
                "Each group's buttons have dict IDs like ",
                html.Code('{"type": "pm-btn", "index": 0}'),
                ". The framework automatically injects ",
                html.Code("_template_name"),
                " and ",
                html.Code("_template_id"),
                " so Group A's callbacks never match Group B's buttons.",
            ]
        )

        groups_row = tab.child[html.Div](style={"display": "flex", "flexWrap": "wrap"})
        self.group_a = CounterGroup(3, "Group A")
        self.group_b = CounterGroup(2, "Group B")
        groups_row.child(self.group_a)
        groups_row.child(self.group_b)

        tab.child(
            html.Div(
                [
                    html.H4(
                        "Actual ID after scope injection", style={"marginTop": "0"}
                    ),
                    html.Code(
                        '{"type": "pm-btn", "index": MATCH, '
                        '"_template_name": "CounterGroup", "_template_id": "countergroup0"}'
                    ),
                    html.P(
                        "Group A's callback uses _template_id='countergroup0', "
                        "Group B's uses 'countergroup1' — complete isolation."
                    ),
                ],
                style={
                    "backgroundColor": "#f5f5f5",
                    "padding": "15px",
                    "borderRadius": "4px",
                    "marginTop": "15px",
                },
            )
        )

    def _build_tab4(self, tabs) -> None:
        """Tab 4: Instance vs Class-Level Callbacks."""
        tab = tabs.child[dcc.Tab](label="4. Class Callbacks", value="tab-4")
        tab.child[html.H3](children="Instance vs Class-Level Callbacks")
        tab.child(
            html.Div(
                [
                    html.Strong("Instance button"),
                    ": each group has its own counter — ",
                    html.Em("3 separate callbacks registered"),
                    html.Span(" (one per ButtonGroup instance)."),
                    html.Br(),
                    html.Strong("Class button"),
                    ": one shared callback matches all groups — ",
                    html.Em("registered once"),
                    html.Span(" via setup_class_callbacks()."),
                ],
                style={"marginBottom": "15px"},
            )
        )

        bg_groups = tab.child[html.Div]()
        self.bg1 = ButtonGroup("Alpha")
        self.bg2 = ButtonGroup("Beta")
        self.bg3 = ButtonGroup("Gamma")
        bg_groups.child(self.bg1)
        bg_groups.child(self.bg2)
        bg_groups.child(self.bg3)

        # Static id required by ButtonGroup.setup_class_callbacks ALL-pattern callback
        tab.child[html.Div](
            id="bg-total",
            children="Click a Class button to see aggregate",
            style={
                "marginTop": "10px",
                "padding": "10px",
                "backgroundColor": "#e3f2fd",
                "borderRadius": "4px",
                "fontWeight": "bold",
            },
        )
        tab.child(
            html.Div(
                [
                    html.H4("Performance note", style={"marginTop": "0"}),
                    html.P(
                        "With 100 ButtonGroup instances: "
                        "instance pattern = 100 callbacks; class pattern = 1 callback."
                    ),
                    html.Code("setup_class_callbacks(cls, instance, app)"),
                    html.Span(
                        " — called once per class per app, not once per instance."
                    ),
                ],
                style={
                    "backgroundColor": "#f5f5f5",
                    "padding": "15px",
                    "borderRadius": "4px",
                    "marginTop": "15px",
                },
            )
        )


# ── App Assembly ──────────────────────────────────────────────────────────────


def create_app() -> Dash:
    """Create and return the Dash application."""
    app = Dash(__name__, suppress_callback_exceptions=True)

    root = AppTemplate()
    app.layout = root.layout()
    root.register_callbacks(app)

    return app


if __name__ == "__main__":
    app = create_app()
    print("\nStarting dash_component_template comprehensive demo")
    print("Visit:  http://localhost:8050/")
    print("Press Ctrl+C to stop\n")
    app.run(host="0.0.0.0", port=8050, debug=True)
