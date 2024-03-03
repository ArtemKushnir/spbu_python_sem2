from typing import Generic, TypeVar

INTERFACE = TypeVar("INTERFACE")


class Registry(Generic[INTERFACE]):
    def __init__(self, default=None):
        self._default = default
        self._registry_storage = {}

    def register(self, name):
        print(name in self._registry_storage, self._registry_storage)
        if name in self._registry_storage:
            raise ValueError("This name is already reserved")

        def _decorator(cls):
            self._registry_storage[name] = cls
            return cls

        return _decorator

    def dispatch(self, name):
        if name in self._registry_storage or self._default:
            return self._registry_storage.get(name, self._default)
        raise ValueError("No class with this name found")
