"""Simple counter example demonstrating setup_callbacks pattern.

This example shows:
1. Defining layout structure in __init__ using .child[Type](...) syntax
2. Registering callbacks in setup_callbacks(app) with standard @app.callback
3. Separating business logic into testable pure-Python methods
4. Running multiple independent instances in one app

Run:
    uv run python examples/counter_with_callbacks.py

Then visit http://localhost:8050
"""

from dash import Dash, Input, Output, html

from dash_component_template import Template


class CounterTemplate(Template):
    """A simple counter widget with a customisable multiplication factor."""

    def __init__(self, factor: float = 1.0, label: str = "Count"):
        """Initialize counter template.

        Parameters
        ----------
        factor : float, default 1.0
            Multiplication factor applied to the click count.
        label : str, default "Count"
            Label prefix shown in the display.
        """
        super().__init__()
        self._factor = factor
        self._label = label

        # Wrap everything in a container so layout() returns a single component
        container = self.child[html.Div](
            style={"border": "1px solid #ccc", "padding": "10px"}
        )
        self.button = container.child[html.Button](
            children="Click me", n_clicks=0, style={"margin": "10px"}
        )
        self.display = container.child[html.Div](
            children=f"{label}: 0", style={"margin": "10px", "fontSize": "20px"}
        )

    # ------------------------------------------------------------------ #
    # Business logic — pure Python, no Dash required, fully unit-testable
    # ------------------------------------------------------------------ #

    def compute_display(self, n_clicks: int | None) -> str:
        """Return the formatted display string for a given click count.

        Parameters
        ----------
        n_clicks : int or None
            Number of button clicks.

        Returns
        -------
        str
            Formatted counter string (e.g. ``"Doubled: 10.0"``).
        """
        count = (n_clicks or 0) * self._factor
        return f"{self._label}: {count:.1f}"

    # ------------------------------------------------------------------ #
    # Callback wiring
    # ------------------------------------------------------------------ #

    def setup_callbacks(self, app: Dash) -> None:
        """Register the update callback with standard @app.callback.

        Parameters
        ----------
        app : Dash
            The Dash application instance.
        """

        @app.callback(
            Output(self.display(), "children"),
            Input(self.button(), "n_clicks"),
        )
        def _update(n_clicks: int | None) -> str:
            return self.compute_display(n_clicks)


# ---------------------------------------------------------------------- #
# Quick unit test (no Dash required)
# ---------------------------------------------------------------------- #


def test_counter_logic() -> None:
    """Verify business logic without a running Dash app."""
    c = CounterTemplate(factor=2.0, label="Doubled")
    assert c.compute_display(None) == "Doubled: 0.0"
    assert c.compute_display(0) == "Doubled: 0.0"
    assert c.compute_display(5) == "Doubled: 10.0"
    assert c.compute_display(10) == "Doubled: 20.0"
    print("All counter logic tests passed.")


# ---------------------------------------------------------------------- #
# App factory
# ---------------------------------------------------------------------- #


def create_app() -> Dash:
    """Create a Dash app with three independent counter instances."""
    app = Dash(__name__)

    # Each instance has independent state and auto-scoped IDs
    counter1 = CounterTemplate(factor=1.0, label="Normal")
    counter2 = CounterTemplate(factor=2.0, label="Doubled")
    counter3 = CounterTemplate(factor=0.5, label="Halved")

    app.layout = html.Div(
        children=[
            html.H1("Counter Example — setup_callbacks Pattern"),
            html.P(
                "Each counter has its own isolated state. "
                "Click the buttons to see them update independently."
            ),
            html.Hr(),
            html.Div(
                [counter1.layout(), counter2.layout(), counter3.layout()],
                style={"display": "flex", "gap": "20px", "margin": "10px"},
            ),
        ],
        style={"fontFamily": "Arial, sans-serif", "padding": "20px"},
    )

    # register_callbacks walks the template tree and calls setup_callbacks
    # on every template node, with automatic per-instance ID scoping.
    counter1.register_callbacks(app)
    counter2.register_callbacks(app)
    counter3.register_callbacks(app)

    return app


if __name__ == "__main__":
    test_counter_logic()
    app = create_app()
    print("\nStarting Dash app on http://localhost:8050/")
    print("Press Ctrl+C to stop\n")
    app.run(host="0.0.0.0", port=8050, debug=True)
