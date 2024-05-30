from random import randint

import hypothesis.strategies as st
import pytest
from hypothesis import given

from src.homeworks.homework2.main import *

INFO = create_info()


class TestInsertLeft:
    action = InsertLeft

    @pytest.mark.parametrize(
        "collection,new_value,expected", [([], 99, [99]), ([1, 2, 3], 1, [1, 1, 2, 3]), ([5], 1000, [1000, 5])]
    )
    def test_do(self, collection, new_value, expected):
        action = self.action(new_value)
        action.do_action(collection)
        assert collection == expected

    @given(collection=st.lists(st.integers(), min_size=0, max_size=1000))
    def test_undo(self, collection):
        initial_state = collection.copy()
        action = self.action(randint(-1000, 1000))
        action.do_action(collection)
        action.undo_action(collection)
        assert collection == initial_state

    def test_raise_exception_collection_error_do(self):
        with pytest.raises(CollectionError):
            self.action(0).do_action({})

    def test_raise_exception_collection_error_undo(self):
        with pytest.raises(CollectionError):
            self.action(0).do_action({})


class TestInsertRight:
    action = InsertRight

    @pytest.mark.parametrize(
        "collection,new_value,expected", [([], 99, [99]), ([1, 2, 3], 1, [1, 2, 3, 1]), ([5], 1000, [5, 1000])]
    )
    def test_do(self, collection, new_value, expected):
        action = self.action(new_value)
        action.do_action(collection)
        assert collection == expected

    @given(collection=st.lists(st.integers(), min_size=0, max_size=1000))
    def test_undo(self, collection):
        initial_state = collection.copy()
        action = self.action(randint(-1000, 1000))
        action.do_action(collection)
        action.undo_action(collection)
        assert collection == initial_state

    def test_raise_exception_collection_error_do(self):
        with pytest.raises(CollectionError):
            self.action(0).do_action({})

    def test_raise_exception_collection_error_undo(self):
        with pytest.raises(CollectionError):
            self.action(0).do_action({})


class TestMoveElement:
    action = MoveElement

    @pytest.mark.parametrize(
        "collection,i,j,expected",
        [([11, 1], 0, 1, [1, 11]), ([11, 1], 1, 0, [1, 11]), ([1, 2, 3, 4, 5, 6], 1, 5, [1, 3, 4, 5, 6, 2])],
    )
    def test_do(self, collection, i, j, expected):
        action = self.action(i, j)
        action.do_action(collection)
        assert collection == expected

    @given(collection=st.lists(st.integers(), min_size=1, max_size=1000))
    def test_undo(self, collection):
        initial_state = collection.copy()
        i, j = randint(0, len(collection) - 1), randint(0, len(collection) - 1)
        action = self.action(i, j)
        action.do_action(collection)
        action.undo_action(collection)
        assert collection == initial_state

    def test_raise_exception_collection_error_do(self):
        with pytest.raises(CollectionError):
            self.action(0, 0).do_action({})

    def test_raise_exception_collection_error_undo(self):
        with pytest.raises(CollectionError):
            self.action(0, 0).do_action({})


class TestAddValue:
    action = AddValue

    @pytest.mark.parametrize(
        "collection,i,value,expected",
        [([11, 1], 0, 1, [12, 1]), ([999], 0, -999, [0]), ([1, 2, 3, 4, 5, 6], 3, 500, [1, 2, 3, 504, 5, 6])],
    )
    def test_do(self, collection, i, value, expected):
        action = self.action(i, value)
        action.do_action(collection)
        assert collection == expected

    @given(collection=st.lists(st.integers(), min_size=1, max_size=1000))
    def test_undo(self, collection):
        initial_state = collection.copy()
        i, value = randint(0, len(collection) - 1), randint(-1000, 1000)
        action = self.action(i, value)
        action.do_action(collection)
        action.undo_action(collection)
        assert collection == initial_state

    def test_raise_exception_collection_error_do(self):
        with pytest.raises(CollectionError):
            self.action(0, 0).do_action({})

    def test_raise_exception_collection_error_undo(self):
        with pytest.raises(CollectionError):
            self.action(0, 0).do_action({})


