from .control import Control
import dash_core_components as dcc
from dash.dependencies import Input, Output


class Interval(Control):
    def _update_values(self):
        pass

    def _create_default_value(self):
        pass

    def _create_component(self):
        self.dash_component = dcc.Interval(
            id=self._id,
            interval=self._values['interval'],
            n_intervals=0
        )

    def get_output(self, component_property='interval'):
        return [Output(component_id=self._id, component_property=component_property)]

    def get_input(self, component_property='n_intervals'):
        return [Input(component_id=self._id, component_property=component_property)]
