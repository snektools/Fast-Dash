import Data_Handling.SQL as sql
import timeit

test_dash = sql.SqlDataSource(
    sql_folder_path=r'C:\Users\david.smit\PycharmProjects\NWT_Dash\global_queries',
    sql_file_name='generic.sql',
    cache=True,
)

query = test_dash.query.station_data

# output_data = query(
#     station='View_Station445',
#     database='C1_RDM',
# )

def print_query():
    print(query(
        station='View_Station445',
        database='C1_RDM',
        top=1000,
    ))

print(timeit.timeit(print_query, number=6))
