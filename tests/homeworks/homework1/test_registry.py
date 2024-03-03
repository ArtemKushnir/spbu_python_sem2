import pytest
from src.homeworks.homework1 import registry
from typing import Mapping


MAPPING_REGISTRY1 = registry.Registry[Mapping](default=dict)
MAPPING_REGISTRY2 = registry.Registry[Mapping]()


@MAPPING_REGISTRY1.register("bst")
class BST(Mapping):
    def __getitem__(self, item):
        pass

    def __len__(self):
        pass

    def __iter__(self):
        pass


@MAPPING_REGISTRY2.register("avl_tree")
class AVLTree(Mapping):
    def __getitem__(self, item):
        pass

    def __len__(self):
        pass

    def __iter__(self):
        pass


class Cartesian_tree(Mapping):
    def __getitem__(self, item):
        pass

    def __len__(self):
        pass

    def __iter__(self):
        pass


@pytest.mark.parametrize("register,name,expected", [
    (MAPPING_REGISTRY1, "bst", BST),
    (MAPPING_REGISTRY2, "avl_tree", AVLTree),
])
def test_register(register, name, expected):
    assert name in register._registry_storage
    assert issubclass(register._registry_storage[name], expected)


@pytest.mark.parametrize("register,name,expected", [
    (MAPPING_REGISTRY1, "bst", BST),
    (MAPPING_REGISTRY1, "test1", dict),
    (MAPPING_REGISTRY2, "avl_tree", AVLTree)
])
def test_dispatch(register, name, expected):
    actual = register.dispatch(name)()
    assert isinstance(actual, expected)


def test_raise_exception_register():
    with pytest.raises(ValueError):
        @MAPPING_REGISTRY1.register("bst")
        class Test(Mapping):
            def __getitem__(self, item):
                pass

            def __len__(self):
                pass

            def __iter__(self):
                pass


def test_raise_exception_dispatch():
    with pytest.raises(ValueError):
        MAPPING_REGISTRY2.dispatch("test2")
