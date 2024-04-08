from typing import Mapping

import pytest

from src.homeworks.homework1 import registry


class BST(Mapping):
    pass


class AVLTree(Mapping):
    pass


class Treap(Mapping):
    pass


class TestRegistryWithDefault:
    MAPPING_REGISTRY1 = registry.Registry[Mapping](default=dict)
    MAPPING_REGISTRY1.register("bst")(BST)
    MAPPING_REGISTRY1.register("avl_tree")(AVLTree)
    MAPPING_REGISTRY1.register("treap")(Treap)

    @pytest.mark.parametrize(
        "name,expected",
        [("bst", BST), ("avl_tree", AVLTree), ("treap", Treap)],
    )
    def test_register(self, name, expected):
        assert name in self.MAPPING_REGISTRY1._registry_storage
        assert issubclass(self.MAPPING_REGISTRY1._registry_storage[name], expected)

    @pytest.mark.parametrize(
        "name,expected",
        [("bst", BST), ("avl_tree", AVLTree), ("treap", Treap)],
    )
    def test_dispatch(self, name, expected):
        actual = self.MAPPING_REGISTRY1.dispatch(name)
        assert issubclass(actual, expected)

    @pytest.mark.parametrize("name,expected", [("test1", dict), ("qwerty", dict), ("python", dict)])
    def test_dispatch_return_default(self, name, expected):
        actual = self.MAPPING_REGISTRY1.dispatch(name)
        assert issubclass(actual, expected)

    def test_raise_exception_register(self):
        with pytest.raises(ValueError):
            self.MAPPING_REGISTRY1.register("bst")(AVLTree)


class TestRegistry:
    MAPPING_REGISTRY2 = registry.Registry[Mapping]()
    MAPPING_REGISTRY2.register("bst")(BST)
    MAPPING_REGISTRY2.register("avl")(AVLTree)
    MAPPING_REGISTRY2.register("cartesian_tree")(Treap)

    @pytest.mark.parametrize(
        "name,expected",
        [("bst", BST), ("avl", AVLTree), ("cartesian_tree", Treap)],
    )
    def test_register(self, name, expected):
        assert name in self.MAPPING_REGISTRY2._registry_storage
        assert issubclass(self.MAPPING_REGISTRY2._registry_storage[name], expected)

    @pytest.mark.parametrize(
        "name,expected",
        [("bst", BST), ("cartesian_tree", Treap), ("avl", AVLTree)],
    )
    def test_dispatch(self, name, expected):
        actual = self.MAPPING_REGISTRY2.dispatch(name)
        assert issubclass(actual, expected)

    def test_raise_exception_dispatch(self):
        with pytest.raises(ValueError):
            self.MAPPING_REGISTRY2.dispatch("test2")

    def test_raise_exception_register(self):
        with pytest.raises(ValueError):
            self.MAPPING_REGISTRY2.register("avl")(BST)
