from abc import ABC, abstractmethod


class Pane(ABC):
    """
    Class for creating a container that contains visualizations,
    controls, callbacks and return a built html div.
    """
    def __init__(self,):
        self._layout = None

    def get_layout(self):
        return self._layout

    @abstractmethod
    def _build_controls(self):
        pass

    @abstractmethod
    def _build_layout(self):
        pass
