class Plot:
    def __init__(self, data_source, query_name):
        self._data_source = data_source
        self._query_name = query_name

    def refresh(self,parameters=None):
        self._data_source.get_data(parameters, query_name)
