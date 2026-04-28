# dash_component_template

![PyPI version](https://img.shields.io/pypi/v/dash_component_template.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![Dash](https://img.shields.io/badge/dash-%3E%3D3.2-green)
![Tests](https://img.shields.io/badge/tests-329%2F329%20passing-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen)

**A powerful, type-safe framework for building reusable Dash components with integrated callback support.**

Build self-contained, composable Dash widgets that bundle UI structure and interactive behavior into clean Python classes. Features hierarchical tree-aware IDs, integrated callback scoping, and full type safety.

**✨ What's New in v5.0:**
- **🔄 Integrated Callbacks**: Define callbacks directly in templates with `setup_callbacks(app)`
- **🎯 Automatic Scoping**: Multiple template instances maintain independent callback state
- **🎭 Pattern Matching**: Full support for MATCH and ALL patterns
- **🔍 Type Safety**: Enhanced type hints and generic support with `Template[ComponentType]`
- **⚡ Call Operator**: Clean syntax with `self.button()` to get Component for callbacks

---

## ✨ Features

### Core Capabilities
- **🎯 Type-Safe Component Trees**: Build component hierarchies with full IDE autocomplete
- **🔄 Integrated Callback System**: Define callbacks directly in templates with automatic scoping
- **🎨 Flexible Props System**: Create components with configurable, validated properties using Pydantic
- **♻️ Component Reusability**: Define templates once, instantiate multiple times with independent state
- **🌲 Intuitive Tree API**: Parent-child relationships with `.child[Type](...)` bracket syntax
- **🎭 Pattern Matching Support**: MATCH and ALL patterns for dynamic callback targets
- **🧪 Production Ready**: 329 comprehensive tests with 98% coverage

---

## 🚀 Quick Start

### Installation

```bash
# Using uv (recommended)
uv pip install dash-component-template

# Or using pip
pip install dash-component-template
```

### Simple Counter with Callbacks

```python
from dash import Dash, Input, Output, html
from dash_component_template import Template

class CounterTemplate(Template):
    """A reusable counter component with integrated callbacks."""

    def __init__(self, factor: float = 1.0, label: str = "Count"):
        super().__init__()
        # Create the component tree
        container = self.child[html.Div]()

        # Add children using bracket syntax for type safety
        self.button = container.child[html.Button](
            children=f"Click me ({label})",
            n_clicks=0
        )
        self.display = container.child[html.Div](
            children=f"{label}: 0"
        )

        # Store configuration
        self.factor = factor
        self.label = label

    def setup_callbacks(self, app):
        """Define callbacks for this template."""
        @app.callback(
            Output(self.display(), "children"),  # Use () to get Component
            Input(self.button(), "n_clicks"),
        )
        def update_count(n_clicks):
            if n_clicks is None:
                n_clicks = 0
            value = int(n_clicks * self.factor)
            return f"{self.label}: {value}"

# Create a Dash app
app = Dash(__name__)

# Create two independent counter instances
counter1 = CounterTemplate(factor=1.0, label="Counter 1")
counter2 = CounterTemplate(factor=2.0, label="Counter 2")

# Set up the layout
app.layout = html.Div([
    counter1.layout(),
    counter2.layout(),
])

# Register callbacks for both instances
counter1.register_callbacks(app)
counter2.register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
```

**Key Points:**
- Use `Template` as the base class (not `ComponentTemplate`)
- Use `.child[Type](...)` bracket syntax for type-safe child creation
- Use `self.component()` (call operator) to get the Component for callbacks
- Call `setup_callbacks(app)` to define callbacks for the template
- Call `register_callbacks(app)` to wire up callbacks for each instance

---

## 📖 Core Concepts

### 1. Template Base Class

The `Template` class is the foundation for building reusable components:

```python
from dash_component_template import Template
from dash import html

class MyTemplate(Template):
    def __init__(self, title: str = "Default"):
        super().__init__()

        # Create component tree
        self.header = self.child[html.H1](children=title)
        self.content = self.child[html.Div]()
```

### 2. Type-Safe Child Creation

Use bracket syntax `.child[Type](...)` for IDE autocomplete and type checking:

```python
# Correct: Bracket syntax
self.button = container.child[html.Button](children="Click")
self.div = container.child[html.Div](className="container")

# The type parameter helps your IDE provide autocomplete
# for component-specific props
```

### 3. Component Access with Call Operator

Wrapped components implement `__call__()` to return the underlying Dash Component:

```python
class MyTemplate(Template):
    def __init__(self):
        super().__init__()
        self.button = self.child[html.Button](children="Click", n_clicks=0)

    def setup_callbacks(self, app):
        @app.callback(
            Output(self.button(), "children"),  # self.button() returns Component
            Input(self.button(), "n_clicks"),
        )
        def update_button(n_clicks):
            return f"Clicked {n_clicks} times"
```

**Why the call operator?**
- Clean, consistent syntax for getting Components
- Clear distinction between wrapped object and Dash Component
- Type-safe: returns `Component` type for callback signatures

### 4. Integrated Callback System

Templates can define their own callbacks using `setup_callbacks(app)`:

```python
class FormTemplate(Template):
    def __init__(self):
        super().__init__()
        self.input = self.child[dcc.Input](value="")
        self.output = self.child[html.Div]()

    def setup_callbacks(self, app):
        """Define callbacks for this template."""
        @app.callback(
            Output(self.output(), "children"),
            Input(self.input(), "value"),
        )
        def update_output(value):
            return f"You typed: {value}"

# In your app:
form = FormTemplate()
app.layout = form.layout()
form.register_callbacks(app)  # Wires up the callbacks
```

### 5. Multiple Independent Instances

Each template instance maintains its own state and callbacks:

```python
# Create multiple instances with different configurations
counter1 = CounterTemplate(factor=1.0, label="Counter 1")
counter2 = CounterTemplate(factor=2.0, label="Counter 2")
counter3 = CounterTemplate(factor=5.0, label="Counter 3")

app.layout = html.Div([
    counter1.layout(),
    counter2.layout(),
    counter3.layout(),
])

# Each instance gets its own scoped callbacks
counter1.register_callbacks(app)
counter2.register_callbacks(app)
counter3.register_callbacks(app)
```

Each counter operates independently—clicking one doesn't affect the others!

---

## 🎭 Pattern Matching Support

Templates fully support Dash's pattern-matching callbacks with MATCH and ALL:

```python
from dash import MATCH, ALL
from dash_component_template import Template

class DynamicListTemplate(Template):
    def __init__(self):
        super().__init__()
        self.container = self.child[html.Div]()
        self.add_button = self.child[html.Button](children="Add Item")

    def setup_callbacks(self, app):
        # Callback using MATCH pattern
        @app.callback(
            Output({"type": "item-display", "index": MATCH}, "children"),
            Input({"type": "item-button", "index": MATCH}, "n_clicks"),
        )
        def update_item(n_clicks):
            return f"Clicked {n_clicks} times"

        # Callback using ALL pattern
        @app.callback(
            Output("summary", "children"),
            Input({"type": "item-button", "index": ALL}, "n_clicks"),
        )
        def update_summary(all_clicks):
            total = sum(c or 0 for c in all_clicks)
            return f"Total clicks across all items: {total}"
```

Pattern matching enables:
- Dynamic component creation
- Shared callbacks across similar components
- Flexible, data-driven UIs

---

## 🎨 Props System

Templates support a comprehensive props system for component configuration:

### Basic Props Access

```python
class CardTemplate(Template):
    def __init__(self, title: str, description: str):
        super().__init__()
        self.card = self.child[html.Div](
            className="card",
            # Access and modify props
        )

        # Read props
        current_class = self.card.props.className  # "card"

        # Update props (shallow merge)
        self.card.props_update({"style": {"padding": "10px"}})

        # Recursive update (deep merge)
        self.card.props_rupdate({
            "style": {"margin": "5px"}  # Merges with existing style
        })
```

### Wildcard Properties

Full support for `data-*` and `aria-*` attributes:

```python
self.button = self.child[html.Button](
    children="Click me",
    **{
        "data-test-id": "submit-btn",
        "aria-label": "Submit form",
        "aria-pressed": "false",
    }
)

# Access wildcard props
test_id = self.button.props["data-test-id"]
```

### Props Utilities

```python
# Check if prop exists
if "className" in self.button.props:
    print(self.button.props.className)

# Convert to dict
props_dict = self.button.props.to_dict()

# Iterate over props
for key, value in self.button.props.items():
    print(f"{key}: {value}")
```

---

## 🌲 Tree API

Templates provide a tree-based API for navigation and inspection:

```python
class DashboardTemplate(Template):
    def __init__(self):
        super().__init__()

        # Create hierarchy
        self.sidebar = self.child[html.Div](className="sidebar")
        self.nav = self.sidebar.child[html.Nav]()
        self.link1 = self.nav.child[html.A](href="/page1")

        # Tree navigation
        assert self.link1.parent == self.nav
        assert self.nav.parent == self.sidebar
        assert self.sidebar.parent == self  # Root template

        # Access children
        nav_children = self.nav.children  # [self.link1]

        # Get unique tree-aware ID
        link_id = self.link1.id  # Something like "dashboard_sidebar_nav_link1"
```

### Tree Properties

- **`.parent`**: Reference to parent component
- **`.children`**: List of child components
- **`.id`**: Unique hierarchical ID string
- **`.layout()`**: Generate Dash layout from tree

---

## 🔧 Advanced Usage

### Custom Validation with Pydantic

Combine with Pydantic for validated configuration:

```python
from pydantic import BaseModel, Field
from dash_component_template import Template

class ChartConfig(BaseModel):
    title: str = Field(..., min_length=1)
    max_points: int = Field(100, ge=1, le=1000)
    color: str = Field("#3366cc", pattern=r"^#[0-9a-fA-F]{6}$")

class ChartTemplate(Template):
    def __init__(self, config: ChartConfig):
        super().__init__()
        self.config = config  # Automatically validated!

        self.title = self.child[html.H2](children=config.title)
        self.graph = self.child[dcc.Graph](
            figure=self._create_figure()
        )
```

### Lazy Component Loading

Use `LazyComponent` for components that should be created on-demand:

```python
from dash_component_template import LazyComponent

class ExpensiveTemplate(Template):
    def __init__(self):
        super().__init__()

        # Component created only when accessed
        self.expensive = LazyComponent(
            lambda: self._create_expensive_component()
        )

    def _create_expensive_component(self):
        # Heavy computation here
        return html.Div(children="Expensive content")
```

### Callback Scope Context

Use `callback_scope` context manager for advanced callback organization:

```python
from dash_component_template import callback_scope

class ComplexTemplate(Template):
    def setup_callbacks(self, app):
        # Group related callbacks
        with callback_scope(app, scope_id=f"{self.id}_main"):
            @app.callback(...)
            def callback1(...):
                pass

            @app.callback(...)
            def callback2(...):
                pass
```

---

## 📚 Examples

The repository includes comprehensive examples:

- **`examples/counter_with_callbacks.py`**: Basic counter showing callback integration
- **`examples/multi_instance.py`**: Multiple independent template instances
- **`examples/pattern_matching.py`**: Using MATCH and ALL patterns
- **`examples/props_demo.py`**: Props system and wildcard attributes
- **`examples/tree_navigation.py`**: Tree API and hierarchical IDs

Run any example:

```bash
uv run python examples/counter_with_callbacks.py
```

---

## 🧪 Testing

The package includes 329 comprehensive tests covering:

- Template creation and hierarchy ✅
- Callback integration and scoping ✅
- Pattern matching (MATCH/ALL) ✅
- Props system and updates ✅
- Tree navigation and IDs ✅
- Type safety and generics ✅
- Edge cases and error handling ✅

Run tests:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=dash_component_template --cov-report=html

# Run specific test file
uv run pytest tests/test_template.py -v
```

---

## 📖 Documentation

- **Design Documentation**: See `design/` directory for comprehensive design docs
  - `MEMORY_BANK_v5_0_callbacks.md`: v5.0 callback system design and API reference
  - `CODE_QUALITY_REPORT_v5_0_2.md`: Quality validation and test coverage
  - `INDEX.md`: Complete design documentation index

- **API Reference**: Full API documentation in the design docs
- **Examples**: Working examples in `examples/` directory
- **Tests**: Test suite in `tests/` demonstrates all features

---

## 🔄 Migration from v4.x

If you're upgrading from v4.x, here are the key changes:

### Class Name Change
```python
# Old (v4.x)
from dash_component_template import ComponentTemplate

# New (v5.0+)
from dash_component_template import Template
```

### Child Creation Syntax
```python
# Old (v4.x)
self.button = container.child(html.Button, children="Click")

# New (v5.0+)
self.button = container.child[html.Button](children="Click")
```

### Callback Integration
```python
# Old (v4.x) - External callbacks
@app.callback(
    Output(counter.display.id, "children"),
    Input(counter.button.id, "n_clicks"),
)
def update(...):
    pass

# New (v5.0+) - Integrated callbacks
class Counter(Template):
    def setup_callbacks(self, app):
        @app.callback(
            Output(self.display(), "children"),
            Input(self.button(), "n_clicks"),
        )
        def update(...):
            pass

counter.register_callbacks(app)
```

### Component Access
```python
# Old (v4.x)
component_id = self.button.id  # Access ID property

# New (v5.0+)
component = self.button()  # Get Component with call operator
component_id = component.id  # Then access ID
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests (`uv run pytest`)
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Built for the [Plotly Dash](https://dash.plotly.com/) framework
- Inspired by component-based architectures in React and Vue
- Developed for the TolTEC project at UMass Astronomy

---

## 📧 Contact

- **Author**: Zhiyuan Ma
- **Email**: zhiyuanma@umass.edu
- **Issues**: [GitHub Issues](https://github.com/toltec-astro/dash_component_template/issues)
- **Documentation**: See `design/` directory in the repository

---

**Status**: Production Ready (v5.0.2) | **Tests**: 329/329 Passing | **Coverage**: 98%
