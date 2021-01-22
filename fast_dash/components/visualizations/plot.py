from abc import abstractmethod
import plotly.graph_objs as go
import dash_core_components as dcc
from dash.dependencies import Input, Output
from fast_dash.components import CoreComponent


class Plot(CoreComponent):
    def __init__(
            self,
            data_source,
            colorway=None,
            style=None,
            static_data_args=None,
            **kwargs
    ):
        self._assign_id()
        self._data_source = data_source
        self._colorway = colorway or ['#581845', '#900C3F', '#C70039', '#FF5733', '#FFC300', '#DAF7A6']
        self._style = style
        self._go_data = None
        self._go_layout = None
        self._figure = None
        self._data = None
        self.dash_component = None
        self._static_data_args = static_data_args or {}
        self._user_arguments = {}
        self._retrieve_current_attributes()
        self._set_default_arguments()
        self._record_default_arguments()
        self._build_dash_component(**kwargs)

    def _retrieve_current_attributes(self):
        self._user_arguments = {
            attribute: None
            for attribute in dir(self)
            if not callable(getattr(self, attribute))
        }

    def _set_default_arguments(self):
        pass

    def _record_default_arguments(self):
        new_arguments = {
            attribute
            for attribute in dir(self)
            if not callable(self.__getattribute__(attribute))
        } - set(self._user_arguments.keys())
        self._user_arguments = {
            argument: self.__getattribute__(argument)
            for argument in new_arguments
        }
        self._user_arguments.update(
            self._static_data_args
        )

    def _set_arguments(self, **kwargs):
        for argument, default_value in self._user_arguments.items():
            self._set_argument(argument, default_value, **kwargs)

    def _set_argument(self, arg_name, default, falsey_invalid=True, **kwargs):
        if arg_name in kwargs:
            value = kwargs[arg_name]
        else:
            value = default

        if falsey_invalid and not value:
            value = default

        self.__setattr__(arg_name, value)

    def get_output(self, component_property='figure'):
        return [Output(component_id=self._id, component_property=component_property)]

    def get_input(self, component_property='select'):
        return [Input(component_id=self._id, component_property=component_property)]

    @abstractmethod
    def _build_plot_data(self, **kwargs):
        pass

    def _build_layout(self, **kwargs):
        self._go_layout = go.Layout()

    def _build_figure(self):
        self._figure = {'data': self._go_data, 'layout': self._go_layout}

    def update_component(self, **kwargs):
        self._data = self._data_source(**kwargs)
        self._set_arguments(**kwargs)
        self._build_plot_data(**kwargs)
        self._build_layout(**kwargs)
        self._build_figure()
        return self._figure

    def _build_dash_component(self, **kwargs):
        self.update_component(**kwargs)
        self.dash_component = dcc.Graph(id=self._id, figure=self._figure, style=self._style)
