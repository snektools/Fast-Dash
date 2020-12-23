from abc import ABC
import secrets


class CoreComponent(ABC):
    ids = []

    @classmethod
    def _get_name(cls):
        return cls.__name__

    def _assign_id(self):
        new_id = self._get_name() + '_' + secrets.token_urlsafe(6)
        if new_id in self.ids:
            self._assign_id()
        else:
            self._id = new_id

    def get_id(self):
        return self._id
