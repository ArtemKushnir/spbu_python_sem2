from abc import ABCMeta, abstractmethod
from random import random
from typing import Any, Callable, Generic, Iterator, MutableMapping, Optional, TypeVar


class Comparable(metaclass=ABCMeta):
    @abstractmethod
    def __lt__(self, other: Any) -> bool:
        ...

    @abstractmethod
    def __gt__(self, other: Any) -> bool:
        ...


Key = TypeVar("Key", bound=Comparable)
Value = TypeVar("Value")


class Node(Generic[Key, Value]):
    def __init__(self, key: Key, value: Value) -> None:
        self.key: Key = key
        self.value: Value = value
        self.priority: float = random()
        self.left: Optional["Node[Key, Value]"] = None
        self.right: Optional["Node[Key, Value]"] = None

    def __iter__(self) -> Iterator[Key]:
        if self.left:
            yield from self.left
        yield self.key
        if self.right:
            yield from self.right

    def __str__(self) -> str:
        return f"key: {self.key}, value: {self.value}, priority: {self.priority}"


class Comparator:
    def create_comparator(self) -> filter:
        raise NotImplementedError


class PreorderComparator(Comparator):
    def __init__(self, node: Node[Key, Value]) -> None:
        self.node: Node[Key, Value] = node

    def create_comparator(self) -> filter:
        return filter(None, (self.node, self.node.left, self.node.right))


class InorderComparator(Comparator):
    def __init__(self, node: Node[Key, Value]) -> None:
        self.node: Node[Key, Value] = node

    def create_comparator(self) -> filter:
        return filter(None, (self.node.left, self.node, self.node.right))


class PostorderComparator(Comparator):
    def __init__(self, node: Node[Key, Value]) -> None:
        self.node: Node[Key, Value] = node

    def create_comparator(self) -> filter:
        return filter(None, (self.node.left, self.node.right, self.node))


class CartesianTree(MutableMapping, Generic[Key, Value]):
    def __init__(self) -> None:
        self.root: Optional[Node[Key, Value]] = None
        self.size: int = 0

    def _is_empty(self) -> bool:
        return self.size == 0

    def __setitem__(self, key: Key, value: Value) -> None:
        if self._is_empty():
            self.root = Node(key, value)
            self.size = 1
        else:
            node = self._find_node(key)
            if node is not None:
                node.value = value
            else:
                smaller_root, bigger_root = self.split(self.root, key)
                smaller_root = self.merge(smaller_root, Node(key, value))
                self.root = self.merge(smaller_root, bigger_root)
                self.size += 1

    def __getitem__(self, key: Key) -> Value:
        node = self._find_node(key)
        if node is not None:
            return node.value
        raise KeyError

    def get(self, key: Key, default: Any = None) -> Value:
        try:
            return self[key]
        except KeyError:
            if default is not None:
                return default
            raise KeyError

    def traverse(self, order: str = "inorder") -> list[tuple[Key, Value]]:
        items: list[tuple[Key, Value]] = []
        if self.root is None:
            return items

        def traverse_recursion(curr_node: Node[Key, Value], order_func: Callable) -> None:
            node_order = order_func(curr_node).create_comparator()
            for node in node_order:
                if node is not curr_node:
                    traverse_recursion(node, order_func)
                else:
                    items.append((node.key, node.value))

        if order == "preorder":
            traverse_recursion(self.root, PreorderComparator)
        elif order == "inorder":
            traverse_recursion(self.root, InorderComparator)
        elif order == "postorder":
            traverse_recursion(self.root, PostorderComparator)
        return items

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterator[Key]:
        if self.root is not None:
            return iter(self.root)
        raise TypeError

    def __delitem__(self, key: Key) -> None:
        if not self.__contains__(key):
            raise KeyError
        smaller_root, bigger_root = self.split(self.root, key)
        if bigger_root is not None:
            if bigger_root.key == key:
                self.root = smaller_root
            else:
                curr_node = bigger_root
                while curr_node.left is not None:
                    parent_root = curr_node
                    curr_node = curr_node.left
                parent_root.left = None
                self.root = self.merge(smaller_root, bigger_root)
            self.size -= 1

    def pop(self, __key: Key, default: Any = None) -> Value:
        try:
            value = self[__key]
            del self[__key]
            return value
        except KeyError:
            if default is not None:
                return default
            raise KeyError

    def __contains__(self, key: object) -> bool:
        return self._find_node(key) is not None

    def _find_node(self, key: object) -> Optional[Node[Key, Value]]:
        curr_node = self.root
        while curr_node is not None:
            if curr_node.key == key:
                return curr_node
            elif curr_node.key > key:
                curr_node = curr_node.left
            else:
                curr_node = curr_node.right
        return None

    @staticmethod
    def split(
        tree_root: Optional[Node[Key, Value]], key: Key
    ) -> tuple[Optional[Node[Key, Value]], Optional[Node[Key, Value]]]:
        def recursion_split(
            curr_node: Optional[Node[Key, Value]]
        ) -> tuple[Optional[Node[Key, Value]], Optional[Node[Key, Value]]]:
            if curr_node is None:
                return None, None
            elif curr_node.key < key:
                smaller_node, bigger_node = recursion_split(curr_node.right)
                curr_node.right = smaller_node
                return curr_node, bigger_node
            else:
                smaller_node, bigger_node = recursion_split(curr_node.left)
                curr_node.left = bigger_node
                return smaller_node, curr_node

        return recursion_split(tree_root)

    @staticmethod
    def merge(
        first_tree_root: Optional[Node[Key, Value]], second_tree_root: Optional[Node[Key, Value]]
    ) -> Optional[Node[Key, Value]]:
        def recursion_merge(
            curr_node1: Optional[Node[Key, Value]], curr_node2: Optional[Node[Key, Value]]
        ) -> Optional[Node[Key, Value]]:
            if curr_node1 is None:
                return curr_node2
            elif curr_node2 is None:
                return curr_node1
            elif curr_node1.priority > curr_node2.priority:
                curr_node1.right = recursion_merge(curr_node1.right, curr_node2)
                return curr_node1
            elif curr_node1.priority < curr_node2.priority:
                curr_node2.left = recursion_merge(curr_node1, curr_node2.left)
                return curr_node2

        return recursion_merge(first_tree_root, second_tree_root)

    def __str__(self) -> str:
        result = f"Cartesian Tree\nsize = {self.size}\nitems in symmetrical order:\n"
        for key in iter(self):
            result += f"key: {str(key)}, value: {str(self[key])}\n"
        return result

    def __repr__(self) -> str:
        result = ""
        for key in iter(self):
            node = self._find_node(key)
            if node is not None:
                result += f"key: {node.key}, value: {node.value}, priority: {node.priority}\n"
        return result
