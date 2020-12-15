from abc import abstractmethod

try:
    from fast_dash.components import CoreComponent
except:
    from Fast_Dash.components.core_component import CoreComponent


class Control(CoreComponent):
    def __init__(self, values: dict = None, default_value=None):
        self._values = values
        self._assign_id()
        self._update_values()
        self._value = default_value or self._create_default_value()
        self._create_component()

    @abstractmethod
    def _update_values(self):
        pass

    @abstractmethod
    def _create_default_value(self):
        pass

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





