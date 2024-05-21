from typing import Sequence

from src.homeworks.homework2.actions import *


class ActionIndexError(Exception):
    pass


class CollectionError(Exception):
    pass


class PerformedCommandStorage:
    def __init__(self, numbers_collection: Sequence):
        self.actions: list[Action] = []
        self.numbers: Sequence = numbers_collection

    def apply(self, action: Action) -> None:
        if not any(isinstance(self.numbers, getattr(cls, "collection_type")) for cls in type(action).__bases__):
            raise CollectionError("This collection does not support this action")
        action.do_action(self.numbers)
        self.actions.append(action)

    def cancel(self) -> None:
        if len(self.actions) > 0:
            self.actions[-1].undo_action(self.numbers)
            self.actions.pop()
        else:
            raise ActionIndexError("No action was performed")
