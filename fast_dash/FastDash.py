from dash import Dash
import dash_html_components as html
import dash_core_components as dcc

class FastDash(Dash):
    _default_tab_name = 'default'
    def __init__(self, has_tabs=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tabs = {self._default_tab_name :[]}

    def add_pane(self, pane, tab_name=None):
        self._new_pane(pane, tab_name=tab_name)

    def build_pane(self, data_source, visualization, filters=None):
        pass

    def _new_pane(self, pane, tab_name):
        tab_name = tab_name or self._default_tab_name
        if tab_name in self._tabs:
            self._tabs[tab_name].append(pane)
        else:
            self._tabs.update(
                {
                    tab_name: [pane]
                }
            )
        self._update_layout()
        self._register_callbacks(pane)

    def _update_layout(self):
        if self._is_multi_tab():
            self._build_layout_tabbed()
        else:
            self._build_layout_single_page()


    def _is_multi_tab(self):
        return len(self._tabs) > 1

    def _build_layout_tabbed(self):
        self._layout = html.Div(
            [
                dcc.Tabs(
                    [
                        dcc.Tab(
                            label=name,
                            children=self._build_page(tab_name=name)
                        )
                        for name, panes in self._tabs.items()
                    ]
                )
            ]
        )

    def _build_layout_single_page(self):
        self._layout = self._build_page()

    def _build_page(self, tab_name=None):
        tab_name = tab_name or self._default_tab_name
        return html.Div(
            [
                pane.get_layout()
                for pane in self._tabs[tab_name]
            ]
        )

    def _register_callbacks(self, pane):
        for cb in pane:
            self.callback(cb.outputs, cb.inputs, cb.states)(cb.func)
