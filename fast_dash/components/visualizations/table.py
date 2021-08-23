import dash_table
from dash.dependencies import Input, Output
import pandas as pd
from fast_dash.components import CoreComponent


class Table(CoreComponent):
    def __init__(
            self,
            data_source,
            static_data_args=None,
            **kwargs
    ):
        self._assign_id()
        self._data_source = data_source
        self._data = None
        self._table = None
        self.dash_component = None
        self._static_data_args = static_data_args or {}
        self._user_arguments = {}
        self._build_dash_component(**kwargs)

    def get_output(self, component_property='data'):
        return [Output(component_id=self._id, component_property=component_property)]

    def get_input(self, component_property='select'):
        return [Input(component_id=self._id, component_property=component_property)]

    def _build_table(self):
        self._table = dash_table.DataTable(
            id=self._id,
            columns=[{'name': column, 'id': column} for column in self._data.columns],
            data=self._data.to_dict('records'),
        )

    def update_component(self, **kwargs):
        kwargs = self._set_arguments(**kwargs)
        self._data = self._data_source(**kwargs)
        self._build_table()
        return self._data.to_dict('records')

    def _build_dash_component(self, **kwargs):
        self.update_component(**kwargs)
        self._build_table()
        self.dash_component = self._table


