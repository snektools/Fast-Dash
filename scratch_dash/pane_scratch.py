from Layout_Components.Pane import Pane
from Layout_Components.Visualization.Scatter import Scatter
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from Callbacks.callback import CallbackDefinition

class ScratchPane(Pane):
    def __init__(self, data_source, **kwargs):
        self._layout = None
        self._data_source = data_source
        self._build_visualizations(**kwargs)
        self._build_controls(**kwargs)
        self._build_layout()
        self._build_callbacks()

    def _build_visualizations(self, **kwargs):
        self._scatter = Scatter(dcc_id='scratchit', data_source=self._data_source, **kwargs)

    def _build_controls(self, **kwargs):
        self._radio_side = dcc.RadioItems(
            id='side',
            options=[
                {
                    'label':'Right Clutch Matching 2 Torque Actual',
                    'value':'Right Clutch Matching 2 Torque Actual',
                },
                {
                    'label': 'Left Clutch Matching 2 Torque Actual',
                    'value': 'Left Clutch Matching 2 Torque Actual',
                }
            ],
            value=kwargs['column_displayed'],
        )
        self._radio_machine = dcc.RadioItems(
            id='machine',
            options=[
                {
                    'label': 'Station 440',
                    'value': 'View_Station440',
                },
                {
                    'label': 'Station 445',
                    'value': 'View_Station445',
                }
            ],
            value=kwargs['station'],
        )


    def _build_layout(self):
        self._layout = html.Div(
            [
                self._scatter.dash_component,
                self._radio_side,
                self._radio_machine
            ]
        )

    def _build_callbacks(self):
        def scatter_sort(side, machine):
            return [self._scatter.update_figure(database='C1_RDM',station=machine,column_displayed=side)]

        self._callbacks = [
            CallbackDefinition(
                inputs=[
                    Input(component_id='side', component_property='value'),
                    Input(component_id='machine', component_property='value'),
                ],
                outputs=[
                    Output(component_id=self._scatter.get_id(), component_property='figure'),
                ],
                func=scatter_sort,
            )
        ]


