
import pandas as pd
import pyodbc
from jinjaql import factory
import pathlib

def nwt_engine(query_string: str, connection_string: str):
    """
    :param query_string: The raw query string to execute
    :param connection: Connection string formatted for use by PYODBC
    :return: A pandas DataFrame
    """
    connection = pyodbc.connect(connection_string)
    try:
        return pd.read_sql_query(query_string, connection)
    except Exception as e:
        print(e)
    finally:
        connection.close()

class SqlDataSource:
    def __init__(
            self,
            sql_folder_path,
            sql_file_name,
            engine=nwt_engine,
            cache=False,
    ):
        self._sql_folder_path = pathlib.Path(sql_folder_path)
        self._sql_file_name = sql_file_name
        self._engine = engine
        self._cache = cache
        self._build_queries()

    def _build_queries(self):
        query_factory = factory.JinJAQL(
            folder_path=self._sql_folder_path,
            engine=self._engine,
            cache=self._cache,
        )
        self.query = query_factory.load_queries(self._sql_file_name)
