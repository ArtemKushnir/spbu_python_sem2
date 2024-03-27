from collections import Counter, OrderedDict, UserDict, defaultdict
from typing import Callable, Generic, Optional, Type, TypeVar

R = TypeVar("R")


class Registry(Generic[R]):
    def __init__(self, default: Optional[Type[R]] = None) -> None:
        self._default: Optional[Type[R]] = default
        self._registry_storage: dict[str, Type[R]] = {}

    def register(self, name: str) -> Callable:
        if name in self._registry_storage:
            raise ValueError("This name is already reserved")

        def _decorator(cls: Type[R]) -> Type[R]:
            self._registry_storage[name] = cls
            return cls

        return _decorator

    def dispatch(self, name: str) -> Type[R]:
        dispatch_class = self._registry_storage.get(name, self._default)
        if dispatch_class is not None:
            return dispatch_class
        raise ValueError("No class with this name found")


def main() -> None:
    mapping_registry = Registry[dict](dict)
    mapping_registry.register("default_dict")(defaultdict)
    mapping_registry.register("ordered_dict")(OrderedDict)
    mapping_registry.register("user_dict")(UserDict)
    mapping_registry.register("counter")(Counter)
    print("select one of the following dictionaries:\n1.DefaultDict\n2.OrderedDict\n3.UserDict\n4.Counter")
    user_input = input()
    if user_input == "1":
        user_dict = mapping_registry.dispatch("default_dict")()
    elif user_input == "2":
        user_dict = mapping_registry.dispatch("ordered_dict")()
    elif user_input == "3":
        user_dict = mapping_registry.dispatch("user_dict")()
    elif user_input == "4":
        user_dict = mapping_registry.dispatch("counter")()
    user_dict[1] = "Python"
    user_dict[2] = "C"
    user_dict[3] = "Java"
    user_dict[4] = "C#"
    print("Your dict with random data:", user_dict)


if __name__ == "__main__":
    main()
