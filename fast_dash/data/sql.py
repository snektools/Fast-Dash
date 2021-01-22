from jinjaql import factory
import pathlib


class SqlSource:

    def __init__(
            self,
            sql_folder_path,
            sql_file_name,
            engine,
            cache=None,
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


