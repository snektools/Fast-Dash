import plotly.graph_objs as go
import dash_core_components as dcc


class Plot:

    def __init__(self, dcc_id, colorway=None):
        self._id = dcc_id
        self._go_data = None
        self._go_layout = None
        self._figure = None
        self._data = None
        self._colorway = colorway or ['#581845', '#900C3F', '#C70039', '#FF5733', '#FFC300', '#DAF7A6']
        self.dash_component = None

    def get_id(self):
        return self._id

    def _read_data(self):
        pass

    def _build_plot_data(self):
        pass

    def _build_layout(self):
        self._go_layout = go.Layout()

    def _build_figure(self):
        self._figure = {'data': self._go_data, 'layout': self._go_layout}

    def update_figure(self):
        self._read_data()
        self._build_plot_data()
        self._build_layout()
        self._build_figure()
        return self._figure

    def build_dash_component(self):
        self.update_figure()
        self.dash_component = dcc.Graph(id=self._id, figure=self._figure)
