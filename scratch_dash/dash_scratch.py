import dash
import dash_html_components as html
from Data_Handling.SQL import SqlDataSource
from scratch_dash.pane_scratch import ScratchPane

app = dash.Dash(__name__)

sql_source = SqlDataSource(
    sql_folder_path=r'global_queries',
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

@app.callback(pane.outputs_1, pane.inputs_1)
def pane_callback(*inputs):
    return pane.func_1(*inputs)



if __name__ == '__main__':
    app.run_server(debug=True)