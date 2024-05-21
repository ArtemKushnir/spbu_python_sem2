from typing import Collection, Generic, MutableSequence, MutableSet, Optional, TypeVar

from src.homeworks.homework1.registry import Registry

T = TypeVar("T", bound=Collection)

ACTION_REGISTRY = Registry["Action"]()


class ActionIndexError(Exception):
    pass


class CollectionError(Exception):
    def __init__(self, *args: Optional[str]) -> None:
        if args is not None:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self) -> str:
        if self.message:
            return self.message
        return "This collection does not support this action"


class Action(Generic[T]):
    def do_action(self, numbers: T) -> None:
        raise NotImplementedError

    def undo_action(self, numbers: T) -> None:
        raise NotImplementedError


class MutableSequenceAction(Action):
    collection_type = MutableSequence

    def do_action(self, numbers: MutableSequence) -> None:
        raise NotImplementedError

    def undo_action(self, numbers: MutableSequence) -> None:
        raise NotImplementedError


class MutableSetAction(Action):
    collection_type = MutableSet

    def do_action(self, numbers: MutableSet) -> None:
        raise NotImplementedError

    def undo_action(self, numbers: MutableSet) -> None:
        raise NotImplementedError


@ACTION_REGISTRY.register("insert_left")
class InsertLeft(MutableSequenceAction):
    """insert_left --value (add an element to the beginning)"""

    def __init__(self, value: int):
        self.value: int = value

    def do_action(self, numbers: MutableSequence) -> None:
        if not isinstance(numbers, self.collection_type):
            raise CollectionError
        numbers.insert(0, self.value)

    def undo_action(self, numbers: MutableSequence) -> None:
        numbers.pop(0)


@ACTION_REGISTRY.register("insert_right")
class InsertRight(MutableSequenceAction):
    """insert_right --value (add an element to the end)"""

    def __init__(self, number: int):
        self.number: int = number

    def do_action(self, numbers: MutableSequence) -> None:
        if not isinstance(numbers, self.collection_type):
            raise CollectionError
        numbers.append(self.number)

    def undo_action(self, numbers: MutableSequence) -> None:
        numbers.pop()


@ACTION_REGISTRY.register("move_element")
class MoveElement(MutableSequenceAction):
    """move_element --i --j (move element from i to j position)"""

    def __init__(self, first_index: int, second_index: int):
        self.first_index: int = first_index
        self.second_index: int = second_index

    def do_action(self, numbers: MutableSequence) -> None:
        if not isinstance(numbers, self.collection_type):
            raise CollectionError
        elem = numbers.pop(self.first_index)
        numbers.insert(self.second_index, elem)

    def undo_action(self, numbers: MutableSequence) -> None:
        elem = numbers.pop(self.second_index)
        numbers.insert(self.first_index, elem)


@ACTION_REGISTRY.register("add_value")
class AddValue(MutableSequenceAction):
    """add_value --i --value (Add value to the element at position i)"""

    def __init__(self, index: int, value: int):
        self.index: int = index
        self.value: int = value

    def do_action(self, numbers: MutableSequence) -> None:
        if not isinstance(numbers, self.collection_type):
            raise CollectionError
        numbers[self.index] += self.value

    def undo_action(self, numbers: MutableSequence) -> None:
        numbers[self.index] -= self.value


@ACTION_REGISTRY.register("reverse")
class Reverse(MutableSequenceAction):
    """reverse (expand your collection)"""

    def do_action(self, numbers: MutableSequence) -> None:
        if not isinstance(numbers, self.collection_type):
            raise CollectionError
        numbers.reverse()

    def undo_action(self, numbers: MutableSequence) -> None:
        self.do_action(numbers)


@ACTION_REGISTRY.register("swap")
class Swap(MutableSequenceAction):
    """swap --i --j (swap elements at i and j positions)"""

    def __init__(self, first_index: int, second_index: int):
        self.first_index: int = first_index
        self.second_index: int = second_index

    def do_action(self, numbers: MutableSequence) -> None:
        if not isinstance(numbers, self.collection_type):
            raise CollectionError
        numbers[self.first_index], numbers[self.second_index] = numbers[self.second_index], numbers[self.first_index]

    def undo_action(self, numbers: MutableSequence) -> None:
        self.do_action(numbers)


@ACTION_REGISTRY.register("add")
class Add(MutableSetAction):
    """add --value (add an element to the collection)"""

    def __init__(self, value: int) -> None:
        self.value: int = value
        self.repeat = False

    def do_action(self, numbers: MutableSet) -> None:
        if not isinstance(numbers, self.collection_type):
            raise CollectionError
        if self.value in numbers:
            self.repeat = True
        numbers.add(self.value)

    def undo_action(self, numbers: MutableSet) -> None:
        if not self.repeat:
            numbers.remove(self.value)


@ACTION_REGISTRY.register("pop")
class Pop(MutableSequenceAction):
    """pop --i (remove element at i position)"""

    def __init__(self, index: int):
        self.index: int = index
        self.value: Optional[int] = None

    def do_action(self, numbers: MutableSequence) -> None:
        if not isinstance(numbers, self.collection_type):
            raise CollectionError
        self.value = numbers.pop(self.index)

    def undo_action(self, numbers: MutableSequence) -> None:
        numbers.insert(self.index, self.value)


@ACTION_REGISTRY.register("clear")
class Clear(MutableSequenceAction):
    """clear (clear collection)"""

    def __init__(self) -> None:
        self.numbers: Optional[MutableSequence] = None

    def do_action(self, numbers: MutableSequence) -> None:
        if not isinstance(numbers, self.collection_type):
            raise CollectionError
        self.numbers = type(numbers)()
        self.numbers.extend(numbers)
        numbers.clear()

    def undo_action(self, numbers: MutableSequence) -> None:
        if self.numbers is not None:
            numbers.extend(self.numbers)


@ACTION_REGISTRY.register("discard")
class Discard(MutableSetAction):
    """discard --value (remove value without raising exceptions)"""

    def __init__(self, value: int) -> None:
        self.value: int = value
        self.delete: bool = False

    def do_action(self, numbers: MutableSet) -> None:
        if not isinstance(numbers, self.collection_type):
            raise CollectionError
        if self.value in numbers:
            self.delete = True
        numbers.discard(self.value)

    def undo_action(self, numbers: MutableSet) -> None:
        if self.delete:
            numbers.add(self.value)


@ACTION_REGISTRY.register("pop_random")
class PopRandom(MutableSetAction):
    """pop_random (removes a random value)"""

    def __init__(self) -> None:
        self.pop_value: Optional[int] = None

    def do_action(self, numbers: MutableSet) -> None:
        if not isinstance(numbers, self.collection_type):
            raise CollectionError
        self.pop_value = numbers.pop()

    def undo_action(self, numbers: MutableSet) -> None:
        numbers.add(self.pop_value)
