import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

try:
    from components.controls.control import Control
except:
    from Fast_Dash.components.controls.control import Control


class Radio(Control):
    def _update_values(self):
        self._options = [
            {
                'label': key,
                'value': value,
            }
            for key, value in self._values.items()
        ]

    def _create_default_value(self):
        self._value = list(self._values.values())[0]

    def _create_component(self):
        self.dash_component = dcc.RadioItems(
            id=self._id,
            options=self._options,
            value=self._value,
        )

    def get_output(self, component_property='options'):
        return Output(component_id=self._id, component_property=component_property)

    def get_input(self, component_property='value'):
        return Input(component_id=self._id, component_property=component_property)

