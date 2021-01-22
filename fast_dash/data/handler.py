from abc import ABC, abstractmethod


def default_function(data):
    return data


class Handler(ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class DefaultHandler(Handler):
    def __init__(
            self,
            data_source: callable,
            post_processing_function: callable = default_function,
            aggregating_function: callable = default_function,
            static_data_arguments = None
    ):
        self._static_data_arguments = static_data_arguments or dict()
        self._data_source = data_source
        self._queried_data = None
        self._post_processing_function = post_processing_function
        self._processed_data = None
        self._aggregating_function = aggregating_function
        self._final_data = None

    def __call__(self, *args, **kwargs):
        kwargs = self._prepare_arguments(**kwargs)
        self._queried_data = self._data_source(**kwargs)
        self._processed_data = self._post_processing_function(self._queried_data)
        self._final_data = self._aggregating_function(self._processed_data)

    def _prepare_arguments(self, kwargs):
        kwargs.update(self._static_data_arguments)
        kwargs = {
            key: value
            for key, value in kwargs.items()
            if key[:1] != '_'
        }
        return kwargs


class DataHandlers:
    def __init__(self):
        pass

    def create_handler(
            self,
            data_source: callable,
            post_processing_function: callable = None,
            aggregating_fuction: callable =None,
            HandlerObj: Handler = DefaultHandler
    ):
        self.__setattr__(
            'name',
            HandlerObj(
                data_source=data_source,
                post_processing_function=post_processing_function,
                aggregating_function=aggregating_fuction,
            )
        )