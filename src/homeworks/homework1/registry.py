from typing import Callable, Generic, Optional, TypeVar

INTERFACE = TypeVar("INTERFACE")


class Registry(Generic[INTERFACE]):
    def __init__(self, default: Optional[INTERFACE] = None) -> None:
        self._default: Optional[INTERFACE] = default
        self._registry_storage: dict[str, INTERFACE] = {}

    def register(self, name: str) -> Callable:
        print(name in self._registry_storage, self._registry_storage)
        if name in self._registry_storage:
            raise ValueError("This name is already reserved")

        def _decorator(cls: INTERFACE) -> INTERFACE:
            self._registry_storage[name] = cls
            return cls

        return _decorator

    def dispatch(self, name: str) -> Optional[INTERFACE]:
        if name in self._registry_storage or self._default:
            return self._registry_storage.get(name, self._default)
        raise ValueError("No class with this name found")
