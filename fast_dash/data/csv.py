import pandas as pd
import pathlib

class MultipleCSVDataSource:
    def __init__(
            self,
            csv_folder_path: str,
            file_name_pattern: str = '*TestData.csv',
            recursive: bool = False,
            meta_data_engine=BepcoMeta,
            cache=None,
    ):
        self._csv_folder_path = pathlib.Path(csv_folder_path)
        self._recursive = recursive
        self._cache = cache
        self._meta_engine = meta_data_engine()

    def _load_files(self):
        pass

    def query(
            self,
            units_passed=True,
            units_failed=True,
            partial_trace=None,
            type=None,
            machine=None,
            cycle_id=None,
    ):
        if cycle_id:
            if cycle_id in self._cycles:
                return self._cycles[cycle_id]
            else:
                raise Exception('The cycle requested.')

        queried_cycle_ids = self._meta_engine.query_cycles(
            units_passed,
            units_failed,
            partial_trace,
            type,
            machine,
        )

        return self._get_ids(queried_cycle_ids)



