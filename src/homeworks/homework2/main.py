from typing import Type

from src.homeworks.homework1.registry import Registry
from src.homeworks.homework2.command_storage import *


def _create_registry(registry: Registry, parent_class: Type[Action]) -> Registry:
    for cls in parent_class.__subclasses__():
        for action in cls.__subclasses__():
            registry.register(action.__name__.lower())(action)
    return registry


def create_info(parent_class: Type) -> str:
    info = ""
    cnt = 1
    for cls in parent_class.__subclasses__():
        for action in cls.__subclasses__():
            info += f"{cnt}. {action.__doc__}\n"
            cnt += 1
    return info


def main() -> None:
    print("Write your collection")
    user_collection = eval(input("For example [], {1, 2, 3}: "))
    user_storage: PerformedCommandStorage = PerformedCommandStorage(user_collection)
    registry = _create_registry(Registry[Action](), Action)
    info = create_info(Action)
    print(info)
    user_request = input("write your request: ")
    while user_request != "exit":
        if user_request == "info":
            print(info)
        elif user_request == "cancel":
            try:
                user_storage.cancel()
            except ActionIndexError as e:
                print(e)
            else:
                print("Result:", user_storage.numbers)
        else:
            action, *arguments = user_request.replace("_", "").split("--")
            arguments = map(int, arguments)
            try:
                user_storage.apply(registry.dispatch(action.strip())(*arguments))
            except IndexError:
                print("Indexes are incorrectly specified")
            except ValueError:
                print("Invalid request")
            except TypeError:
                print("The request has an incorrect number of arguments")
            except CollectionError as e:
                print(e)
            else:
                print("Result:", user_storage.numbers)
        user_request = input("Write your request: ")


if __name__ == "__main__":
    main()
