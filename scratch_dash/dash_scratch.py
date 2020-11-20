import dash
import dash_html_components as html
from Data_Handling.SQL import SqlDataSource
from scratch_dash.pane_scratch import ScratchPane

app = dash.Dash(__name__)

sql_source = SqlDataSource(
    sql_folder_path=r'..\global_queries',
    sql_file_name='generic.sql',
    # cache=True,
)

pane = ScratchPane(
    data_source=sql_source.query.station_data,
    app=app,
    column_displayed='Left Clutch Matching 2 Torque Actual',
    database='C1_RDM',
    station='View_Station440',
)

app.layout = html.Div(
    pane.get_layout()
)

for cb in pane:
    @app.callback(cb.outputs,cb.inputs, cb.states)
    def func(*inputs):
        return cb.func(*inputs)


if __name__ == '__main__':
    app.run_server(debug=True)