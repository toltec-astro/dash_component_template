from typing import Any

from dash_component_template.lazy_component import LazyComponent
from dash_component_template.template import _Template

class _PropsNamespaceHtmlDiv:
    children: Any | None
    id: str | dict | None
    n_clicks: Any | None
    n_clicks_timestamp: Any | None
    disable_n_clicks: bool | None
    key: str | None
    accessKey: str | None  # noqa: N815
    className: str | None  # noqa: N815
    contentEditable: str | None  # noqa: N815
    dir: str | None
    draggable: str | None
    hidden: Any | None
    lang: str | None
    role: str | None
    spellCheck: str | None  # noqa: N815
    style: Any | None
    tabIndex: Any | None  # noqa: N815
    title: str | None

class ComponentTemplateHtmlDiv(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceHtmlDiv:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        children: Any | None = None,
        id: str | dict | None = None,
        n_clicks: Any | None = None,
        n_clicks_timestamp: Any | None = None,
        disable_n_clicks: bool | None = None,
        key: str | None = None,
        accessKey: str | None = None,  # noqa: N803
        className: str | None = None,  # noqa: N803
        contentEditable: str | None = None,  # noqa: N803
        dir: str | None = None,
        draggable: str | None = None,
        hidden: Any | None = None,
        lang: str | None = None,
        role: str | None = None,
        spellCheck: str | None = None,  # noqa: N803
        style: Any | None = None,
        tabIndex: Any | None = None,  # noqa: N803
        title: str | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...
