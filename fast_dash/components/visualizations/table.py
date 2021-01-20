import dash_table
from dash.dependencies import Input, Output
import pandas as pd

from fast_dash.components.visualizations.plot import Plot

def default_data_source(df):
    def return_data():
        return df

    return return_data

class Table(Plot):
    def __init__(
            self,
            data_source,
            post_process_func=None,
            colorway=None,
            style=None,
            static_data_args=None,
            **kwargs
    ):
        if isinstance(data_source, pd.DataFrame):
            data_source = default_data_source(data_source)
        elif callable(data_source):
            data_source = data_source
        else:
            raise Exception('Data source not valid, please pass in a dataframe or function')

        super().__init__(
            data_source,
            post_process_func,
            colorway,
            style,
            static_data_args,
            **kwargs
        )

    def get_output(self, component_property='data'):
        return [Output(component_id=self._id, component_property=component_property)]

    def _build_plot_data(self, **kwargs):
        pass

    def _build_dash_component(self, **kwargs):
        self.update_component(**kwargs)
        print(self.get_processed_data())
        self.dash_component = dash_table.DataTable(
            id=self._id,
            columns=[
                {'name': column, 'id': column}
                for column in self._output_data.columns
            ],
            data=self._output_data.to_dict('records'),
        )


