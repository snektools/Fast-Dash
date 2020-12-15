import dash_core_components as dcc
from dash.dependencies import Input, Output

try:
    from fast_dash.components.controls.control import Control
except:
    from Fast_Dash.components.controls.control import Control

class DropDown(Control):
    def _update_values(self):
        if isinstance(self._values, dict):
            values = self._values
        else:
            values = {
                item:item
                for item in self._values
            }
        self._options = [
            {
                'label': key,
                'value': value,
            }
            for key, value in values.items()
        ]

    def _create_default_value(self):
        if isinstance(self._values, dict):
            self._value = list(self._values.values())[0]
        else:
            self._value = self._values[0]

    def _create_component(self):
        self.dash_component = dcc.Dropdown(
            id=self._id,
            options=self._options,
            value=self._value,
            multi=True,
        )

    def get_output(self, component_property='options'):
        return Output(component_id=self._id, component_property=component_property)

    def get_input(self, component_property='value'):
        return Input(component_id=self._id, component_property=component_property)
