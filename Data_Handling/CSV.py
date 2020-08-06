from Data_Handling.DataSource import DataSource
import Data_Handling.dates as dates
import datetime
import pathlib
import pandas as pd
import pyodbc


class CsvDataSource(DataSource):
    def __init__(
            self,
            folder_path: str,
            filter: str,
    ):
        self._folder_path = pathlib.Path(folder_path)
        self._filter = filter
        self._read_file_paths()
        self._read_files()

    def _read_file_paths(self):
        self._file_paths = self._folder_path.rglob(f'{self._filter}*.csv')

    def _read_files(self):
        pass

    def get_data(
            self,
            start_date=None,
            end_date=None,
            time_frame: datetime.timedelta = datetime.timedelta(days=0.5)
    ):
        end_date = end_date or dates.create_end_date()
        start_date = start_date or dates.create_start_date(end_date, delta=time_frame)
        if self._is_new_request(start_date, end_date):
            self._start_date = start_date
            self._end_date = end_date
            query_str = self._build_query_str(start_date=start_date,end_date=end_date,)
            self._execute_query(query_str=query_str)

        return self._data

    def _is_new_request(self, start_date, end_date):
        # Throttle queries to 1 per minute
        return not (self._start_date and
                    self._end_date and
                    dates.within(time1=end_date, time2=self._end_date, minutes=1) and
                    dates.within(time1=start_date, time2=self._start_date, minutes=1)
                    )
