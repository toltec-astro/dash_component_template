# dash_component_template Examples

**Package version:** v5.0.2
**API:** `Template`, `LazyComponent`, `WrappedComponent`, `callback_scope`

---

## Quick Start

Install the package and run the comprehensive demo:

```bash
# From the dash_component_template/ root
uv pip install -e .
uv run python examples/app.py
```

Then open **http://localhost:8050/** in your browser.

---

## Examples

### `app.py` — Comprehensive Demo (start here)

A single tabbed application covering all four major API patterns:

| Tab | Pattern | What it shows |
|-----|---------|---------------|
| 1. Basic Callbacks | `setup_callbacks(app)` | Instance-scoped callbacks; business logic separation |
| 2. Composition | `.child()` patterns | Factory, wrap, and compose sub-templates |
| 3. Pattern Matching | MATCH/ALL | Automatic `_template_id` scope injection |
| 4. Class Callbacks | `setup_class_callbacks()` | One shared callback for all instances |

```bash
uv run python examples/app.py
```

---

### `counter_with_callbacks.py` — Basic Callbacks

**Demonstrates:**
- `setup_callbacks(app)` with standard `@app.callback` decorator
- `self.button()` and `self.display()` returning auto-scoped component IDs
- Separating business logic into testable methods
- Multiple instances with independent state

```bash
uv run python examples/counter_with_callbacks.py
```

Key pattern:
```python
class CounterTemplate(Template):
    def __init__(self, factor=1.0, label="Count"):
        super().__init__()
        container = self.child[html.Div](...)
        self.button = container.child[html.Button](n_clicks=0)
        self.display = container.child[html.Div]()

    def setup_callbacks(self, app):
        @app.callback(
            Output(self.display(), "children"),
            Input(self.button(), "n_clicks"),
        )
        def update(n_clicks):
            return self.calculate(n_clicks)
```

---

### `flexible_child_patterns.py` — Template Composition

**Demonstrates all three `.child()` patterns:**

| Pattern | Syntax | Use case |
|---------|--------|----------|
| Factory | `self.child[html.Div](props)` | Typed components with IDE autocomplete |
| Wrap | `self.child(existing_component)` | Integrate existing Dash component instances |
| Compose | `self.child(template_instance)` | Nest Template subclasses |

```bash
uv run python examples/flexible_child_patterns.py
```

---

### `pattern_matching_demo.py` — MATCH Pattern Callbacks

**Demonstrates:**
- Dict IDs: `id={"type": "counter-btn", "index": i}`
- Automatic `_template_name` and `_template_id` injection at materialize time
- `self.button({"index": MATCH})` merges MATCH into the dict ID with scope
- Two independent `CounterGroup` instances that don't interfere

```bash
uv run python examples/pattern_matching_demo.py
```

Key pattern:
```python
# In __init__: explicit dict ID for pattern matching
self.button = container.child[html.Button](
    id={"type": "counter-btn", "index": i},
)

# In setup_callbacks: MATCH merges with auto-injected _template_id
@app.callback(
    Output(self.displays[0]({"index": MATCH}), "children"),
    Input(self.buttons[0]({"index": MATCH}), "n_clicks"),
)
def update(n_clicks): ...
```

---

### `class_level_callbacks.py` — Class Callbacks

**Demonstrates:**
- `setup_callbacks(app)` — one callback per instance (instance-scoped)
- `setup_class_callbacks(cls, instance, app)` — one callback for all instances (class-scoped)
- `callback_scope(template=ALL, template_cls=cls)` — ALL pattern for aggregation
- `ButtonGroup.reset_counter()` — clean state for predictable IDs

```bash
uv run python examples/class_level_callbacks.py
```

Key pattern:
```python
class ButtonGroup(Template):
    def setup_callbacks(self, app):
        # One per instance — _template_id scoped automatically
        @app.callback(Output(...), Input(...))
        def update_instance(n_clicks): ...

    @classmethod
    def setup_class_callbacks(cls, instance, app):
        # One for all instances — MATCH scope set automatically
        @app.callback(Output(...), Input(...))
        def update_class(n_clicks): ...

        # ALL pattern — needs explicit callback_scope
        with callback_scope(template=ALL, template_cls=cls):
            @app.callback(Output("total", "children"), Input(...))
            def aggregate(all_clicks): ...
```

---

## API Reference

### Template Lifecycle

```python
from dash_component_template import Template

class MyTemplate(Template):
    def __init__(self):
        super().__init__()
        # Build component tree here using .child[]
        container = self.child[html.Div]()
        self.button = container.child[html.Button](n_clicks=0)
        self.display = container.child[html.Div]()

    def setup_callbacks(self, app):
        # Define callbacks using standard Dash API
        @app.callback(
            Output(self.display(), "children"),
            Input(self.button(), "n_clicks"),
        )
        def update(n_clicks):
            return f"Clicked {n_clicks or 0} times"

# Usage
app = Dash(__name__)
template = MyTemplate()
app.layout = template.layout()        # Returns single Component; materializes tree
template.register_callbacks(app)      # Walks tree; calls setup_callbacks() on all nodes
app.run(host="0.0.0.0", port=8050, debug=True)
```

### Three `.child()` Patterns

```python
# 1. Factory — typed, IDE autocomplete
self.button = self.child[html.Button](children="Click", n_clicks=0)

# 2. Wrap — existing component instance
existing = html.Graph(id="my-graph", figure={...})
self.child(existing)

# 3. Compose — Template subclass
self.child(NavTemplate())
```

### Component ID Access

```python
# In setup_callbacks():
Output(self.display(), "children")          # Returns materialized component
Input(self.button(), "n_clicks")            # Returns materialized component

# Pattern matching (requires dict ID):
self.button = self.child[html.Button](id={"type": "btn", "index": 0})
Output(self.button({"index": MATCH}), "children")   # Returns scoped dict ID
Input(self.button({"index": MATCH}), "n_clicks")
```

### Multiple Instances

```python
# Each instance has an independent ID namespace
t1 = MyTemplate()   # IDs like: "mytemplate0-button0", "mytemplate0-div0"
t2 = MyTemplate()   # IDs like: "mytemplate1-button0", "mytemplate1-div0"

app.layout = html.Div([t1.layout(), t2.layout()])
t1.register_callbacks(app)
t2.register_callbacks(app)
```

---

## Troubleshooting

**Import error**: Install the package first:
```bash
uv pip install -e .   # from dash_component_template/ root
```

**`ValueError: materialize() returned empty list`**: Call `template.layout()` or
`template.materialize()` before `register_callbacks(app)`.

**Pattern matching not working**: Components need dict IDs set at construction time —
not string IDs. Use `id={"type": "...", "index": i}` when creating the component.

**Hot reload**: Reset state with `MyTemplate.reset_class_state(app)` if callbacks
are registered twice due to hot reload.
