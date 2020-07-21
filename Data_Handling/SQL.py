from Data_Handling.DataSource import DataSource
import pandas as pd


class SqlDataSource(DataSource):
    def __init__(
            self,
            sql_filepath,
            conn_obj,
            replace
    ):
        self._sql_filepath = sql_filepath
        self._read_file()
        self._connection = conn_obj
        self.replace = replace

    def _read_file(self):
        pass

    def _build_query_str(
            self,
            start_date=None,
            end_date=None,
    ):
        pass

    def _execute_query(
            self,
            query_str,
    ):
        self._data = pd.read_sql_query(sql=query_str, con=self._connection)
        # TODO: Do we need to close connection?

    def get_data_date_range(
            self,
            start_date=None,
            end_date=None,
    ):
        if self._is_not_within_minute(start_date, end_date):
            self._start_date = start_date
            self._end_date = end_date
            self._build_query_str(
                start_date=start_date,
                end_date=end_date,
            )
            self._execute_query()

        return self._data

    def _is_not_within_minute(self, start_date, end_date):
        pass
