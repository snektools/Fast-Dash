from abc import abstractmethod

from fast_dash.components import CoreComponent



class Control(CoreComponent):
    def __init__(self, values: dict = None, default_value=None,):
        self._values = values
        self._assign_id()
        self._update_values()
        self._value = default_value or self._create_default_value()
        self._create_component()

    def _update_values(self):
        if isinstance(self._values, dict):
            values = self._values
        else:
            values = {
                item: item
                for item in self._values
            }
        self._options = [
            {
                'label': key,
                'value': value,
            }
            for key, value in values.items()
        ]

    def _create_default_value(self):
        return self._options[0]['value']

    @abstractmethod
    def _create_component(self):
        pass

    @abstractmethod
    def get_output(self):
        pass

    @abstractmethod
    def get_input(self):
        pass

    def update_component(self, values):
        self._value = values
        self._update_values()





