from abc import ABC
import random
import string

random.seed(100)


class CoreComponent(ABC):
    ids = []

    @classmethod
    def _get_name(cls):
        return cls.__name__

    def _assign_id(self):
        new_id = self._get_name() + '_' + str(random.randrange(100, 900))
        if new_id in self.ids:
            self._assign_id()
        else:
            self._id = new_id

    def get_id(self):
        return self._id

    def _retrieve_current_attributes(self):
        self._user_arguments = {
            attribute: None
            for attribute in dir(self)
            if not callable(getattr(self, attribute))
        }

    def _set_default_arguments(self):
        pass

    def _record_default_arguments(self):
        current_arguments = {
            attribute
            for attribute in dir(self)
            if not callable(self.__getattribute__(attribute))
        }
        previous_arguments = set(self._user_arguments.keys())

        new_arguments = current_arguments - previous_arguments

        self._user_arguments = {
            argument: self.__getattribute__(argument)
            for argument in new_arguments
        }
        self._user_arguments.update(
            self._static_data_args
        )

    def _set_arguments(self, **kwargs) -> dict:
        for argument, default_value in self._user_arguments.items():
            self._set_argument(argument, default_value, **kwargs)
            kwargs.update(
                {
                    argument: self.__getattribute__(argument),
                }
            )
        return kwargs

    def _set_argument(self, arg_name, default, falsey_invalid=True, **kwargs):
        if arg_name in kwargs:
            value = kwargs[arg_name]
        else:
            value = default

        if falsey_invalid and not value:
            value = default

        self.__setattr__(arg_name, value)
