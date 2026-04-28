from collections.abc import Callable
from typing import overload

import dash_mantine_components
from dash import dcc, html

from dash_component_template.lazy_component import LazyComponent
from dash_component_template.stubs.dash_mantine_components import *

# Import all component template stub classes
from dash_component_template.stubs.dcc import *
from dash_component_template.stubs.html import *

class LazyComponentFactory:
    @overload
    def __getitem__(
        self, component_cls: type[dcc.Checklist]
    ) -> Callable[..., LazyComponentDccChecklist]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.Clipboard]
    ) -> Callable[..., LazyComponentDccClipboard]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.ConfirmDialog]
    ) -> Callable[..., LazyComponentDccConfirmDialog]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.ConfirmDialogProvider]
    ) -> Callable[..., LazyComponentDccConfirmDialogProvider]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.DatePickerRange]
    ) -> Callable[..., LazyComponentDccDatePickerRange]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.DatePickerSingle]
    ) -> Callable[..., LazyComponentDccDatePickerSingle]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.Download]
    ) -> Callable[..., LazyComponentDccDownload]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.Dropdown]
    ) -> Callable[..., LazyComponentDccDropdown]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.Geolocation]
    ) -> Callable[..., LazyComponentDccGeolocation]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.Graph]
    ) -> Callable[..., LazyComponentDccGraph]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.Input]
    ) -> Callable[..., LazyComponentDccInput]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.Interval]
    ) -> Callable[..., LazyComponentDccInterval]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.Link]
    ) -> Callable[..., LazyComponentDccLink]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.Loading]
    ) -> Callable[..., LazyComponentDccLoading]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.Location]
    ) -> Callable[..., LazyComponentDccLocation]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.Markdown]
    ) -> Callable[..., LazyComponentDccMarkdown]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.RadioItems]
    ) -> Callable[..., LazyComponentDccRadioItems]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.RangeSlider]
    ) -> Callable[..., LazyComponentDccRangeSlider]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.Slider]
    ) -> Callable[..., LazyComponentDccSlider]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.Store]
    ) -> Callable[..., LazyComponentDccStore]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.Tab]
    ) -> Callable[..., LazyComponentDccTab]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.Tabs]
    ) -> Callable[..., LazyComponentDccTabs]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.Textarea]
    ) -> Callable[..., LazyComponentDccTextarea]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.Tooltip]
    ) -> Callable[..., LazyComponentDccTooltip]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dcc.Upload]
    ) -> Callable[..., LazyComponentDccUpload]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.A]
    ) -> Callable[..., LazyComponentHtmlA]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Abbr]
    ) -> Callable[..., LazyComponentHtmlAbbr]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Acronym]
    ) -> Callable[..., LazyComponentHtmlAcronym]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Address]
    ) -> Callable[..., LazyComponentHtmlAddress]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Area]
    ) -> Callable[..., LazyComponentHtmlArea]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Article]
    ) -> Callable[..., LazyComponentHtmlArticle]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Aside]
    ) -> Callable[..., LazyComponentHtmlAside]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Audio]
    ) -> Callable[..., LazyComponentHtmlAudio]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.B]
    ) -> Callable[..., LazyComponentHtmlB]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Base]
    ) -> Callable[..., LazyComponentHtmlBase]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Basefont]
    ) -> Callable[..., LazyComponentHtmlBasefont]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Bdi]
    ) -> Callable[..., LazyComponentHtmlBdi]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Bdo]
    ) -> Callable[..., LazyComponentHtmlBdo]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Big]
    ) -> Callable[..., LazyComponentHtmlBig]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Blink]
    ) -> Callable[..., LazyComponentHtmlBlink]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Blockquote]
    ) -> Callable[..., LazyComponentHtmlBlockquote]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Br]
    ) -> Callable[..., LazyComponentHtmlBr]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Button]
    ) -> Callable[..., LazyComponentHtmlButton]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Canvas]
    ) -> Callable[..., LazyComponentHtmlCanvas]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Caption]
    ) -> Callable[..., LazyComponentHtmlCaption]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Center]
    ) -> Callable[..., LazyComponentHtmlCenter]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Cite]
    ) -> Callable[..., LazyComponentHtmlCite]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Code]
    ) -> Callable[..., LazyComponentHtmlCode]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Col]
    ) -> Callable[..., LazyComponentHtmlCol]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Colgroup]
    ) -> Callable[..., LazyComponentHtmlColgroup]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Content]
    ) -> Callable[..., LazyComponentHtmlContent]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Data]
    ) -> Callable[..., LazyComponentHtmlData]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Datalist]
    ) -> Callable[..., LazyComponentHtmlDatalist]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Dd]
    ) -> Callable[..., LazyComponentHtmlDd]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Del]
    ) -> Callable[..., LazyComponentHtmlDel]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Details]
    ) -> Callable[..., LazyComponentHtmlDetails]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Dfn]
    ) -> Callable[..., LazyComponentHtmlDfn]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Dialog]
    ) -> Callable[..., LazyComponentHtmlDialog]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Div]
    ) -> Callable[..., LazyComponentHtmlDiv]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Dl]
    ) -> Callable[..., LazyComponentHtmlDl]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Dt]
    ) -> Callable[..., LazyComponentHtmlDt]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Em]
    ) -> Callable[..., LazyComponentHtmlEm]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Embed]
    ) -> Callable[..., LazyComponentHtmlEmbed]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Fieldset]
    ) -> Callable[..., LazyComponentHtmlFieldset]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Figcaption]
    ) -> Callable[..., LazyComponentHtmlFigcaption]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Figure]
    ) -> Callable[..., LazyComponentHtmlFigure]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Font]
    ) -> Callable[..., LazyComponentHtmlFont]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Footer]
    ) -> Callable[..., LazyComponentHtmlFooter]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Form]
    ) -> Callable[..., LazyComponentHtmlForm]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Frame]
    ) -> Callable[..., LazyComponentHtmlFrame]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Frameset]
    ) -> Callable[..., LazyComponentHtmlFrameset]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.H1]
    ) -> Callable[..., LazyComponentHtmlH1]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.H2]
    ) -> Callable[..., LazyComponentHtmlH2]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.H3]
    ) -> Callable[..., LazyComponentHtmlH3]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.H4]
    ) -> Callable[..., LazyComponentHtmlH4]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.H5]
    ) -> Callable[..., LazyComponentHtmlH5]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.H6]
    ) -> Callable[..., LazyComponentHtmlH6]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Header]
    ) -> Callable[..., LazyComponentHtmlHeader]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Hgroup]
    ) -> Callable[..., LazyComponentHtmlHgroup]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Hr]
    ) -> Callable[..., LazyComponentHtmlHr]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.I]
    ) -> Callable[..., LazyComponentHtmlI]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Iframe]
    ) -> Callable[..., LazyComponentHtmlIframe]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Img]
    ) -> Callable[..., LazyComponentHtmlImg]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Ins]
    ) -> Callable[..., LazyComponentHtmlIns]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Kbd]
    ) -> Callable[..., LazyComponentHtmlKbd]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Keygen]
    ) -> Callable[..., LazyComponentHtmlKeygen]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Label]
    ) -> Callable[..., LazyComponentHtmlLabel]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Legend]
    ) -> Callable[..., LazyComponentHtmlLegend]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Li]
    ) -> Callable[..., LazyComponentHtmlLi]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Link]
    ) -> Callable[..., LazyComponentHtmlLink]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Main]
    ) -> Callable[..., LazyComponentHtmlMain]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.MapEl]
    ) -> Callable[..., LazyComponentHtmlMapEl]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Mark]
    ) -> Callable[..., LazyComponentHtmlMark]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Marquee]
    ) -> Callable[..., LazyComponentHtmlMarquee]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Meta]
    ) -> Callable[..., LazyComponentHtmlMeta]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Meter]
    ) -> Callable[..., LazyComponentHtmlMeter]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Nav]
    ) -> Callable[..., LazyComponentHtmlNav]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Nobr]
    ) -> Callable[..., LazyComponentHtmlNobr]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Noscript]
    ) -> Callable[..., LazyComponentHtmlNoscript]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.ObjectEl]
    ) -> Callable[..., LazyComponentHtmlObjectEl]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Ol]
    ) -> Callable[..., LazyComponentHtmlOl]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Optgroup]
    ) -> Callable[..., LazyComponentHtmlOptgroup]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Option]
    ) -> Callable[..., LazyComponentHtmlOption]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Output]
    ) -> Callable[..., LazyComponentHtmlOutput]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.P]
    ) -> Callable[..., LazyComponentHtmlP]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Param]
    ) -> Callable[..., LazyComponentHtmlParam]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Picture]
    ) -> Callable[..., LazyComponentHtmlPicture]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Plaintext]
    ) -> Callable[..., LazyComponentHtmlPlaintext]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Pre]
    ) -> Callable[..., LazyComponentHtmlPre]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Progress]
    ) -> Callable[..., LazyComponentHtmlProgress]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Q]
    ) -> Callable[..., LazyComponentHtmlQ]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Rb]
    ) -> Callable[..., LazyComponentHtmlRb]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Rp]
    ) -> Callable[..., LazyComponentHtmlRp]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Rt]
    ) -> Callable[..., LazyComponentHtmlRt]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Rtc]
    ) -> Callable[..., LazyComponentHtmlRtc]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Ruby]
    ) -> Callable[..., LazyComponentHtmlRuby]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.S]
    ) -> Callable[..., LazyComponentHtmlS]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Samp]
    ) -> Callable[..., LazyComponentHtmlSamp]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Script]
    ) -> Callable[..., LazyComponentHtmlScript]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Section]
    ) -> Callable[..., LazyComponentHtmlSection]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Select]
    ) -> Callable[..., LazyComponentHtmlSelect]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Shadow]
    ) -> Callable[..., LazyComponentHtmlShadow]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Slot]
    ) -> Callable[..., LazyComponentHtmlSlot]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Small]
    ) -> Callable[..., LazyComponentHtmlSmall]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Source]
    ) -> Callable[..., LazyComponentHtmlSource]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Spacer]
    ) -> Callable[..., LazyComponentHtmlSpacer]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Span]
    ) -> Callable[..., LazyComponentHtmlSpan]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Strike]
    ) -> Callable[..., LazyComponentHtmlStrike]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Strong]
    ) -> Callable[..., LazyComponentHtmlStrong]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Sub]
    ) -> Callable[..., LazyComponentHtmlSub]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Summary]
    ) -> Callable[..., LazyComponentHtmlSummary]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Sup]
    ) -> Callable[..., LazyComponentHtmlSup]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Table]
    ) -> Callable[..., LazyComponentHtmlTable]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Tbody]
    ) -> Callable[..., LazyComponentHtmlTbody]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Td]
    ) -> Callable[..., LazyComponentHtmlTd]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Template]
    ) -> Callable[..., LazyComponentHtmlTemplate]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Textarea]
    ) -> Callable[..., LazyComponentHtmlTextarea]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Tfoot]
    ) -> Callable[..., LazyComponentHtmlTfoot]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Th]
    ) -> Callable[..., LazyComponentHtmlTh]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Thead]
    ) -> Callable[..., LazyComponentHtmlThead]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Time]
    ) -> Callable[..., LazyComponentHtmlTime]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Title]
    ) -> Callable[..., LazyComponentHtmlTitle]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Tr]
    ) -> Callable[..., LazyComponentHtmlTr]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Track]
    ) -> Callable[..., LazyComponentHtmlTrack]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.U]
    ) -> Callable[..., LazyComponentHtmlU]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Ul]
    ) -> Callable[..., LazyComponentHtmlUl]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Var]
    ) -> Callable[..., LazyComponentHtmlVar]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Video]
    ) -> Callable[..., LazyComponentHtmlVideo]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Wbr]
    ) -> Callable[..., LazyComponentHtmlWbr]: ...
    @overload
    def __getitem__(
        self, component_cls: type[html.Xmp]
    ) -> Callable[..., LazyComponentHtmlXmp]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Accordion]
    ) -> Callable[..., LazyComponentDmcAccordion]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.AccordionControl]
    ) -> Callable[..., LazyComponentDmcAccordionControl]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.AccordionItem]
    ) -> Callable[..., LazyComponentDmcAccordionItem]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.AccordionPanel]
    ) -> Callable[..., LazyComponentDmcAccordionPanel]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.ActionIcon]
    ) -> Callable[..., LazyComponentDmcActionIcon]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.ActionIconGroup]
    ) -> Callable[..., LazyComponentDmcActionIconGroup]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Affix]
    ) -> Callable[..., LazyComponentDmcAffix]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Alert]
    ) -> Callable[..., LazyComponentDmcAlert]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Anchor]
    ) -> Callable[..., LazyComponentDmcAnchor]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.AppShell]
    ) -> Callable[..., LazyComponentDmcAppShell]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.AppShellAside]
    ) -> Callable[..., LazyComponentDmcAppShellAside]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.AppShellFooter]
    ) -> Callable[..., LazyComponentDmcAppShellFooter]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.AppShellHeader]
    ) -> Callable[..., LazyComponentDmcAppShellHeader]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.AppShellMain]
    ) -> Callable[..., LazyComponentDmcAppShellMain]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.AppShellNavbar]
    ) -> Callable[..., LazyComponentDmcAppShellNavbar]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.AppShellSection]
    ) -> Callable[..., LazyComponentDmcAppShellSection]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.AreaChart]
    ) -> Callable[..., LazyComponentDmcAreaChart]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.AreaChart]
    ) -> Callable[..., LazyComponentDmcAreaChart]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.AspectRatio]
    ) -> Callable[..., LazyComponentDmcAspectRatio]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Autocomplete]
    ) -> Callable[..., LazyComponentDmcAutocomplete]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Avatar]
    ) -> Callable[..., LazyComponentDmcAvatar]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.AvatarGroup]
    ) -> Callable[..., LazyComponentDmcAvatarGroup]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.BackgroundImage]
    ) -> Callable[..., LazyComponentDmcBackgroundImage]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Badge]
    ) -> Callable[..., LazyComponentDmcBadge]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.BarChart]
    ) -> Callable[..., LazyComponentDmcBarChart]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.BarChart]
    ) -> Callable[..., LazyComponentDmcBarChart]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Blockquote]
    ) -> Callable[..., LazyComponentDmcBlockquote]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Box]
    ) -> Callable[..., LazyComponentDmcBox]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Breadcrumbs]
    ) -> Callable[..., LazyComponentDmcBreadcrumbs]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.BubbleChart]
    ) -> Callable[..., LazyComponentDmcBubbleChart]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.BubbleChart]
    ) -> Callable[..., LazyComponentDmcBubbleChart]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Burger]
    ) -> Callable[..., LazyComponentDmcBurger]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Button]
    ) -> Callable[..., LazyComponentDmcButton]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.ButtonGroup]
    ) -> Callable[..., LazyComponentDmcButtonGroup]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Card]
    ) -> Callable[..., LazyComponentDmcCard]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.CardSection]
    ) -> Callable[..., LazyComponentDmcCardSection]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Carousel]
    ) -> Callable[..., LazyComponentDmcCarousel]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.CarouselSlide]
    ) -> Callable[..., LazyComponentDmcCarouselSlide]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Center]
    ) -> Callable[..., LazyComponentDmcCenter]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Checkbox]
    ) -> Callable[..., LazyComponentDmcCheckbox]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.CheckboxCard]
    ) -> Callable[..., LazyComponentDmcCheckboxCard]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.CheckboxGroup]
    ) -> Callable[..., LazyComponentDmcCheckboxGroup]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.CheckboxIndicator]
    ) -> Callable[..., LazyComponentDmcCheckboxIndicator]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Chip]
    ) -> Callable[..., LazyComponentDmcChip]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.ChipGroup]
    ) -> Callable[..., LazyComponentDmcChipGroup]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.ChipGroupContext]
    ) -> Callable[..., LazyComponentDmcChipGroupContext]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Code]
    ) -> Callable[..., LazyComponentDmcCode]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.CodeHighlight]
    ) -> Callable[..., LazyComponentDmcCodeHighlight]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.CodeHighlight]
    ) -> Callable[..., LazyComponentDmcCodeHighlight]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.CodeHighlightTabs]
    ) -> Callable[..., LazyComponentDmcCodeHighlightTabs]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.CodeHighlightTabs]
    ) -> Callable[..., LazyComponentDmcCodeHighlightTabs]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Collapse]
    ) -> Callable[..., LazyComponentDmcCollapse]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.ColorInput]
    ) -> Callable[..., LazyComponentDmcColorInput]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.ColorPicker]
    ) -> Callable[..., LazyComponentDmcColorPicker]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.CompositeChart]
    ) -> Callable[..., LazyComponentDmcCompositeChart]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.CompositeChart]
    ) -> Callable[..., LazyComponentDmcCompositeChart]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Container]
    ) -> Callable[..., LazyComponentDmcContainer]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.DateInput]
    ) -> Callable[..., LazyComponentDmcDateInput]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.DatePicker]
    ) -> Callable[..., LazyComponentDmcDatePicker]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.DatePickerInput]
    ) -> Callable[..., LazyComponentDmcDatePickerInput]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.DateTimePicker]
    ) -> Callable[..., LazyComponentDmcDateTimePicker]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.DatesProvider]
    ) -> Callable[..., LazyComponentDmcDatesProvider]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.DirectionProvider]
    ) -> Callable[..., LazyComponentDmcDirectionProvider]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Divider]
    ) -> Callable[..., LazyComponentDmcDivider]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.DonutChart]
    ) -> Callable[..., LazyComponentDmcDonutChart]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.DonutChart]
    ) -> Callable[..., LazyComponentDmcDonutChart]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Drawer]
    ) -> Callable[..., LazyComponentDmcDrawer]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.DrawerStack]
    ) -> Callable[..., LazyComponentDmcDrawerStack]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Fieldset]
    ) -> Callable[..., LazyComponentDmcFieldset]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Flex]
    ) -> Callable[..., LazyComponentDmcFlex]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.FloatingTooltip]
    ) -> Callable[..., LazyComponentDmcFloatingTooltip]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Grid]
    ) -> Callable[..., LazyComponentDmcGrid]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.GridCol]
    ) -> Callable[..., LazyComponentDmcGridCol]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Group]
    ) -> Callable[..., LazyComponentDmcGroup]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Highlight]
    ) -> Callable[..., LazyComponentDmcHighlight]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.HoverCard]
    ) -> Callable[..., LazyComponentDmcHoverCard]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.HoverCardDropdown]
    ) -> Callable[..., LazyComponentDmcHoverCardDropdown]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.HoverCardTarget]
    ) -> Callable[..., LazyComponentDmcHoverCardTarget]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Image]
    ) -> Callable[..., LazyComponentDmcImage]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Indicator]
    ) -> Callable[..., LazyComponentDmcIndicator]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.InlineCodeHighlight]
    ) -> Callable[..., LazyComponentDmcInlineCodeHighlight]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.InlineCodeHighlight]
    ) -> Callable[..., LazyComponentDmcInlineCodeHighlight]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.InputWrapper]
    ) -> Callable[..., LazyComponentDmcInputWrapper]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.JsonInput]
    ) -> Callable[..., LazyComponentDmcJsonInput]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Kbd]
    ) -> Callable[..., LazyComponentDmcKbd]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.LineChart]
    ) -> Callable[..., LazyComponentDmcLineChart]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.LineChart]
    ) -> Callable[..., LazyComponentDmcLineChart]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.List]
    ) -> Callable[..., LazyComponentDmcList]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.ListItem]
    ) -> Callable[..., LazyComponentDmcListItem]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Loader]
    ) -> Callable[..., LazyComponentDmcLoader]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.LoadingOverlay]
    ) -> Callable[..., LazyComponentDmcLoadingOverlay]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.ManagedDrawer]
    ) -> Callable[..., LazyComponentDmcManagedDrawer]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.ManagedModal]
    ) -> Callable[..., LazyComponentDmcManagedModal]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.MantineProvider]
    ) -> Callable[..., LazyComponentDmcMantineProvider]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Mark]
    ) -> Callable[..., LazyComponentDmcMark]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Menu]
    ) -> Callable[..., LazyComponentDmcMenu]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.MenuDivider]
    ) -> Callable[..., LazyComponentDmcMenuDivider]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.MenuDropdown]
    ) -> Callable[..., LazyComponentDmcMenuDropdown]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.MenuItem]
    ) -> Callable[..., LazyComponentDmcMenuItem]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.MenuLabel]
    ) -> Callable[..., LazyComponentDmcMenuLabel]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.MenuTarget]
    ) -> Callable[..., LazyComponentDmcMenuTarget]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.MiniCalendar]
    ) -> Callable[..., LazyComponentDmcMiniCalendar]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Modal]
    ) -> Callable[..., LazyComponentDmcModal]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.ModalStack]
    ) -> Callable[..., LazyComponentDmcModalStack]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.MonthPickerInput]
    ) -> Callable[..., LazyComponentDmcMonthPickerInput]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.MultiSelect]
    ) -> Callable[..., LazyComponentDmcMultiSelect]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.NavLink]
    ) -> Callable[..., LazyComponentDmcNavLink]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.NavigationProgress]
    ) -> Callable[..., LazyComponentDmcNavigationProgress]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.NavigationProgressProvider]
    ) -> Callable[..., LazyComponentDmcNavigationProgressProvider]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Notification]
    ) -> Callable[..., LazyComponentDmcNotification]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.NotificationContainer]
    ) -> Callable[..., LazyComponentDmcNotificationContainer]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.NotificationProvider]
    ) -> Callable[..., LazyComponentDmcNotificationProvider]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.NumberFormatter]
    ) -> Callable[..., LazyComponentDmcNumberFormatter]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.NumberInput]
    ) -> Callable[..., LazyComponentDmcNumberInput]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Overlay]
    ) -> Callable[..., LazyComponentDmcOverlay]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Pagination]
    ) -> Callable[..., LazyComponentDmcPagination]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Paper]
    ) -> Callable[..., LazyComponentDmcPaper]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.PasswordInput]
    ) -> Callable[..., LazyComponentDmcPasswordInput]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.PieChart]
    ) -> Callable[..., LazyComponentDmcPieChart]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.PieChart]
    ) -> Callable[..., LazyComponentDmcPieChart]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.PinInput]
    ) -> Callable[..., LazyComponentDmcPinInput]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Popover]
    ) -> Callable[..., LazyComponentDmcPopover]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.PopoverDropdown]
    ) -> Callable[..., LazyComponentDmcPopoverDropdown]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.PopoverTarget]
    ) -> Callable[..., LazyComponentDmcPopoverTarget]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Progress]
    ) -> Callable[..., LazyComponentDmcProgress]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.ProgressLabel]
    ) -> Callable[..., LazyComponentDmcProgressLabel]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.ProgressRoot]
    ) -> Callable[..., LazyComponentDmcProgressRoot]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.ProgressSection]
    ) -> Callable[..., LazyComponentDmcProgressSection]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.RadarChart]
    ) -> Callable[..., LazyComponentDmcRadarChart]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.RadarChart]
    ) -> Callable[..., LazyComponentDmcRadarChart]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Radio]
    ) -> Callable[..., LazyComponentDmcRadio]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.RadioCard]
    ) -> Callable[..., LazyComponentDmcRadioCard]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.RadioGroup]
    ) -> Callable[..., LazyComponentDmcRadioGroup]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.RadioGroupContext]
    ) -> Callable[..., LazyComponentDmcRadioGroupContext]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.RadioIndicator]
    ) -> Callable[..., LazyComponentDmcRadioIndicator]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.RangeSlider]
    ) -> Callable[..., LazyComponentDmcRangeSlider]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Rating]
    ) -> Callable[..., LazyComponentDmcRating]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.RichTextEditor]
    ) -> Callable[..., LazyComponentDmcRichTextEditor]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.RichTextEditor]
    ) -> Callable[..., LazyComponentDmcRichTextEditor]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.RingProgress]
    ) -> Callable[..., LazyComponentDmcRingProgress]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.ScatterChart]
    ) -> Callable[..., LazyComponentDmcScatterChart]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.ScatterChart]
    ) -> Callable[..., LazyComponentDmcScatterChart]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.ScrollArea]
    ) -> Callable[..., LazyComponentDmcScrollArea]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.ScrollAreaAutosize]
    ) -> Callable[..., LazyComponentDmcScrollAreaAutosize]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.SegmentedControl]
    ) -> Callable[..., LazyComponentDmcSegmentedControl]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Select]
    ) -> Callable[..., LazyComponentDmcSelect]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.SemiCircleProgress]
    ) -> Callable[..., LazyComponentDmcSemiCircleProgress]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.SimpleGrid]
    ) -> Callable[..., LazyComponentDmcSimpleGrid]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Skeleton]
    ) -> Callable[..., LazyComponentDmcSkeleton]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Slider]
    ) -> Callable[..., LazyComponentDmcSlider]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Space]
    ) -> Callable[..., LazyComponentDmcSpace]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Sparkline]
    ) -> Callable[..., LazyComponentDmcSparkline]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Sparkline]
    ) -> Callable[..., LazyComponentDmcSparkline]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Spoiler]
    ) -> Callable[..., LazyComponentDmcSpoiler]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Stack]
    ) -> Callable[..., LazyComponentDmcStack]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Stepper]
    ) -> Callable[..., LazyComponentDmcStepper]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.StepperCompleted]
    ) -> Callable[..., LazyComponentDmcStepperCompleted]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.StepperStep]
    ) -> Callable[..., LazyComponentDmcStepperStep]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.SubMenu]
    ) -> Callable[..., LazyComponentDmcSubMenu]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.SubMenuDropdown]
    ) -> Callable[..., LazyComponentDmcSubMenuDropdown]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.SubMenuItem]
    ) -> Callable[..., LazyComponentDmcSubMenuItem]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.SubMenuTarget]
    ) -> Callable[..., LazyComponentDmcSubMenuTarget]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Switch]
    ) -> Callable[..., LazyComponentDmcSwitch]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Table]
    ) -> Callable[..., LazyComponentDmcTable]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.TableCaption]
    ) -> Callable[..., LazyComponentDmcTableCaption]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.TableScrollContainer]
    ) -> Callable[..., LazyComponentDmcTableScrollContainer]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.TableTbody]
    ) -> Callable[..., LazyComponentDmcTableTbody]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.TableTd]
    ) -> Callable[..., LazyComponentDmcTableTd]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.TableTfoot]
    ) -> Callable[..., LazyComponentDmcTableTfoot]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.TableTh]
    ) -> Callable[..., LazyComponentDmcTableTh]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.TableThead]
    ) -> Callable[..., LazyComponentDmcTableThead]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.TableTr]
    ) -> Callable[..., LazyComponentDmcTableTr]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Tabs]
    ) -> Callable[..., LazyComponentDmcTabs]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.TabsList]
    ) -> Callable[..., LazyComponentDmcTabsList]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.TabsPanel]
    ) -> Callable[..., LazyComponentDmcTabsPanel]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.TabsTab]
    ) -> Callable[..., LazyComponentDmcTabsTab]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.TagsInput]
    ) -> Callable[..., LazyComponentDmcTagsInput]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Text]
    ) -> Callable[..., LazyComponentDmcText]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.TextInput]
    ) -> Callable[..., LazyComponentDmcTextInput]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Textarea]
    ) -> Callable[..., LazyComponentDmcTextarea]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.ThemeIcon]
    ) -> Callable[..., LazyComponentDmcThemeIcon]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.TimeGrid]
    ) -> Callable[..., LazyComponentDmcTimeGrid]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.TimeInput]
    ) -> Callable[..., LazyComponentDmcTimeInput]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.TimePicker]
    ) -> Callable[..., LazyComponentDmcTimePicker]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Timeline]
    ) -> Callable[..., LazyComponentDmcTimeline]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.TimelineItem]
    ) -> Callable[..., LazyComponentDmcTimelineItem]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Title]
    ) -> Callable[..., LazyComponentDmcTitle]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Tooltip]
    ) -> Callable[..., LazyComponentDmcTooltip]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.Tree]
    ) -> Callable[..., LazyComponentDmcTree]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.TypographyStylesProvider]
    ) -> Callable[..., LazyComponentDmcTypographyStylesProvider]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.UnstyledButton]
    ) -> Callable[..., LazyComponentDmcUnstyledButton]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.VisuallyHidden]
    ) -> Callable[..., LazyComponentDmcVisuallyHidden]: ...
    @overload
    def __getitem__(
        self, component_cls: type[dash_mantine_components.YearPickerInput]
    ) -> Callable[..., LazyComponentDmcYearPickerInput]: ...

    # Fallback for any other component type
    def __getitem__(self, component_cls: type) -> Callable[..., LazyComponent]: ...
