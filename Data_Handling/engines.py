import pandas as pd
import pyodbc
from itsdangerous import Serializer

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


def new_persist_engine(query_string: str, connection_string: str):
    """
    :param query_string: The raw query string to execute
    :param connection: Connection string formatted for use by PYODBC
    :return: A pandas DataFrame
    """
    serializer = Serializer('jfksjdfisaeiojasfoiajsodifjioejfijefief',)
    return serializer.dumps(query_string)#.decode('utf-8')