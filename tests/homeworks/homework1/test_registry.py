from typing import Mapping, Optional

import pytest

from src.homeworks.homework1 import registry

MAPPING_REGISTRY1 = registry.Registry[Mapping](default=dict)
MAPPING_REGISTRY2 = registry.Registry[Mapping]()


@MAPPING_REGISTRY1.register("bst")
class BST(Mapping):
    def __getitem__(self, item) -> None:
        pass

    def __len__(self) -> None:
        pass

    def __iter__(self) -> None:
        pass


@MAPPING_REGISTRY2.register("avl_tree")
class AVLTree(Mapping):
    def __getitem__(self, item) -> None:
        pass

    def __len__(self) -> None:
        pass

    def __iter__(self) -> None:
        pass


@pytest.mark.parametrize(
    "register,name,expected",
    [
        (MAPPING_REGISTRY1, "bst", BST),
        (MAPPING_REGISTRY2, "avl_tree", AVLTree),
    ],
)
def test_register(register, name, expected) -> None:
    assert name in register._registry_storage
    assert issubclass(register._registry_storage[name], expected)


@pytest.mark.parametrize(
    "register,name,expected",
    [(MAPPING_REGISTRY1, "bst", BST), (MAPPING_REGISTRY1, "test1", dict), (MAPPING_REGISTRY2, "avl_tree", AVLTree)],
)
def test_dispatch(register, name, expected) -> None:
    actual = register.dispatch(name)()
    assert isinstance(actual, expected)


def test_raise_exception_register() -> None:
    with pytest.raises(ValueError):

        @MAPPING_REGISTRY1.register("bst")
        class Test(Mapping):
            def __getitem__(self, item) -> None:
                pass

            def __len__(self) -> Optional[int]:
                pass

            def __iter__(self) -> None:
                pass


def test_raise_exception_dispatch() -> None:
    with pytest.raises(ValueError):
        MAPPING_REGISTRY2.dispatch("test2")
