from abc import abstractmethod
import plotly.graph_objs as go
import dash_core_components as dcc
from dash.dependencies import Input, Output

import pandas as pd

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
        self._processed_data = pd.DataFrame()
        self._aggregated_data = pd.DataFrame()
        self._output_data = None
        self._static_data_args = static_data_args or dict()
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
        # TODO Test if this is necesary and delete
        # elif arg_name in self._static_data_args:
        #     value = self._static_data_args[arg_name]
        else:
            value = default

        if falsey_invalid and not value:
            value = default

        self.__setattr__(arg_name, value)

    def get_output(self, component_property='figure'):
        return [Output(component_id=self._id, component_property=component_property)]

    def get_input(self, component_property='select'):
        return [Input(component_id=self._id, component_property=component_property)]

    def _read_data(self, **kwargs):
        kwargs.update(self._static_data_args)
        kwargs = {
            key:value
            for key, value in kwargs.items()
            if key[:1] != '_'
        }
        self._data = self._data_source(**kwargs)

    def _post_process_data_user_func(self, **kwargs):
        if self._post_process_func:
            self._processed_data = self._post_process_func(self._data, **kwargs)
        else:
            self._processed_data = self._data

    def _post_process_data(self, **kwargs):
        pass

    def _aggregate_data(self, **kwargs):
        pass

    def _set_data_to_output(self):
        if len(self._aggregated_data) > 0:
            self._output_data = self._aggregated_data
            return
        else:
            self._output_data = self._processed_data
            return

    @abstractmethod
    def _build_plot_data(self, **kwargs):
        pass

    def _build_layout(self, **kwargs):
        self._go_layout = go.Layout()

    def _build_figure(self, **kwargs):
        self._figure = {'data': self._go_data, 'layout': self._go_layout}

    def update_component(self, **kwargs):
        self._read_data(**kwargs)
        self._set_arguments(**kwargs)
        self._post_process_data_user_func(**kwargs)
        self._post_process_data(**kwargs)
        # TODO: Can all parameters be pulled out so you don't have to pass kwargs?
        self._aggregate_data()
        self._set_data_to_output()
        self._build_plot_data(**kwargs)
        self._build_layout(**kwargs)
        self._build_figure(**kwargs)
        return self._figure

    def _build_dash_component(self, **kwargs):
        self.update_component(**kwargs)
        self.dash_component = dcc.Graph(id=self._id, figure=self._figure, style=self._style)

    def get_raw_data(self):
        return self._data.copy(deep=True)

    def get_processed_data(self):
        return self._processed_data.copy(deep=True)
