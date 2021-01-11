import dash_core_components as dcc
from dash.dependencies import Input, Output

from fast_dash.components.controls.control import Control

class DropDown(Control):
    def __init__(
            self,
            values: dict = None,
            default_value=None,
            multi: bool=True
    ):
        self._multi = multi
        super().__init__(values=values, default_value=default_value)

    def _create_component(self):
        self.dash_component = dcc.Dropdown(
            id=self._id,
            options=self._options,
            value=self._value,
            multi=self._multi,
        )

    def get_output(self, component_property='options'):
        return [Output(component_id=self._id, component_property=component_property)]

    def get_input(self, component_property='value'):
        return [Input(component_id=self._id, component_property=component_property)]
