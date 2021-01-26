from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import List, Dict, Optional, Tuple
import pandas as pd


def default_function(data, **kwargs):
    return data


def default_function_preprocessing(data, *args, **kwargs):
    return data, args, kwargs


class Handler(ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass


class DefaultHandler(Handler):
    def __init__(
            self,
            data_source: Callable,
            pre_processing_function: Callable = default_function_preprocessing,
            post_processing_function: Callable = default_function,
            aggregating_function: Callable = None,
            static_data_arguments: Dict = None,
    ):
        self._static_data_arguments = static_data_arguments or dict()
        self._data_source = data_source
        self._pre_processing_function = pre_processing_function
        self._queried_data = None
        self._post_processing_function = None
        self._create_post_process_function(post_processing_function)
        self._processed_data = None
        self._aggregating_function = aggregating_function or default_function
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

    def __call__(self, input_data: pd.DataFrame = None, *args, **kwargs):
        if not isinstance(input_data, pd.DataFrame):
            input_data = pd.DataFrame()
        input_data = input_data.copy(deep=True)
        input_data, args, kwargs = self._pre_processing_function(input_data, *args, **kwargs)
        kwargs = self._prepare_arguments(**kwargs)
        self._queried_data = self._data_source(**kwargs)
        self._processed_data = self._post_processing_function(self._queried_data, **kwargs)
        self._final_data = self._aggregating_function(self._processed_data, **kwargs)
        return self._final_data

    def _prepare_arguments(self, **kwargs):
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
            name: str,
            data_source: Callable,
            post_processing_function: Callable = None,
            aggregating_function: Callable = None,
            static_data_arguments: Dict = None,
            handler_obj: Handler = DefaultHandler,
    ):
        self.__setattr__(
            name,
            handler_obj(
                data_source=data_source,
                post_processing_function=post_processing_function,
                aggregating_function=aggregating_function,
                static_data_arguments=static_data_arguments,
            )
        )

    def chain(
            self,
            name,
            handlers: List[Callable],
            concat: bool = False,
    ):
        def chain_handlers(input_data: pd.DataFrame = None, *args, **kwargs):
            if not isinstance(input_data, pd.DataFrame):
                input_data = pd.DataFrame()
            data = input_data.copy(deep=True)
            for handler in handlers:
                new_handler_data = handler(input_data=input_data, *args, **kwargs)
                if concat:
                    data = pd.concat([data, new_handler_data])
                else:
                    data = new_handler_data
            return data

        self.__setattr__(
            name,
            chain_handlers
        )

    def merge(
            self,
            name,
            left_handler: Handler,
            right_handler: Handler,
            how: str = 'inner',
            on: Optional[List[str], str] = None,
            left_on: Optional[List[str], str]=None,
            right_on: Optional[List[str], str] = None,
            left_index: bool = False,
            right_index: bool = False,
            sort: bool = False,
            suffixes: Tuple[str] =('_x','_y'),
            copy: bool = True,
            indicator: bool = False,
            validate: str = None,
    ):
        def merge_handlers(input_data: pd.DataFrame = None, *args, **kwargs):
            if not isinstance(input_data, pd.DataFrame):
                input_data = pd.DataFrame()
            data = input_data.copy(deep=True)
            left_data = left_handler(input_data=data, *args, **kwargs)
            right_data = right_handler(input_data=data, *args, **kwargs)
            data = left_data.merge(
                right_data,
                how=how,
                left_on=left_on,
                right_on=right_on,
                left_index=left_index,
                right_index=right_index,
                sort=sort,
                suffixes=suffixes,
                copy=copy,
                indicator=indicator,
                validate=validate,
            )
            return data
        self.__setattr__(name, merge_handlers)
