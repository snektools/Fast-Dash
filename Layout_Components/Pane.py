class Pane:
    """
    Class for creating a container that contains visualizations,
    controls, callbacks and return a built html div.
    """
    def __init__(self,):
        self._layout = None

    def get_layout(self):
        return self._layout

    def _build_controls(self):
        pass

    def _build_layout(self):
        pass
