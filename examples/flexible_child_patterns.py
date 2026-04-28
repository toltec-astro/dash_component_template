"""Three ways to add children to a template.

This example demonstrates all three child-addition patterns:

1. **Factory pattern** ``template.child[ComponentType](**props)``
   The primary pattern. Creates a typed LazyComponent with IDE autocomplete.

2. **Wrap existing component** ``template.child(existing_component)``
   Integrates pre-built Dash components into the template tree.

3. **Adopt template instance** ``template.child(other_template)``
   Composes reusable template objects into a parent layout tree.

Run:
    uv run python examples/flexible_child_patterns.py

Then visit http://localhost:8050
"""

from dash import Dash, html

from dash_component_template import Template

# ----------------------------------------------------------------------- #
# Reusable sub-templates (Pattern 3 building blocks)
# ----------------------------------------------------------------------- #


class HeaderTemplate(Template):
    """Page header with a title and a subtitle."""

    def __init__(self, title: str = "Flexible Child Patterns Demo") -> None:
        super().__init__()
        # Pattern 1 — factory syntax with keyword props
        self.title = self.child[html.H1](
            children=title,
            style={"color": "#2c3e50"},
        )
        self.subtitle = self.child[html.P](
            children="Three ways to compose component trees",
            style={"color": "#7f8c8d"},
        )


class FooterTemplate(Template):
    """Simple page footer."""

    def __init__(self) -> None:
        super().__init__()
        self.child[html.Footer](
            children="dash-component-template — flexible by design",
            style={"borderTop": "1px solid #ccc", "padding": "10px", "color": "#999"},
        )


# ----------------------------------------------------------------------- #
# Page layout using all three patterns
# ----------------------------------------------------------------------- #


def build_page() -> Template:
    """Assemble a full page using all three child patterns."""
    root = Template()

    # --- Pattern 3: adopt existing template instances ---
    header = HeaderTemplate()
    root.child(header)
    print("Pattern 3: HeaderTemplate adopted as child of root")

    nav = Template()
    nav_bar = nav.child[html.Nav](style={"background": "#ecf0f1", "padding": "8px"})
    nav_bar.child[html.A](children="Home", href="/", style={"marginRight": "12px"})
    nav_bar.child[html.A](children="About", href="/about")
    root.child(nav)
    print("Pattern 3: Nav template adopted as child of root")

    # --- Pattern 1: factory syntax for main content ---
    main = root.child[html.Main](style={"padding": "20px"})
    print("Pattern 1: html.Main created via factory")

    section = main.child[html.Section]()
    section.child[html.H2](children="About These Patterns")
    dl = section.child[html.Dl]()

    dl.child[html.Dt](children="1. Factory — child[Type](**props)")
    dl.child[html.Dd](
        children=(
            "Creates typed LazyComponent with full IDE autocomplete "
            "(prop names, types, and defaults)."
        )
    )
    dl.child[html.Dt](children="2. Wrap — child(existing_component)")
    dl.child[html.Dd](
        children=(
            "Integrates any pre-built Dash component instance into the template tree."
        )
    )
    dl.child[html.Dt](children="3. Adopt — child(template_instance)")
    dl.child[html.Dd](
        children=(
            "Composes reusable template objects; "
            "register_callbacks walks the whole tree automatically."
        )
    )

    # --- Pattern 2: wrap an existing component instance ---
    info_box = html.Div(
        children=[
            html.Strong("Pro tip: "),
            "Mix all three patterns as needed — each has its use case.",
        ],
        style={
            "background": "#eaf4fb",
            "border": "1px solid #aed6f1",
            "padding": "10px",
            "borderRadius": "4px",
        },
    )
    main.child(info_box)
    print("Pattern 2: pre-built html.Div wrapped into template tree")

    # --- Pattern 3 again: adopt a footer template ---
    root.child(FooterTemplate())
    print("Pattern 3: FooterTemplate adopted as child of root")

    return root


# ----------------------------------------------------------------------- #
# App setup
# ----------------------------------------------------------------------- #


def create_app() -> Dash:
    """Build and return the Dash application."""
    print("\n=== Flexible Child Patterns Demo ===\n")
    page = build_page()

    app = Dash(__name__, suppress_callback_exceptions=True)
    # page has multiple direct children -> wrap in a single Div for app.layout
    app.layout = html.Div(
        children=page.materialize(),
        style={
            "fontFamily": "Arial, sans-serif",
            "maxWidth": "800px",
            "margin": "auto",
        },
    )
    # No callbacks in this example, but register_callbacks would handle them
    # automatically across the full template tree.
    page.register_callbacks(app)
    return app


if __name__ == "__main__":
    app = create_app()
    print("\nStarting Dash app on http://localhost:8050/")
    print("Press Ctrl+C to stop\n")
    app.run(host="0.0.0.0", port=8050, debug=True)
