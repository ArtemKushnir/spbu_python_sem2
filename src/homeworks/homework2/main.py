from typing import Type

from src.homeworks.homework2.command_storage import *


def create_info(parent_class: Type) -> str:
    info = ""
    cnt = 1
    for cls in parent_class.__subclasses__():
        info += f"{cnt}. {cls.__doc__}\n"
        cnt += 1
    return info


def main() -> None:
    print("Write your collection")
    user_collection = eval(input("For example [], [1, 2, 3]: "))
    user_storage: PerformedCommandStorage = PerformedCommandStorage(user_collection)
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
            action, *arguments = user_request.split("--")
            arguments = map(int, arguments)
            try:
                user_storage.apply(ACTION_REGISTRY.dispatch(action.strip())(*arguments))
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
