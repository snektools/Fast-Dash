from abc import ABC, abstractmethod
import plotly.graph_objs as go
import dash_core_components as dcc
import secrets



class Dcc(ABC):

    ids = []

    def _assign_id(self):
        new_id = secrets.token_urlsafe(16)
        if new_id in self.ids:
            self._assign_id()
        else:
            self._id = new_id

    def get_id(self):
        return self._id