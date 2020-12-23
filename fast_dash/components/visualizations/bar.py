import plotly.graph_objects as go
from fast_dash.components.visualizations.plot import Plot
import numpy as np



class Bar(Plot):
    def _post_process_data(self, **kwargs):
        x_agg = self._x_agg
        y_agg = self._y_agg
        x = self._x
        y = self._y
        if x_agg and type(self._data[x_agg].values[0]) is np.datetime64:
            self._data = 1
        elif x_agg in self._data:
            self._data = self._data.groupby(x_agg)

    def _build_plot_data(self, **kwargs):
        if self.self._data[self._x_agg]
        figure = go.Figure(
            go.Scatter(
                x=self._data[kwargs['x']],
                y=self._data[kwargs['y']],
            )
        )
        self._go_data = figure._data

    def
