from Data_Handling.DataSource import DataSource
import Data_Handling.dates as dates
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
        self._start_date = None
        self._end_date = None

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

    def get_data(
            self,
            start_date=None,
            end_date=None,
            days=0.5
    ):
        end_date = end_date or dates.create_end_date()
        start_date = start_date or dates.create_start_date(end_date, delta=days)
        if self._is_new_request(start_date, end_date):
            self._start_date = start_date
            self._end_date = end_date
            self._build_query_str(
                start_date=start_date,
                end_date=end_date,
            )
            self._execute_query()

        return self._data

    def _is_new_request(self, start_date, end_date):
        # Throttle queries to 1 per minute
        return not (self._start_date and
                    self._end_date and
                    dates.within(time1=end_date, time2=self._end_date, minutes=1) and
                    dates.within(time1=start_date, time2=self._start_date, minutes=1)
                    )
