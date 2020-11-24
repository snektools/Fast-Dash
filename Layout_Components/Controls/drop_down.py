import dash_html_components as html
import dash_core_components as dcc
try:
    from Layout_Components.DCC import Dcc
except:
    from Fast_Dash.Layout_Components.DCC import Dcc

class DropDown(Dcc):
    def __init__(self, values: dict, ):
        self._assign_id()
        self._values = values
        self._create_values()

    def _create_values(self):
        pass