import dash_core_components as dcc
from dash.dependencies import Input, Output

from fast_dash.components.controls.control import Control

from typing import List, Dict


class Radio(Control):
    def __init__(
        self,
        values: List[str] = None,
        default_value: str = None,
        label_style: Dict = None,
    ):
        self._label_style = label_style
        super().__init__(values=values, default_value=default_value)

    def _create_component(self):
        self.dash_component = dcc.RadioItems(
            id=self._id,
            options=self._options,
            value=self._value,
            labelStyle=self._label_style,
        )

    def get_output(self, component_property="options"):
        return [Output(component_id=self._id, component_property=component_property)]

    def get_input(self, component_property="value"):
        return [Input(component_id=self._id, component_property=component_property)]
