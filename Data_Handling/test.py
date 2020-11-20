import Data_Handling.SQL as sql
from Data_Handling.SQLengines import new_persist_engine
import timeit

test_dash = sql.SqlDataSource(
    sql_folder_path=r'..\global_queries',
    sql_file_name='generic.sql',
    cache=True,
    # engine=new_persist_engine,
)

query = test_dash.query.station_data

output_data = query(
    station='View_Station445',
    database='C1_RDM',
)
print(output_data)
# def print_query():
#     print(query(
#         station='View_Station445',
#         database='C1_RDM',
#         top=1000,
#     ))
#
# print(timeit.timeit(print_query, number=6))
