from random import random
from typing import Any, Generic, Iterable, Iterator, MutableMapping, Optional, Protocol, Type, TypeVar


class Comparable(Protocol):
    def __gt__(self, other: Any) -> bool:
        ...


Key = TypeVar("Key", bound=Comparable)
Value = TypeVar("Value")


class EmptyTreeError(Exception):
    pass


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
    @staticmethod
    def create_comparator(node: Node[Key, Value]) -> Iterable:
        raise NotImplementedError


class PreorderComparator(Comparator):
    @staticmethod
    def create_comparator(node: Node[Key, Value]) -> Iterable:
        return filter(None, (node, node.left, node.right))


class InorderComparator(Comparator):
    @staticmethod
    def create_comparator(node: Node[Key, Value]) -> Iterable:
        return filter(None, (node.left, node, node.right))


class PostorderComparator(Comparator):
    @staticmethod
    def create_comparator(node: Node[Key, Value]) -> Iterable:
        return filter(None, (node.left, node.right, node))


class CartesianTree(MutableMapping, Generic[Key, Value]):
    def __init__(self) -> None:
        self.root: Optional[Node[Key, Value]] = None
        self.size: int = 0

    def __setitem__(self, key: Key, value: Value) -> None:
        if self.root is None:
            self.root = Node(key, value)
            self.size = 1
            return
        node = self._find_node(key)
        if node is not None:
            node.value = value
            return
        smaller_root, bigger_root = self.split(self.root, key)
        smaller_root = self.merge(smaller_root, Node(key, value))
        self.root = self.merge(smaller_root, bigger_root)
        self.size += 1

    def __getitem__(self, key: Key) -> Value:
        node = self._find_node(key)
        if node is not None:
            return node.value
        raise KeyError("There is no such key")

    def traverse(self, order: str = "inorder") -> list[tuple[Key, Value]]:
        items: list[tuple[Key, Value]] = []
        if self.root is None:
            return items

        def traverse_recursion(curr_node: Node[Key, Value], order_func: Type[Comparator]) -> None:
            node_order = order_func.create_comparator(curr_node)
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
        raise EmptyTreeError("Tree is empty")

    def __delitem__(self, key: Key) -> None:
        def del_recursion(curr_node: Optional[Node[Key, Value]]) -> Optional[Node[Key, Value]]:
            if curr_node is None:
                raise KeyError("There is no such key")
            elif curr_node.key < key:
                curr_node.right = del_recursion(curr_node.right)
            elif curr_node.key > key:
                curr_node.left = del_recursion(curr_node.left)
            else:
                return self.merge(curr_node.left, curr_node.right)
            return curr_node

        self.root = del_recursion(self.root)
        self.size -= 1

    def pop(self, key: Key, default: Any = None) -> Value:
        try:
            value = self[key]
            del self[key]
            return value
        except KeyError:
            if default is not None:
                return default
            raise KeyError("There is no such key")

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
        curr_node: Optional[Node[Key, Value]], key: Key
    ) -> tuple[Optional[Node[Key, Value]], Optional[Node[Key, Value]]]:
        if curr_node is None:
            return None, None
        elif curr_node.key < key:
            left_node, right_node = CartesianTree.split(curr_node.right, key)
            curr_node.right = left_node
            return curr_node, right_node
        else:
            left_node, right_node = CartesianTree.split(curr_node.left, key)
            curr_node.left = right_node
            return left_node, curr_node

    @staticmethod
    def merge(
        left_node: Optional[Node[Key, Value]], right_node: Optional[Node[Key, Value]]
    ) -> Optional[Node[Key, Value]]:
        if left_node is None:
            return right_node
        elif right_node is None:
            return left_node
        elif left_node.priority > right_node.priority:
            left_node.right = CartesianTree.merge(left_node.right, right_node)
            return left_node
        elif left_node.priority < right_node.priority:
            right_node.left = CartesianTree.merge(left_node, right_node.left)
            return right_node

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
