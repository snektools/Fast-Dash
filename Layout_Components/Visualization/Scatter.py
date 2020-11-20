import  plotly.graph_objects as go
from Layout_Components.Visualization.Plot import Plot

class Scatter(Plot):
    def _post_process_data(self, **kwargs):
        pass

    def _build_plot_data(self, **kwargs):
        figure = go.Figure(
            go.Scatter(
                x=self._data['TimeStamp'],
                y=self._data[kwargs['column_displayed']],
            )
        )
        self._go_data = figure._data
