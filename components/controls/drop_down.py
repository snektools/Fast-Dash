import dash_html_components as html
import dash_core_components as dcc
try:
    from components.core_component import CoreComponent
except:
    from Fast_Dash.components.core_component import CoreComponent

class DropDown(CoreComponent):

    def _create_values(self):
        pass