"""Bare Dash counter — same layout as CounterTemplate in app.py, no framework.

Apple-to-apple comparison for callback latency vs the framework version.
Open http://localhost:8051/ and use the Dash debug callback graph to compare.

Run:
    uv run python examples/bare_counter.py
"""

from dash import Dash, Input, Output, html

app = Dash(__name__)


def _counter_layout(prefix: str, label: str) -> html.Div:
    """Replicate the exact same DOM structure as CounterTemplate."""
    return html.Div(
        style={
            "border": "1px solid #ccc",
            "borderRadius": "8px",
            "padding": "15px",
            "margin": "10px",
            "minWidth": "200px",
        },
        children=[
            html.H4(children=label, style={"margin": "0 0 10px 0"}),
            html.Button(
                id=f"{prefix}-button",
                children="Increment",
                n_clicks=0,
                style={"marginBottom": "10px"},
            ),
            html.Div(
                id=f"{prefix}-display",
                children=f"{label}: 0.0",
                style={"fontSize": "18px", "fontWeight": "bold"},
            ),
        ],
    )


app.layout = html.Div(
    [
        html.H1(
            "Bare counter — no framework",
            style={"borderBottom": "2px solid #333", "paddingBottom": "10px"},
        ),
        html.P(
            "Same component tree as Tab 1 in app.py. Use the Dash debug callback graph to compare latency."
        ),
        html.Div(
            [
                _counter_layout("c1", "Normal ×1"),
                _counter_layout("c2", "Doubled ×2"),
                _counter_layout("c3", "Halved ×0.5"),
            ],
            style={"display": "flex", "flexWrap": "wrap"},
        ),
    ]
)


@app.callback(Output("c1-display", "children"), Input("c1-button", "n_clicks"))
def _update_c1(n):
    return f"Normal ×1: {(n or 0) * 1.0:.1f}"


@app.callback(Output("c2-display", "children"), Input("c2-button", "n_clicks"))
def _update_c2(n):
    return f"Doubled ×2: {(n or 0) * 2.0:.1f}"


@app.callback(Output("c3-display", "children"), Input("c3-button", "n_clicks"))
def _update_c3(n):
    return f"Halved ×0.5: {(n or 0) * 0.5:.1f}"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8051)
