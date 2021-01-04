from abc import abstractmethod
import plotly.graph_objs as go
import dash_core_components as dcc
from dash.dependencies import Input, Output

from fast_dash.components import CoreComponent


class Plot(CoreComponent):
    def __init__(
            self,
            data_source,
            post_process_func=None,
            colorway=None,
            style=None,
            static_data_args=None,
            **kwargs
    ):
        self._assign_id()
        self._data_source = data_source
        self._post_process_func = post_process_func
        self._colorway = colorway or ['#581845', '#900C3F', '#C70039', '#FF5733', '#FFC300', '#DAF7A6']
        self._style = style
        self._go_data = None
        self._go_layout = None
        self._figure = None
        self._data = None
        self.dash_component = None
        self._static_data_args = static_data_args or dict()
        self._build_dash_component(**kwargs)

    def get_output(self, component_property='figure'):
        return Output(component_id=self._id, component_property=component_property)

    def get_input(self, component_property='select'):
        return Input(component_id=self._id, component_property=component_property)

    def _read_data(self, **kwargs):
        kwargs.update(self._static_data_args)
        self._data = self._data_source(**kwargs)

    def _post_process_data(self, **kwargs):
        if self._post_process_func:
            self._data = self._post_process_func(self._data)

    @abstractmethod
    def _build_plot_data(self, **kwargs):
        pass

    def _build_layout(self, **kwargs):
        self._go_layout = go.Layout()

    def _build_figure(self, **kwargs):
        self._figure = {'data': self._go_data, 'layout': self._go_layout}

    def update_component(self, **kwargs):
        self._read_data(**kwargs)
        self._post_process_data(**kwargs)
        self._build_plot_data(**kwargs)
        self._build_layout(**kwargs)
        self._build_figure(**kwargs)
        return self._figure

    def _build_dash_component(self, **kwargs):
        self.update_component(**kwargs)
        self.dash_component = dcc.Graph(id=self._id, figure=self._figure, style=self._style)
