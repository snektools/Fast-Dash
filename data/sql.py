from jinjaql import factory
import pathlib

class QueryStringEngine:
    def __init__(self, *args, **kwargs):
        self._build_query_string_engine(*args, **kwargs)

    def _build_query_string_engine(self):
        pass

    def get(self, parameters):
        pass

def build_data_source(
        connection_string=None,
        server=None,
        query_folder=None,
        query_name=None,
):
    pass

class SqlDataSource:

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
        if self._cache:
            query_factory = factory.JinJAQL(
                folder_path=self._sql_folder_path,
                engine=self._engine,
                cache=self._cache,
            )
        else:
            query_factory = factory.JinJAQL(
                folder_path=self._sql_folder_path,
                engine=self._engine,
            )
        self.query = query_factory.load_queries(self._sql_file_name)
