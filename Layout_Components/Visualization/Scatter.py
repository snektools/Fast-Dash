import plotly.graph_objects as go
# TODO: Remove this once this goes to PtPi
try:
    from Layout_Components.Visualization.Plot import Plot
except:
    from Fast_Dash.Layout_Components.Visualization.Plot import Plot


class Scatter(Plot):
    def _post_process_data(self, **kwargs):
        pass

    def _build_plot_data(self, **kwargs):
        figure = go.Figure(
            go.Scatter(
                x=self._data[kwargs['x']],
                y=self._data[kwargs['y']],
            )
        )
        self._go_data = figure._data
