from dash import Dash
import dash_html_components as html


class FastDash(Dash):
    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_pane(self, pane):
        self._new_pane(pane)

    def build_pane(self, data_source, visualization, filters=None):
        pass

    def _new_pane(self, pane):
        if not hasattr(self, '_panes'):
            self._panes = []
        self._panes.append(pane)
        self._update_layout()
        self._register_callbacks(pane)

    def _update_layout(self):
        self.layout = html.Div(
            [
                pane.get_layout()
                for pane in self._panes
            ]
        )

    def _register_callbacks(self, pane):
        for cb in pane:
            self.callback(cb.outputs, cb.inputs, cb.states)(cb.func)
