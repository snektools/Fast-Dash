from abc import ABC, abstractmethod


def default_function(data, **kwargs):
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
            static_data_arguments=None
    ):
        self._static_data_arguments = static_data_arguments or dict()
        self._data_source = data_source
        self._queried_data = None
        self._post_processing_function = None
        self._create_post_process_function(post_processing_function)
        self._processed_data = None
        self._aggregating_function = aggregating_function
        self._final_data = None

    def _create_post_process_function(self, post_processing_function):
        if callable(post_processing_function):
            self._post_processing_function = post_processing_function
        elif isinstance(post_processing_function, (list, tuple, set)):
            def post_processing_functions(data, **kwargs):
                for function in post_processing_function:
                    data = function(data, **kwargs)
                return data
            self._post_processing_function = post_processing_functions
        else:
            raise('A function or colleciton of functions needs to be passed for post_processing_function')

    def __call__(self, *args, **kwargs):
        kwargs = self._prepare_arguments(**kwargs)
        self._queried_data = self._data_source(**kwargs)
        self._processed_data = self._post_processing_function(self._queried_data, **kwargs)
        self._final_data = self._aggregating_function(self._processed_data, **kwargs)
        return self._final_data

    def _prepare_arguments(self, kwargs):
        kwargs.update(self._static_data_arguments)
        kwargs = {
            key: value
            for key, value in kwargs.items()
            if key[:1] != '_'
        }
        return kwargs

    @property
    def queried_data(self):
        return self._queried_data

    @property
    def processed_data(self):
        return self._processed_data

    @property
    def data(self):
        return self._final_data

class DataHandlers:
    def __init__(self):
        pass

    def create_handler(
            self,
            name,
            data_source: callable,
            post_processing_function: callable = None,
            aggregating_fuction: callable =None,
            handler_obj: Handler = DefaultHandler,
    ):
        self.__setattr__(
            name,
            handler_obj(
                data_source=data_source,
                post_processing_function=post_processing_function,
                aggregating_function=aggregating_fuction,
            )
        )