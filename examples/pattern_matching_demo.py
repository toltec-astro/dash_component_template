"""Pattern-matching callbacks with multiple options per template.

This example shows how to use dict IDs and MATCH to handle N similar
components within a template with a single callback definition.

Scenario: A ``PollWidget`` template with N voting options.
- Each option has a *Vote* button and a vote-count display.
- ONE callback (using MATCH on ``index``) handles all N options.
- Two independent polls coexist without interfering.

Key concepts
------------
1. Declare components with explicit dict IDs::

       self.btn = row.child[html.Button](
           id={"type": "poll-btn", "index": i}, ...
       )

2. In ``setup_callbacks`` use any representative component with MATCH::

       Output(self.counts[0]({"index": MATCH}), "children"),
       Input(self.btns[0]({"index": MATCH}),   "n_clicks"),

   The framework injects ``_template_id`` (the owning Template's tree ID)
   into every component at materialisation time, ensuring each PollWidget
   instance is isolated from the other without any extra user code.

3. ``component({"index": MATCH})``:
   - Copies the materialised dict ID
   - Replaces ``"index"`` with ``MATCH``
   - Keeps ``_template_id`` (same for all components in this instance)
   The resulting pattern matches every option *within* this instance but
   none of the other instance's options.

Run:
    uv run python examples/pattern_matching_demo.py

Then visit http://localhost:8050
"""

from __future__ import annotations

from dash import MATCH, Dash, Input, Output, html

from dash_component_template import Template


class PollWidget(Template):
    """Poll with N voting options — one callback handles all via MATCH.

    Each option has:
    - ``btns[i]``   ``html.Button`` with id ``{"type": "poll-btn", "index": i}``
    - ``counts[i]`` ``html.Div``    with id ``{"type": "poll-cnt", "index": i}``

    A single callback updates the count for the clicked option.
    Multiple ``PollWidget`` instances are isolated automatically.
    """

    def __init__(self, question: str, options: list[str]) -> None:
        super().__init__()

        wrapper = self.child[html.Div](
            style={
                "border": "2px solid #2980b9",
                "borderRadius": "8px",
                "padding": "16px",
                "margin": "12px",
                "minWidth": "280px",
            }
        )
        wrapper.child[html.H3](children=question, style={"margin": "0 0 12px"})

        self.btns: list = []
        self.counts: list = []

        for i, option in enumerate(options):
            row = wrapper.child[html.Div](
                style={
                    "display": "flex",
                    "gap": "10px",
                    "alignItems": "center",
                    "margin": "6px 0",
                }
            )
            btn = row.child[html.Button](
                # Explicit dict ID with "index" key for MATCH pattern
                id={"type": "poll-btn", "index": i},
                children=f"Vote: {option}",
                n_clicks=0,
                style={"padding": "6px 14px", "cursor": "pointer", "minWidth": "130px"},
            )
            count = row.child[html.Div](
                id={"type": "poll-cnt", "index": i},
                children="0 votes",
                style={"color": "#555"},
            )
            self.btns.append(btn)
            self.counts.append(count)

    def setup_callbacks(self, app: Dash) -> None:
        """One MATCH callback handles all N options.

        Notes
        -----
        ``self.btns[0]`` is used as a *representative* object — its ``type``
        and the injected ``_template_id`` are what matter; the ``index: 0``
        value is replaced by ``MATCH``.  Dash fires the callback for any
        matching button, and the corresponding count (same matching ``index``)
        is updated.
        """

        @app.callback(
            Output(self.counts[0]({"index": MATCH}), "children"),
            Input(self.btns[0]({"index": MATCH}), "n_clicks"),
        )
        def update_vote(n_clicks: int | None) -> str:
            return f"{n_clicks or 0} votes"


# ----------------------------------------------------------------------- #
# App
# ----------------------------------------------------------------------- #


def create_app() -> Dash:
    """Build a Dash app with two independent polls."""
    app = Dash(__name__)

    poll1 = PollWidget(
        question="Favourite Python web framework?",
        options=["Dash", "Flask", "FastAPI"],
    )
    poll2 = PollWidget(
        question="Preferred data format?",
        options=["JSON", "YAML", "TOML"],
    )

    app.layout = html.Div(
        [
            html.H1("Pattern-Matching Callbacks Demo"),
            html.P(
                "Each poll uses one MATCH callback for all its options. "
                "The two polls are automatically isolated by their _template_id."
            ),
            html.Div(
                [poll1.layout(), poll2.layout()],
                style={"display": "flex", "flexWrap": "wrap"},
            ),
            html.Hr(),
            html.H4("How it works"),
            html.Pre(
                """# Components declared with explicit dict IDs:
self.btn = row.child[html.Button](
    id={"type": "poll-btn", "index": i}, ...
)

# In setup_callbacks — ONE callback for all N options:
@app.callback(
    Output(self.counts[0]({"index": MATCH}), "children"),
    Input(self.btns[0]({"index": MATCH}),   "n_clicks"),
)
def update_vote(n_clicks):
    return f"{n_clicks or 0} votes"

# Framework injects _template_id automatically:
# Materialised btn ID:  {"type": "poll-btn", "index": 2,
#                        "_template_id": "pollwidget0", ...}
# Callback Output:      {"type": "poll-cnt", "index": MATCH,
#                        "_template_id": "pollwidget0", ...}
# -> only matches poll1's components, never poll2's""",
                style={
                    "background": "#f4f4f4",
                    "padding": "12px",
                    "fontSize": "13px",
                    "borderRadius": "4px",
                    "overflowX": "auto",
                },
            ),
        ],
        style={
            "fontFamily": "Arial, sans-serif",
            "padding": "24px",
            "maxWidth": "860px",
        },
    )

    poll1.register_callbacks(app)
    poll2.register_callbacks(app)

    return app


if __name__ == "__main__":
    app = create_app()
    print("\nStarting Dash app on http://localhost:8050/")
    print("Press Ctrl+C to stop\n")
    app.run(host="0.0.0.0", port=8050, debug=True)
