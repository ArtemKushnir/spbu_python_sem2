from src.homeworks.homework2.command_storage import *


def create_info() -> str:
    info = "1. exit (end the program)\n2. info (get info about actions)\n"
    for cnt, cls in enumerate(ACTION_REGISTRY._registry_storage.values(), start=3):
        info += f"{cnt}. {cls.__doc__}\n"
    return info


def main() -> None:
    print("Write your collection")
    user_collection = eval(input("For example [], [1, 2, 3]: "))
    user_storage: PerformedCommandStorage = PerformedCommandStorage(user_collection)
    info = create_info()
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
