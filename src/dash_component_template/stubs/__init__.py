"""Type stub index for dash_component_template (V4.0).

This directory contains type stub files (.pyi) for IDE autocomplete and type checking.

The stubs provide full autocomplete for:
- .child[Type](...) factory pattern (via _component_template_factory.pyi)
- Component properties via .props namespace (via html.pyi, dcc.pyi)
- All Dash component properties as typed attributes

Files:
- _component_template_factory.pyi: Factory __getitem__ overloads for .child[Type]()
- html.pyi: Type stubs for dash.html components (Div, Button, etc.)
- dcc.pyi: Type stubs for dash.dcc components (Dropdown, Graph, etc.)

Usage:
    IDEs and type checkers will automatically discover these stubs.
    No explicit import needed - just use the .child[Type]() pattern:

    from dash import html
    from dash_component_template import Template

    root = Template()
    div = root.child[html.Div](  # <-- IDE knows this returns ComponentTemplateHtmlDiv
        className="...",  # <-- IDE suggests this
        style={...},      # <-- and this
    )
    div.props.className = "..."  # <-- and this too!

Generation:
    To regenerate stubs:
        python -m dash_component_template.stub_generator
"""

__all__ = []  # This is just a stub directory, no runtime exports
