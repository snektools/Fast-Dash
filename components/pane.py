from abc import ABC, abstractmethod


class Pane(ABC):
    """
    Class for creating a container that contains visualizations,
    controls, callbacks and return a built html div.
    """

    def get_layout(self):
        return self._layout

    def __iter__(self):
        for cb in self._callbacks:
            yield cb

    @abstractmethod
    def _build_visualizations(self):
        pass

    @abstractmethod
    def _build_controls(self):
        pass

    @abstractmethod
    def _build_layout(self):
        pass

    @abstractmethod
    def _build_callbacks(self):
        pass
