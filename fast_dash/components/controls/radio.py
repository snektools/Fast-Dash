import dash_core_components as dcc
from dash.dependencies import Input, Output

from fast_dash.components.controls.control import Control

class Radio(Control):

    def _create_component(self):
        self.dash_component = dcc.RadioItems(
            id=self._id,
            options=self._options,
            value=self._value,
        )

    def get_output(self, component_property='options'):
        return [Output(component_id=self._id, component_property=component_property)]

    def get_input(self, component_property='value'):
        return [Input(component_id=self._id, component_property=component_property)]

