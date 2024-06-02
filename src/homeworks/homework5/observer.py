from typing import Any, Callable


class Observable:
    def __init__(self) -> None:
        self._value = None
        self.callbacks: list[Callable] = []

    def add_callback(self, func: Callable) -> Callable:
        pos = len(self.callbacks)
        self.callbacks.append(func)
        return lambda: self.callbacks.pop(pos)

    def _do_callbacks(self) -> None:
        for func in self.callbacks:
            func(self.value)

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, new_value: Any) -> None:
        self._value = new_value
        self._do_callbacks()

    @value.deleter
    def value(self) -> None:
        self._value = None
        self.callbacks = []
