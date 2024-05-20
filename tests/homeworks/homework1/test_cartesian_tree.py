from random import choices, randint

import pytest

from src.homeworks.homework1 import cartesian_tree


class TestCartesianTree:
    @staticmethod
    def create_treap(size, a=-1000, b=1000):
        new_tree = cartesian_tree.CartesianTree()
        items = {}
        for i in range(size):
            random_key = randint(a, b)
            random_value = randint(a, b)
            items[random_key] = random_value
            new_tree[random_key] = random_value
        return new_tree, items

    @staticmethod
    def check_tree(tree) -> bool:
        if tree.root is None:
            return True

        def check_recursion(curr_node):
            if curr_node.left is not None and curr_node.right is not None:
                if (
                    curr_node.left.key >= curr_node.key
                    or curr_node.right.key <= curr_node.key
                    or curr_node.left.priority <= curr_node.priority
                    or curr_node.right.priority <= curr_node.priority
                ):
                    return False
                check_recursion(curr_node.right)
                check_recursion(curr_node.left)
            elif curr_node.left is not None:
                if curr_node.left.key >= curr_node.key or curr_node.left.priority <= curr_node.priority:
                    return False
                check_recursion(curr_node.left)
            elif curr_node.right is not None:
                if curr_node.right.key <= curr_node.key or curr_node.right.priority <= curr_node.priority:
                    return False
                check_recursion(curr_node.right)

        check_recursion(tree.root)
        return True

    @pytest.mark.parametrize(
        "items",
        [
            ((1001, 1001), (2000, 2000), (4500, 4500), (1, 1), (300, 300)),
            (("a", 5), ("qwerty", 9), ("aaa", 100), ("l", 0), ("python", 900)),
        ],
    )
    def test_setitem(self, items):
        new_tree = cartesian_tree.CartesianTree()
        for key, value in items:
            new_tree[key] = value
        for key, value in items:
            assert new_tree.__contains__(key) and new_tree[key] == value

    @pytest.mark.parametrize("cnt", [10, 50, 100, 1000, 10000])
    def test_create_tree(self, cnt):
        new_tree, items = self.create_treap(cnt)
        assert self.check_tree(new_tree) and new_tree.size == len(items)

    def test_getitem(self):
        cnt = 100
        new_tree, items = self.create_treap(cnt)
        for key in items.keys():
            assert new_tree[key] == items[key]

    @pytest.mark.parametrize("cnt", [10, 50, 100, 1000, 1500, 2000, 5678, 10934])
    def test_len(self, cnt):
        new_tree, items = self.create_treap(cnt)
        assert new_tree.size == len(items)

    def test_contains(self):
        cnt = 100
        new_tree, items = self.create_treap(cnt)
        for key in items.keys():
            assert new_tree.__contains__(key)
        for i in range(cnt):
            assert not new_tree.__contains__(randint(1500, 10000))

    @pytest.mark.parametrize("cnt", [10, 50, 100, 1000])
    def test_delitem(self, cnt):
        new_tree, items = self.create_treap(cnt)
        del_keys = set(choices(list(items.keys()), k=randint(1, cnt)))
        for key in del_keys:
            del new_tree[key]

        for key, value in items.items():
            if key not in del_keys:
                assert new_tree[key] == value
            else:
                assert not new_tree.__contains__(key)

    @pytest.mark.parametrize("cnt", [10, 50, 100, 1000])
    def test_pop(self, cnt):
        new_tree, items = self.create_treap(cnt)
        del_keys = set(choices(list(items.keys()), k=randint(1, cnt)))
        for key in del_keys:
            assert new_tree.pop(key) == items[key]

        for key, value in items.items():
            if key not in del_keys:
                assert new_tree[key] == value
            else:
                assert not new_tree.__contains__(key)

    @pytest.mark.parametrize("cnt", [10, 50, 100, 1000])
    def test_iter(self, cnt):
        new_tree, items = self.create_treap(cnt)
        for key in iter(new_tree):
            assert new_tree[key] == items[key]
        assert len(list(iter(new_tree))) == len(items)

    @pytest.mark.parametrize("cnt", [10, 50, 100, 1000])
    def test_traverse(self, cnt):
        new_tree, items = self.create_treap(cnt)
        for key, value in new_tree.traverse():
            assert items.get(key, None) == value

    @pytest.mark.parametrize("cnt", [10, 50, 100, 1000])
    def test_find_node(self, cnt):
        new_tree, items = self.create_treap(cnt)
        for key, value in items.items():
            node = new_tree._find_node(key)
            assert node.key == key and node.value == value
        for i in range(cnt):
            assert new_tree._find_node(randint(1001, 10000)) is None

    @pytest.mark.parametrize("cnt", [10, 50, 100, 1000])
    def test_split(self, cnt):
        new_tree, items = self.create_treap(cnt)
        tree1, tree2 = cartesian_tree.CartesianTree(), cartesian_tree.CartesianTree()
        split_key = randint(-1000, 1000)
        tree1.root, tree2.root = cartesian_tree.CartesianTree.split(new_tree.root, split_key)
        for key, value in items.items():
            if key < split_key:
                assert tree1[key] == items[key]
            else:
                assert tree2[key] == items[key]

        assert self.check_tree(tree1) and self.check_tree(tree2)

    @pytest.mark.parametrize("cnt1,cnt2", [(10, 20), (100, 50), (1000, 2000)])
    def test_merge(self, cnt1, cnt2):
        tree1, items1 = self.create_treap(cnt1)
        tree2, items2 = self.create_treap(cnt2, 2000, 3000)
        new_tree = cartesian_tree.CartesianTree()
        new_tree.root = cartesian_tree.CartesianTree.merge(tree1.root, tree2.root)
        for key, value in (items1 | items2).items():
            assert new_tree[key] == value
        assert self.check_tree(new_tree)

    @pytest.mark.parametrize(
        "key,value,expected",
        [
            (5, 20, "Cartesian Tree\nsize = 1\nitems in symmetrical order:\nkey: 5, value: 20\n"),
            ("first", 1000, "Cartesian Tree\nsize = 1\nitems in symmetrical order:\nkey: first, value: 1000\n"),
            ("a", "b", "Cartesian Tree\nsize = 1\nitems in symmetrical order:\nkey: a, value: b\n"),
        ],
    )
    def test_str(self, key, value, expected):
        new_tree = cartesian_tree.CartesianTree()
        new_tree[key] = value
        assert str(new_tree) == expected

    def test_exception_raises_getitem(self):
        cnt = 100
        new_tree = self.create_treap(cnt)[0]
        for i in range(cnt):
            with pytest.raises(KeyError):
                return new_tree[randint(1001, 100000)]

    def test_exception_raises_delitem(self):
        cnt = 100
        new_tree = self.create_treap(cnt)[0]
        for i in range(cnt):
            with pytest.raises(KeyError):
                del new_tree[randint(1001, 100000)]

    def test_exception_raises_pop(self):
        cnt = 100
        new_tree = self.create_treap(cnt)[0]
        for i in range(cnt):
            with pytest.raises(KeyError):
                new_tree.pop(randint(1001, 100000))