class TestReverse:
    action = Reverse

    @pytest.mark.parametrize(
        "collection,expected", [([11, 1], [1, 11]), ([999], [999]), ([1, 2, 3, 4, 6, 5], [5, 6, 4, 3, 2, 1])]
    )
    def test_do(self, collection, expected):
        action = self.action()
        action.do_action(collection)
        assert collection == expected

    @given(collection=st.lists(st.integers(), min_size=0, max_size=1000))
    def test_undo(self, collection):
        initial_state = collection.copy()
        action = self.action()
        action.do_action(collection)
        action.undo_action(collection)
        assert collection == initial_state

    def test_raise_exception_collection_error_do(self):
        with pytest.raises(CollectionError):
            self.action().do_action({})

    def test_raise_exception_collection_error_undo(self):
        with pytest.raises(CollectionError):
            self.action().do_action({})


class TestSwap:
    action = Swap

    @pytest.mark.parametrize(
        "collection,i,j,expected",
        [([11, 1], 0, 1, [1, 11]), ([11, 1], 1, 0, [1, 11]), ([1, 2, 3, 4, 5, 6], 3, 0, [4, 2, 3, 1, 5, 6])],
    )
    def test_do(self, collection, i, j, expected):
        action = self.action(i, j)
        action.do_action(collection)
        assert collection == expected

    @given(collection=st.lists(st.integers(), min_size=1, max_size=1000))
    def test_undo(self, collection):
        initial_state = collection.copy()
        i, j = randint(0, len(collection) - 1), randint(0, len(collection) - 1)
        action = self.action(i, j)
        action.do_action(collection)
        action.undo_action(collection)
        assert collection == initial_state

    def test_raise_exception_collection_error_do(self):
        with pytest.raises(CollectionError):
            self.action(0, 0).do_action({})

    def test_raise_exception_collection_error_undo(self):
        with pytest.raises(CollectionError):
            self.action(0, 0).do_action({})


class TestPop:
    action = Pop

    @pytest.mark.parametrize(
        "collection,index,expected", [([99], 0, []), ([1, 2, 3], 1, [1, 3]), ([5, 5, 5, 5], 3, [5, 5, 5])]
    )
    def test_do(self, collection, index, expected):
        action = self.action(index)
        action.do_action(collection)
        assert collection == expected

    @given(collection=st.lists(st.integers(), min_size=1, max_size=1000))
    def test_undo(self, collection):
        initial_state = collection.copy()
        action = self.action(randint(0, len(collection) - 1))
        action.do_action(collection)
        action.undo_action(collection)
        assert collection == initial_state

    def test_raise_exception_collection_error_do(self):
        with pytest.raises(CollectionError):
            self.action(0).do_action({})

    def test_raise_exception_collection_error_undo(self):
        with pytest.raises(CollectionError):
            self.action(0).do_action({})


class TestClear:
    action = Clear

    @pytest.mark.parametrize("collection", [[], [1, 2, 3], [5], [1000, 5]])
    def test_do(self, collection):
        action = self.action()
        action.do_action(collection)
        expected = []
        assert collection == expected

    @given(collection=st.lists(st.integers(), min_size=0, max_size=1000))
    def test_undo(self, collection):
        initial_state = collection.copy()
        action = self.action()
        action.do_action(collection)
        action.undo_action(collection)
        assert collection == initial_state

    def test_raise_exception_collection_error_do(self):
        with pytest.raises(CollectionError):
            self.action().do_action({})

    def test_raise_exception_collection_error_undo(self):
        with pytest.raises(CollectionError):
            self.action().do_action({})


class TestPerformedCommandStorage:
    @pytest.mark.parametrize(
        "collection,action,expected",
        [
            ([1, 2, 3], AddValue(1, 100), [1, 102, 3]),
            ([], InsertRight(10), [10]),
            ([1, 2, 3], Reverse(), [3, 2, 1]),
        ],
    )
    def test_apply(self, collection, action, expected):
        storage = PerformedCommandStorage(collection)
        storage.apply(action)
        assert storage.numbers == expected
        assert storage.actions[-1] == action

    @pytest.mark.parametrize(
        "collection,action",
        [([1, 2, 3], AddValue(1, 100)), ([], InsertRight(10)), ([1, 2, 3], Reverse())],
    )
    def test_cancel(self, collection, action):
        initial_state = collection.copy()
        storage = PerformedCommandStorage(collection)
        storage.apply(action)
        storage.cancel()
        assert storage.numbers == initial_state
        assert action not in storage.actions

    def test_raise_exception_action_index_error(self):
        with pytest.raises(ActionIndexError):
            PerformedCommandStorage([]).cancel()


