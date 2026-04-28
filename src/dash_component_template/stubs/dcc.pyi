import datetime
from collections.abc import Sequence
from typing import Any

from dash_component_template.lazy_component import LazyComponent
from dash_component_template.template import _Template

class _PropsNamespaceDccChecklist:
    options: Any | None
    value: Any | None
    inline: bool | None
    className: str | None
    style: Any | None
    inputStyle: dict | None
    inputClassName: str | None
    labelStyle: dict | None
    labelClassName: str | None
    id: str | dict | None
    persistence: Any | None
    persisted_props: Any | None
    persistence_type: Any | None

class LazyComponentDccChecklist(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccChecklist:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        options: Any | None = None,
        value: Any | None = None,
        inline: bool | None = None,
        className: str | None = None,
        style: Any | None = None,
        inputStyle: dict | None = None,
        inputClassName: str | None = None,
        labelStyle: dict | None = None,
        labelClassName: str | None = None,
        id: str | dict | None = None,
        persistence: Any | None = None,
        persisted_props: Any | None = None,
        persistence_type: Any | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccClipboard:
    id: str | dict | None
    target_id: str | dict | None
    content: str | None
    n_clicks: Any | None
    html_content: str | None
    title: str | None
    style: Any | None
    className: str | None

class LazyComponentDccClipboard(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccClipboard:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        id: str | dict | None = None,
        target_id: str | dict | None = None,
        content: str | None = None,
        n_clicks: Any | None = None,
        html_content: str | None = None,
        title: str | None = None,
        style: Any | None = None,
        className: str | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccConfirmDialog:
    id: str | dict | None
    message: str | None
    submit_n_clicks: Any | None
    submit_n_clicks_timestamp: Any | None
    cancel_n_clicks: Any | None
    cancel_n_clicks_timestamp: Any | None
    displayed: bool | None

class LazyComponentDccConfirmDialog(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccConfirmDialog:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        id: str | dict | None = None,
        message: str | None = None,
        submit_n_clicks: Any | None = None,
        submit_n_clicks_timestamp: Any | None = None,
        cancel_n_clicks: Any | None = None,
        cancel_n_clicks_timestamp: Any | None = None,
        displayed: bool | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccConfirmDialogProvider:
    children: Any | None
    id: str | dict | None
    message: str | None
    submit_n_clicks: Any | None
    submit_n_clicks_timestamp: Any | None
    cancel_n_clicks: Any | None
    cancel_n_clicks_timestamp: Any | None
    displayed: bool | None

class LazyComponentDccConfirmDialogProvider(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccConfirmDialogProvider:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        children: Any | None = None,
        id: str | dict | None = None,
        message: str | None = None,
        submit_n_clicks: Any | None = None,
        submit_n_clicks_timestamp: Any | None = None,
        cancel_n_clicks: Any | None = None,
        cancel_n_clicks_timestamp: Any | None = None,
        displayed: bool | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccDatePickerRange:
    start_date: str | datetime.datetime | None
    end_date: str | datetime.datetime | None
    min_date_allowed: str | datetime.datetime | None
    max_date_allowed: str | datetime.datetime | None
    disabled_days: Any | None
    minimum_nights: Any | None
    updatemode: Any | None
    start_date_placeholder_text: str | None
    end_date_placeholder_text: str | None
    initial_visible_month: str | None
    clearable: bool | None
    reopen_calendar_on_clear: bool | None
    display_format: str | None
    month_format: str | None
    first_day_of_week: Any | None
    show_outside_days: bool | None
    stay_open_on_select: bool | None
    calendar_orientation: Any | None
    number_of_months_shown: Any | None
    with_portal: bool | None
    with_full_screen_portal: bool | None
    day_size: Any | None
    is_RTL: bool | None
    disabled: bool | None
    start_date_id: str | None
    end_date_id: str | None
    style: Any | None
    className: str | None
    id: str | dict | None
    persistence: Any | None
    persisted_props: Any | None
    persistence_type: Any | None

class LazyComponentDccDatePickerRange(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccDatePickerRange:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        start_date: str | datetime.datetime | None = None,
        end_date: str | datetime.datetime | None = None,
        min_date_allowed: str | datetime.datetime | None = None,
        max_date_allowed: str | datetime.datetime | None = None,
        disabled_days: Any | None = None,
        minimum_nights: Any | None = None,
        updatemode: Any | None = None,
        start_date_placeholder_text: str | None = None,
        end_date_placeholder_text: str | None = None,
        initial_visible_month: str | None = None,
        clearable: bool | None = None,
        reopen_calendar_on_clear: bool | None = None,
        display_format: str | None = None,
        month_format: str | None = None,
        first_day_of_week: Any | None = None,
        show_outside_days: bool | None = None,
        stay_open_on_select: bool | None = None,
        calendar_orientation: Any | None = None,
        number_of_months_shown: Any | None = None,
        with_portal: bool | None = None,
        with_full_screen_portal: bool | None = None,
        day_size: Any | None = None,
        is_RTL: bool | None = None,
        disabled: bool | None = None,
        start_date_id: str | None = None,
        end_date_id: str | None = None,
        style: Any | None = None,
        className: str | None = None,
        id: str | dict | None = None,
        persistence: Any | None = None,
        persisted_props: Any | None = None,
        persistence_type: Any | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccDatePickerSingle:
    date: str | datetime.datetime | None
    min_date_allowed: str | datetime.datetime | None
    max_date_allowed: str | datetime.datetime | None
    disabled_days: Any | None
    placeholder: str | None
    initial_visible_month: str | datetime.datetime | None
    clearable: bool | None
    reopen_calendar_on_clear: bool | None
    display_format: str | None
    month_format: str | None
    first_day_of_week: Any | None
    show_outside_days: bool | None
    stay_open_on_select: bool | None
    calendar_orientation: Any | None
    number_of_months_shown: Any | None
    with_portal: bool | None
    with_full_screen_portal: bool | None
    day_size: Any | None
    is_RTL: bool | None
    disabled: bool | None
    style: Any | None
    className: str | None
    id: str | dict | None
    persistence: Any | None
    persisted_props: Any | None
    persistence_type: Any | None

class LazyComponentDccDatePickerSingle(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccDatePickerSingle:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        date: str | datetime.datetime | None = None,
        min_date_allowed: str | datetime.datetime | None = None,
        max_date_allowed: str | datetime.datetime | None = None,
        disabled_days: Any | None = None,
        placeholder: str | None = None,
        initial_visible_month: str | datetime.datetime | None = None,
        clearable: bool | None = None,
        reopen_calendar_on_clear: bool | None = None,
        display_format: str | None = None,
        month_format: str | None = None,
        first_day_of_week: Any | None = None,
        show_outside_days: bool | None = None,
        stay_open_on_select: bool | None = None,
        calendar_orientation: Any | None = None,
        number_of_months_shown: Any | None = None,
        with_portal: bool | None = None,
        with_full_screen_portal: bool | None = None,
        day_size: Any | None = None,
        is_RTL: bool | None = None,
        disabled: bool | None = None,
        style: Any | None = None,
        className: str | None = None,
        id: str | dict | None = None,
        persistence: Any | None = None,
        persisted_props: Any | None = None,
        persistence_type: Any | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccDownload:
    id: str | dict | None
    data: Any | None
    base64: bool | None
    type: str | None

class LazyComponentDccDownload(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccDownload:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        id: str | dict | None = None,
        data: Any | None = None,
        base64: bool | None = None,
        type: str | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccDropdown:
    options: Any | None
    value: Any | None
    multi: bool | None
    clearable: bool | None
    searchable: bool | None
    search_value: str | None
    placeholder: str | None
    disabled: bool | None
    closeOnSelect: bool | None
    optionHeight: Any | None
    maxHeight: Any | None
    style: Any | None
    className: str | None
    id: str | dict | None
    persistence: Any | None
    persisted_props: Any | None
    persistence_type: Any | None

class LazyComponentDccDropdown(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccDropdown:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        options: Any | None = None,
        value: Any | None = None,
        multi: bool | None = None,
        clearable: bool | None = None,
        searchable: bool | None = None,
        search_value: str | None = None,
        placeholder: str | None = None,
        disabled: bool | None = None,
        closeOnSelect: bool | None = None,
        optionHeight: Any | None = None,
        maxHeight: Any | None = None,
        style: Any | None = None,
        className: str | None = None,
        id: str | dict | None = None,
        persistence: Any | None = None,
        persisted_props: Any | None = None,
        persistence_type: Any | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccGeolocation:
    id: str | dict | None
    local_date: str | None
    timestamp: Any | None
    position: Any | None
    position_error: Any | None
    show_alert: bool | None
    update_now: bool | None
    high_accuracy: bool | None
    maximum_age: Any | None
    timeout: Any | None

class LazyComponentDccGeolocation(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccGeolocation:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        id: str | dict | None = None,
        local_date: str | None = None,
        timestamp: Any | None = None,
        position: Any | None = None,
        position_error: Any | None = None,
        show_alert: bool | None = None,
        update_now: bool | None = None,
        high_accuracy: bool | None = None,
        maximum_age: Any | None = None,
        timeout: Any | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccGraph:
    id: str | dict | None
    responsive: Any | None
    clickData: dict | None
    clickAnnotationData: dict | None
    hoverData: dict | None
    clear_on_unhover: bool | None
    selectedData: dict | None
    relayoutData: dict | None
    extendData: Sequence | dict | None
    prependData: Sequence | dict | None
    restyleData: Sequence | None
    figure: Any | None
    style: Any | None
    className: str | None
    mathjax: bool | None
    animate: bool | None
    animation_options: dict | None
    config: Any | None

class LazyComponentDccGraph(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccGraph:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        id: str | dict | None = None,
        responsive: Any | None = None,
        clickData: dict | None = None,
        clickAnnotationData: dict | None = None,
        hoverData: dict | None = None,
        clear_on_unhover: bool | None = None,
        selectedData: dict | None = None,
        relayoutData: dict | None = None,
        extendData: Sequence | dict | None = None,
        prependData: Sequence | dict | None = None,
        restyleData: Sequence | None = None,
        figure: Any | None = None,
        style: Any | None = None,
        className: str | None = None,
        mathjax: bool | None = None,
        animate: bool | None = None,
        animation_options: dict | None = None,
        config: Any | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccInput:
    value: Any | None
    type: Any | None
    debounce: Any | None
    placeholder: Any | None
    n_submit: Any | None
    n_submit_timestamp: Any | None
    inputMode: Any | None
    autoComplete: str | None
    readOnly: Any | None
    required: Any | None
    autoFocus: Any | None
    disabled: Any | None
    list: str | None
    multiple: bool | None
    spellCheck: Any | None
    name: str | None
    min: Any | None
    max: Any | None
    step: Any | None
    minLength: Any | None
    maxLength: Any | None
    pattern: str | None
    selectionStart: str | None
    selectionEnd: str | None
    selectionDirection: str | None
    n_blur: Any | None
    n_blur_timestamp: Any | None
    size: str | None
    style: Any | None
    className: str | None
    id: str | dict | None
    persistence: Any | None
    persisted_props: Any | None
    persistence_type: Any | None

class LazyComponentDccInput(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccInput:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        value: Any | None = None,
        type: Any | None = None,
        debounce: Any | None = None,
        placeholder: Any | None = None,
        n_submit: Any | None = None,
        n_submit_timestamp: Any | None = None,
        inputMode: Any | None = None,
        autoComplete: str | None = None,
        readOnly: Any | None = None,
        required: Any | None = None,
        autoFocus: Any | None = None,
        disabled: Any | None = None,
        list: str | None = None,
        multiple: bool | None = None,
        spellCheck: Any | None = None,
        name: str | None = None,
        min: Any | None = None,
        max: Any | None = None,
        step: Any | None = None,
        minLength: Any | None = None,
        maxLength: Any | None = None,
        pattern: str | None = None,
        selectionStart: str | None = None,
        selectionEnd: str | None = None,
        selectionDirection: str | None = None,
        n_blur: Any | None = None,
        n_blur_timestamp: Any | None = None,
        size: str | None = None,
        style: Any | None = None,
        className: str | None = None,
        id: str | dict | None = None,
        persistence: Any | None = None,
        persisted_props: Any | None = None,
        persistence_type: Any | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccInterval:
    id: str | dict | None
    interval: Any | None
    disabled: bool | None
    n_intervals: Any | None
    max_intervals: Any | None

class LazyComponentDccInterval(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccInterval:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        id: str | dict | None = None,
        interval: Any | None = None,
        disabled: bool | None = None,
        n_intervals: Any | None = None,
        max_intervals: Any | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccLink:
    children: Any | None
    href: str | None
    target: str | None
    refresh: bool | None
    title: str | None
    className: str | None
    style: Any | None
    id: str | dict | None
    loading_state: Any | None

class LazyComponentDccLink(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccLink:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        children: Any | None = None,
        href: str | None = None,
        target: str | None = None,
        refresh: bool | None = None,
        title: str | None = None,
        className: str | None = None,
        style: Any | None = None,
        id: str | dict | None = None,
        loading_state: Any | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccLoading:
    children: Any | None
    id: str | dict | None
    type: Any | None
    fullscreen: bool | None
    debug: bool | None
    className: str | None
    parent_className: str | None
    style: Any | None
    parent_style: dict | None
    overlay_style: dict | None
    color: str | None
    display: Any | None
    delay_hide: Any | None
    delay_show: Any | None
    show_initially: bool | None
    target_components: Any | None
    custom_spinner: Any | None

class LazyComponentDccLoading(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccLoading:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        children: Any | None = None,
        id: str | dict | None = None,
        type: Any | None = None,
        fullscreen: bool | None = None,
        debug: bool | None = None,
        className: str | None = None,
        parent_className: str | None = None,
        style: Any | None = None,
        parent_style: dict | None = None,
        overlay_style: dict | None = None,
        color: str | None = None,
        display: Any | None = None,
        delay_hide: Any | None = None,
        delay_show: Any | None = None,
        show_initially: bool | None = None,
        target_components: Any | None = None,
        custom_spinner: Any | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccLocation:
    id: str | dict | None
    pathname: str | None
    search: str | None
    hash: str | None
    href: str | None
    refresh: Any | None

class LazyComponentDccLocation(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccLocation:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        id: str | dict | None = None,
        pathname: str | None = None,
        search: str | None = None,
        hash: str | None = None,
        href: str | None = None,
        refresh: Any | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccMarkdown:
    children: Any | None
    id: str | dict | None
    className: str | None
    mathjax: bool | None
    dangerously_allow_html: bool | None
    link_target: str | None
    dedent: bool | None
    highlight_config: Any | None
    style: Any | None

class LazyComponentDccMarkdown(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccMarkdown:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        children: Any | None = None,
        id: str | dict | None = None,
        className: str | None = None,
        mathjax: bool | None = None,
        dangerously_allow_html: bool | None = None,
        link_target: str | None = None,
        dedent: bool | None = None,
        highlight_config: Any | None = None,
        style: Any | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccRadioItems:
    options: Any | None
    value: Any | None
    inline: bool | None
    style: Any | None
    className: str | None
    inputStyle: dict | None
    inputClassName: str | None
    labelStyle: dict | None
    labelClassName: str | None
    id: str | dict | None
    persistence: Any | None
    persisted_props: Any | None
    persistence_type: Any | None

class LazyComponentDccRadioItems(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccRadioItems:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        options: Any | None = None,
        value: Any | None = None,
        inline: bool | None = None,
        style: Any | None = None,
        className: str | None = None,
        inputStyle: dict | None = None,
        inputClassName: str | None = None,
        labelStyle: dict | None = None,
        labelClassName: str | None = None,
        id: str | dict | None = None,
        persistence: Any | None = None,
        persisted_props: Any | None = None,
        persistence_type: Any | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccRangeSlider:
    min: Any | None
    max: Any | None
    step: Any | None
    marks: Any | None
    value: Any | None
    drag_value: Any | None
    allowCross: bool | None
    pushable: Any | None
    disabled: bool | None
    count: Any | None
    dots: bool | None
    included: bool | None
    tooltip: Any | None
    updatemode: Any | None
    vertical: bool | None
    verticalHeight: Any | None
    className: str | None
    id: str | dict | None
    persistence: Any | None
    persisted_props: Any | None
    persistence_type: Any | None

class LazyComponentDccRangeSlider(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccRangeSlider:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        min: Any | None = None,
        max: Any | None = None,
        step: Any | None = None,
        marks: Any | None = None,
        value: Any | None = None,
        drag_value: Any | None = None,
        allowCross: bool | None = None,
        pushable: Any | None = None,
        disabled: bool | None = None,
        count: Any | None = None,
        dots: bool | None = None,
        included: bool | None = None,
        tooltip: Any | None = None,
        updatemode: Any | None = None,
        vertical: bool | None = None,
        verticalHeight: Any | None = None,
        className: str | None = None,
        id: str | dict | None = None,
        persistence: Any | None = None,
        persisted_props: Any | None = None,
        persistence_type: Any | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccSlider:
    min: Any | None
    max: Any | None
    step: Any | None
    marks: Any | None
    value: Any | None
    drag_value: Any | None
    disabled: bool | None
    dots: bool | None
    included: bool | None
    tooltip: Any | None
    updatemode: Any | None
    vertical: bool | None
    verticalHeight: Any | None
    className: str | None
    id: str | dict | None
    persistence: Any | None
    persisted_props: Any | None
    persistence_type: Any | None

class LazyComponentDccSlider(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccSlider:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        min: Any | None = None,
        max: Any | None = None,
        step: Any | None = None,
        marks: Any | None = None,
        value: Any | None = None,
        drag_value: Any | None = None,
        disabled: bool | None = None,
        dots: bool | None = None,
        included: bool | None = None,
        tooltip: Any | None = None,
        updatemode: Any | None = None,
        vertical: bool | None = None,
        verticalHeight: Any | None = None,
        className: str | None = None,
        id: str | dict | None = None,
        persistence: Any | None = None,
        persisted_props: Any | None = None,
        persistence_type: Any | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccStore:
    id: str | dict | None
    storage_type: Any | None
    data: Any | None
    clear_data: bool | None
    modified_timestamp: Any | None

class LazyComponentDccStore(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccStore:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        id: str | dict | None = None,
        storage_type: Any | None = None,
        data: Any | None = None,
        clear_data: bool | None = None,
        modified_timestamp: Any | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccTab:
    children: Any | None
    id: str | dict | None
    label: str | None
    value: str | None
    disabled: bool | None
    disabled_style: dict | None
    disabled_className: str | None
    className: str | None
    selected_className: str | None
    style: Any | None
    selected_style: dict | None

class LazyComponentDccTab(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccTab:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        children: Any | None = None,
        id: str | dict | None = None,
        label: str | None = None,
        value: str | None = None,
        disabled: bool | None = None,
        disabled_style: dict | None = None,
        disabled_className: str | None = None,
        className: str | None = None,
        selected_className: str | None = None,
        style: Any | None = None,
        selected_style: dict | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccTabs:
    children: Any | None
    id: str | dict | None
    value: str | None
    className: str | None
    content_className: str | None
    parent_className: str | None
    style: Any | None
    parent_style: dict | None
    content_style: dict | None
    vertical: bool | None
    mobile_breakpoint: Any | None
    colors: Any | None
    persistence: Any | None
    persisted_props: Any | None
    persistence_type: Any | None

class LazyComponentDccTabs(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccTabs:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        children: Any | None = None,
        id: str | dict | None = None,
        value: str | None = None,
        className: str | None = None,
        content_className: str | None = None,
        parent_className: str | None = None,
        style: Any | None = None,
        parent_style: dict | None = None,
        content_style: dict | None = None,
        vertical: bool | None = None,
        mobile_breakpoint: Any | None = None,
        colors: Any | None = None,
        persistence: Any | None = None,
        persisted_props: Any | None = None,
        persistence_type: Any | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccTextarea:
    id: str | dict | None
    value: str | None
    autoFocus: str | None
    cols: Any | None
    disabled: str | bool | None
    form: str | None
    maxLength: Any | None
    minLength: Any | None
    name: str | None
    placeholder: str | None
    readOnly: Any | None
    required: Any | None
    rows: Any | None
    wrap: str | None
    accessKey: str | None
    className: str | None
    contentEditable: str | bool | None
    contextMenu: str | None
    dir: str | None
    draggable: Any | None
    hidden: str | None
    lang: str | None
    spellCheck: Any | None
    style: Any | None
    tabIndex: Any | None
    title: str | None
    n_blur: Any | None
    n_blur_timestamp: Any | None
    n_clicks: Any | None
    n_clicks_timestamp: Any | None
    persistence: Any | None
    persisted_props: Any | None
    persistence_type: Any | None

class LazyComponentDccTextarea(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccTextarea:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        id: str | dict | None = None,
        value: str | None = None,
        autoFocus: str | None = None,
        cols: Any | None = None,
        disabled: str | bool | None = None,
        form: str | None = None,
        maxLength: Any | None = None,
        minLength: Any | None = None,
        name: str | None = None,
        placeholder: str | None = None,
        readOnly: Any | None = None,
        required: Any | None = None,
        rows: Any | None = None,
        wrap: str | None = None,
        accessKey: str | None = None,
        className: str | None = None,
        contentEditable: str | bool | None = None,
        contextMenu: str | None = None,
        dir: str | None = None,
        draggable: Any | None = None,
        hidden: str | None = None,
        lang: str | None = None,
        spellCheck: Any | None = None,
        style: Any | None = None,
        tabIndex: Any | None = None,
        title: str | None = None,
        n_blur: Any | None = None,
        n_blur_timestamp: Any | None = None,
        n_clicks: Any | None = None,
        n_clicks_timestamp: Any | None = None,
        persistence: Any | None = None,
        persisted_props: Any | None = None,
        persistence_type: Any | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccTooltip:
    children: Any | None
    id: str | dict | None
    className: str | None
    style: Any | None
    bbox: Any | None
    show: bool | None
    direction: Any | None
    border_color: str | None
    background_color: str | None
    loading_text: str | None
    zindex: Any | None
    targetable: bool | None

class LazyComponentDccTooltip(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccTooltip:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        children: Any | None = None,
        id: str | dict | None = None,
        className: str | None = None,
        style: Any | None = None,
        bbox: Any | None = None,
        show: bool | None = None,
        direction: Any | None = None,
        border_color: str | None = None,
        background_color: str | None = None,
        loading_text: str | None = None,
        zindex: Any | None = None,
        targetable: bool | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...

class _PropsNamespaceDccUpload:
    children: Any | None
    id: str | dict | None
    contents: Any | None
    filename: Any | None
    last_modified: Any | None
    accept: str | None
    disabled: bool | None
    disable_click: bool | None
    max_size: Any | None
    min_size: Any | None
    multiple: bool | None
    className: str | None
    className_active: str | None
    className_reject: str | None
    className_disabled: str | None
    style: Any | None
    style_active: dict | None
    style_reject: dict | None
    style_disabled: dict | None

class LazyComponentDccUpload(LazyComponent):
    @property
    def props(self) -> _PropsNamespaceDccUpload:  # type: ignore[override]
        ...
    def __init__(  # type: ignore[no-untyped-def]
        self,
        children: Any | None = None,
        id: str | dict | None = None,
        contents: Any | None = None,
        filename: Any | None = None,
        last_modified: Any | None = None,
        accept: str | None = None,
        disabled: bool | None = None,
        disable_click: bool | None = None,
        max_size: Any | None = None,
        min_size: Any | None = None,
        multiple: bool | None = None,
        className: str | None = None,
        className_active: str | None = None,
        className_reject: str | None = None,
        className_disabled: str | None = None,
        style: Any | None = None,
        style_active: dict | None = None,
        style_reject: dict | None = None,
        style_disabled: dict | None = None,
        *,
        _parent: _Template | None = None,
    ) -> None: ...
