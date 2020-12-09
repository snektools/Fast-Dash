from abc import ABC, abstractmethod


class Pane(ABC):
    """
    Class for creating a container that contains visualizations,
    controls, callbacks and return a built html div.
    """

    def __init__(self, data_source, **kwargs):
        self._data_source = data_source
        self._build_visualizations(**kwargs)
        self._build_controls(**kwargs)
        self._build_layout()
        self._build_callbacks()

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