class TestMultiplyValue:
    action = MultiplyValue

    @pytest.mark.parametrize(
        "collection,i,value,expected",
        [([11, 1], 0, 1, [11, 1]), ([999], 0, -999, [-999 * 999]), ([1, 2, 3, 4, 5, 6], 3, 500, [1, 2, 3, 2000, 5, 6])],
    )
    def test_do(self, collection, i, value, expected):
        action = self.action(i, value)
        action.do_action(collection)
        assert collection == expected

    @given(collection=st.lists(st.integers(), min_size=1, max_size=1000))
    def test_undo(self, collection):
        initial_state = collection.copy()
        i, value = randint(0, len(collection) - 1), randint(-1000, 1000)
        action = self.action(i, value)
        action.do_action(collection)
        action.undo_action(collection)
        assert collection == initial_state

    def test_raise_exception_collection_error(self):
        with pytest.raises(CollectionError):
            self.action(0, 0).do_action({})


class TestDeleteLeft:
    action = DeleteLeft

    @pytest.mark.parametrize("collection,expected", [([99], []), ([1, 2, 3], [2, 3]), ([5, 5, 5, 5], [5, 5, 5])])
    def test_do(self, collection, expected):
        action = self.action()
        action.do_action(collection)
        assert collection == expected

    @given(collection=st.lists(st.integers(), min_size=1, max_size=1000))
    def test_undo(self, collection):
        initial_state = collection.copy()
        action = self.action()
        action.do_action(collection)
        action.undo_action(collection)
        assert collection == initial_state

    def test_raise_exception_collection_error(self):
        with pytest.raises(CollectionError):
            self.action().do_action({})

    def test_raise_exception_action_error(self):
        with pytest.raises(ActionError):
            self.action()._do_action([])


class TestDeleteRight:
    action = DeleteRight

    @pytest.mark.parametrize("collection,expected", [([99], []), ([1, 2, 3], [1, 2]), ([5, 5, 5, 5], [5, 5, 5])])
    def test_do(self, collection, expected):
        action = self.action()
        action.do_action(collection)
        assert collection == expected

    @given(collection=st.lists(st.integers(), min_size=1, max_size=1000))
    def test_undo(self, collection):
        initial_state = collection.copy()
        action = self.action()
        action.do_action(collection)
        action.undo_action(collection)
        assert collection == initial_state

    def test_raise_exception_collection_error(self):
        with pytest.raises(CollectionError):
            self.action().do_action({})

    def test_raise_exception_action_error(self):
        with pytest.raises(ActionError):
            self.action()._do_action([])


@pytest.mark.parametrize(
    "actions,expected",
    [
        (
            ["[1, 2, 3]", "insert_left --22", "insert_right --11", "exit"],
            "Write your collection\n" + INFO + "\nResult: [22, 1, 2, 3]\nResult: [22, 1, 2, 3, 11]\n",
        ),
        (
            ["[]", "insert_left --0", "insert_left --100", "add_value --1 --99", "cancel", "swap --0 --1", "exit"],
            "Write your collection\n"
            + INFO
            + "\nResult: [0]\nResult: [100, 0]\nResult: [100, 99]\nResult: [100, 0]\nResult: [0, 100]\n",
        ),
        (
            ["[0, 0, 0]", "insert_right --1", "reverse", "exit"],
            "Write your collection\n" + INFO + "\nResult: [0, 0, 0, 1]\nResult: [1, 0, 0, 0]\n",
        ),
    ],
)
def test_main_scenario(actions, expected, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: actions.pop(0))
    main()
    captured = capsys.readouterr().out
    assert captured == expected


@pytest.mark.parametrize(
    "actions,expected",
    [
        (["[1, 2, 3]", "pop --99", "exit"], "Indexes are incorrectly specified"),
        (["[]", "pip --0", "exit"], "Invalid request"),
        (["[]", "insert_left --0 --1", "exit"], "The request has an incorrect number of arguments"),
        (["set()", "insert_left --0", "exit"], "This collection does not support this action"),
        (["[]", "cancel", "exit"], "No action was performed"),
    ],
)
def test_main_scenario_error(actions, expected, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: actions.pop(0))
    main()
    captured = capsys.readouterr().out.split("\n")
    assert captured[-2] == expected
