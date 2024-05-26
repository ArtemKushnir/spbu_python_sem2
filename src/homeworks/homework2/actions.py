from abc import abstractmethod
from typing import MutableSequence, Optional

from src.homeworks.homework1.registry import Registry

ACTION_REGISTRY = Registry["Action"]()


class ActionIndexError(Exception):
    pass


class CollectionError(Exception):
    pass


class ActionError(Exception):
    pass


class Action:
    def do_action(self, numbers: MutableSequence[int]) -> None:
        self.check_type(numbers)
        self._do_action(numbers)

    def undo_action(self, numbers: MutableSequence[int]) -> None:
        self.check_type(numbers)
        self._undo_action(numbers)

    @staticmethod
    def check_type(numbers: MutableSequence[int]) -> None:
        if not isinstance(numbers, MutableSequence):
            raise CollectionError("This collection does not support this action")

    @abstractmethod
    def _do_action(self, numbers: MutableSequence[int]) -> None:
        raise NotImplemented

    @abstractmethod
    def _undo_action(self, numbers: MutableSequence[int]) -> None:
        raise NotImplementedError


@ACTION_REGISTRY.register("insert_left")
class InsertLeft(Action):
    """insert_left --value (add an element to the beginning)"""

    def __init__(self, value: int):
        self.value: int = value

    def _do_action(self, numbers: MutableSequence[int]) -> None:
        numbers.insert(0, self.value)

    def _undo_action(self, numbers: MutableSequence[int]) -> None:
        numbers.pop(0)


@ACTION_REGISTRY.register("insert_right")
class InsertRight(Action):
    """insert_right --value (add an element to the end)"""

    def __init__(self, number: int):
        self.number: int = number

    def _do_action(self, numbers: MutableSequence[int]) -> None:
        numbers.append(self.number)

    def _undo_action(self, numbers: MutableSequence[int]) -> None:
        numbers.pop()


@ACTION_REGISTRY.register("move_element")
class MoveElement(Action):
    """move_element --i --j (move element from i to j position)"""

    def __init__(self, first_index: int, second_index: int):
        self.first_index: int = first_index
        self.second_index: int = second_index

    def _do_action(self, numbers: MutableSequence[int]) -> None:
        elem = numbers.pop(self.first_index)
        numbers.insert(self.second_index, elem)

    def _undo_action(self, numbers: MutableSequence[int]) -> None:
        elem = numbers.pop(self.second_index)
        numbers.insert(self.first_index, elem)


@ACTION_REGISTRY.register("add_value")
class AddValue(Action):
    """add_value --i --value (Add value to the element at position i)"""

    def __init__(self, index: int, value: int):
        self.index: int = index
        self.value: int = value

    def _do_action(self, numbers: MutableSequence[int]) -> None:
        numbers[self.index] += self.value

    def _undo_action(self, numbers: MutableSequence[int]) -> None:
        numbers[self.index] -= self.value


@ACTION_REGISTRY.register("reverse")
class Reverse(Action):
    """reverse (expand your collection)"""

    def _do_action(self, numbers: MutableSequence[int]) -> None:
        numbers.reverse()

    def _undo_action(self, numbers: MutableSequence[int]) -> None:
        self.do_action(numbers)


@ACTION_REGISTRY.register("swap")
class Swap(Action):
    """swap --i --j (swap elements at i and j positions)"""

    def __init__(self, first_index: int, second_index: int):
        self.first_index: int = first_index
        self.second_index: int = second_index

    def _do_action(self, numbers: MutableSequence[int]) -> None:
        numbers[self.first_index], numbers[self.second_index] = numbers[self.second_index], numbers[self.first_index]

    def _undo_action(self, numbers: MutableSequence[int]) -> None:
        self.do_action(numbers)


@ACTION_REGISTRY.register("pop")
class Pop(Action):
    """pop --i (remove element at i position)"""

    def __init__(self, index: int):
        self.index: int = index
        self.value: Optional[int] = None

    def _do_action(self, numbers: MutableSequence[int]) -> None:
        self.value = numbers.pop(self.index)

    def _undo_action(self, numbers: MutableSequence[int]) -> None:
        if self.value is None:
            raise ActionError("The deleted item was not saved")
        numbers.insert(self.index, self.value)


@ACTION_REGISTRY.register("clear")
class Clear(Action):
    """clear (clear collection)"""

    def __init__(self) -> None:
        self.numbers: Optional[MutableSequence] = None

    def _do_action(self, numbers: MutableSequence[int]) -> None:
        self.numbers = type(numbers)()
        self.numbers.extend(numbers)
        numbers.clear()

    def _undo_action(self, numbers: MutableSequence[int]) -> None:
        if self.numbers is not None:
            numbers.extend(self.numbers)


@ACTION_REGISTRY.register("multiply_value")
class MultiplyValue(Action):
    """multiply_value --i --value (Multiply by value the element at position i)"""

    def __init__(self, index: int, value: int):
        self.index: int = index
        self.value: int = value

    def _do_action(self, numbers: MutableSequence[int]) -> None:
        numbers[self.index] *= self.value

    def _undo_action(self, numbers: MutableSequence[int]) -> None:
        numbers[self.index] //= self.value


@ACTION_REGISTRY.register("delete_left")
class DeleteLeft(Action):
    """delete_left (delete the first element)"""

    def __init__(self) -> None:
        self.value: Optional[int] = None

    def _do_action(self, numbers: MutableSequence[int]) -> None:
        if len(numbers) == 0:
            raise ActionError("Collection is empty")
        self.value = numbers.pop(0)

    def _undo_action(self, numbers: MutableSequence[int]) -> None:
        if self.value is None:
            raise ActionError("The deleted item was not saved")
        numbers.insert(0, self.value)


@ACTION_REGISTRY.register("delete_right")
class DeleteRight(Action):
    """delete_right (delete the last element)"""

    def __init__(self) -> None:
        self.value: Optional[int] = None

    def _do_action(self, numbers: MutableSequence[int]) -> None:
        if len(numbers) == 0:
            raise ActionError("Collection is empty")
        self.value = numbers.pop()

    def _undo_action(self, numbers: MutableSequence[int]) -> None:
        if self.value is None:
            raise ActionError("The deleted item was not saved")
        numbers.append(self.value)
