import dash_html_components as html
import dash_core_components as dcc
try:
    from components.DCC import Dcc
except:
    from Fast_Dash.Layout_Components.DCC import Dcc

class DropDown(Dcc):

    def _create_values(self):
        pass