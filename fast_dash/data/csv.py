import pandas as pd
import pathlib


class MultipleFileDataSource:
    def __init__(
        self,
        csv_folder_path: str,
        meta_data_engine,
        read_csv_engine=pd.read_csv,
        file_name_pattern: str = "*TestData.csv",
        recursive: bool = False,
        cache=None,
        load_filter=None,
    ):
        self._csv_folder_path = pathlib.Path(csv_folder_path)
        self._recursive = recursive
        self._cache = cache
        self._file_name_pattern = file_name_pattern
        self._read_csv_engine = read_csv_engine
        self._meta_engine = meta_data_engine()
        self._files_paths = None
        self._files = dict()
        self._load_filter = load_filter
        self._load_files()

    def _filter_file_paths(self):
        if self._load_filter:
            self._files_paths = {
                key: value
                for key, value in self._files_paths.items()
                if self._load_filter(key)
            }

    def _load_files(self):
        if self._recursive:
            self._get_file_paths_recusrive()
        else:
            self._get_file_paths()

        self._filter_file_paths()

        for file_stem, file_path in self._files_paths.items():
            print(file_stem)
            temp_file = self._read_csv_engine(file_path)
            self._files.update({file_stem: None})
            self._meta_engine.add_cycle(file_stem, temp_file)

    def _get_file_paths(self):
        self._files_paths = {
            file_path.stem: file_path
            for file_path in self._csv_folder_path.glob(self._file_name_pattern)
        }

    def _get_file_paths_recusrive(self):
        self._files_paths = {
            file_path.stem: file_path
            for file_path in self._csv_folder_path.rglob(self._file_name_pattern)
        }

    def _get_ids(self, ids):
        return {id: self._read_csv_engine(self._files[id]) for id in ids}

    @property
    def ids(self):
        return tuple(self._files.keys())

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
            if cycle_id in self._files:
                return self._files[cycle_id]
            else:
                raise Exception("The cycle requested.")

        queried_cycle_ids = self._meta_engine.query_cycles(
            units_passed,
            units_failed,
            partial_trace,
            type,
            machine,
        )
        return self._get_ids(queried_cycle_ids)
