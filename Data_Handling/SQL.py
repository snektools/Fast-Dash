from Data_Handling.DataSource import DataSource
from codecs import open
import Data_Handling.dates as dates
import datetime
import pandas as pd
import pyodbc
# Use snaql class to pass file path and return queries.


class SqlDataSource(DataSource):
    def __init__(
            self,
            sql_filepath,
            conn_str='DRIVER=SQL Server;SERVER=DLNWTSR140;Trusted_Connection=Yes',
    ):
        self._sql_filepath = sql_filepath
        self._read_file()
        self._conn_str = conn_str
        self._start_date = None
        self._end_date = None
        self._query_string_engine = None  # Snaql

    def _read_file(self):
        with open(self._sql_filepath, encoding='utf16') as file:
            self._sql_file_str = file.read()

    def _build_query_str(
            self,
            start_date=None,
            end_date=None,
            replace=None,
    ):
        pass

    def _execute_query(
            self,
            query_str,
    ):
        try:
            connection = pyodbc.connect(self._conn_str)
            self._data = pd.read_sql_query(sql=query_str, con=connection)
        except pyodbc.Error as e:
            print(e)
        finally:
            connection.close()

    def get_data(
            self,
            start_date=None,
            end_date=None,
            replace=None,
            time_frame: datetime.timedelta = datetime.timedelta(days=0.5),
    ):
        end_date = end_date or dates.create_end_date()
        start_date = start_date or dates.create_start_date(end_date, delta=time_frame)
        if self._is_new_request(start_date, end_date):
            self._start_date = start_date
            self._end_date = end_date
            query_str = self._build_query_str(start_date=start_date, end_date=end_date, replace=replace)
            self._execute_query(query_str=query_str)

        return self._data

    def _is_new_request(self, start_date, end_date):
        # Throttle queries to 1 per minute
        return not (self._start_date and
                    self._end_date and
                    dates.within(time1=end_date, time2=self._end_date, minutes=1) and
                    dates.within(time1=start_date, time2=self._start_date, minutes=1)
                    )
