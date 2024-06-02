import random

import hypothesis.strategies as st
import pytest
from hypothesis import given

from src.homeworks.homework5.model import EasyBot, GameBoard, HardBot, check_win


@pytest.mark.parametrize(
    "board,sign,expected",
    [
        (["X", "X", "X", "O", "O", None, "O", None, None], "X", True),
        (["X", "X", "X", "O", "O", None, "O", None, None], "O", False),
        (["X", None, None, "O", "X", None, "O", "O", "X"], "X", True),
        (["X", None, None, "X", "O", None, "X", "O", "O"], "X", True),
        (["X", "X", "O", "O", "O", "X", "X", "O", "X"], "O", False),
    ],
)
def test_check_win(board, sign, expected):
    actual = check_win(board, sign)
    assert actual == expected


def get_random_board():
    board = []
    for i in range(9):
        board.append(random.choice(["X", "O", None]))
    return board


class TestEasyBot:
    bot = EasyBot("Bot")
    bot.set_sign("X")

    def test_make_move(self):
        for i in range(100):
            board = get_random_board()
            if None in board:
                curr_move = self.bot.make_move(board)
                assert board[curr_move] is None


class TestHardBot:
    x_bot = HardBot("bot")
    o_bot = HardBot("bot")
    x_bot.set_sign("X")
    o_bot.set_sign("O")

    @pytest.mark.parametrize(
        "board",
        [
            ["X", "X", None, "O", "O", None, None, None, None],
            ["X", "O", None, "O", "X", None, "O", "X", None],
            ["O", "X", "X", "O", "O", None, None, None, "X"],
        ],
    )
    def test_make_move_x_bot(self, board):
        curr_move = self.x_bot.make_move(board)
        board[curr_move] = self.x_bot.sign
        assert check_win(board, "X")

    @pytest.mark.parametrize(
        "board",
        [
            ["X", "X", "O", "O", "O", None, None, "X", "X"],
            ["X", "O", "X", None, "O", "X", None, None, None],
            ["O", "X", "X", "X", "O", "O", "X", None, None],
        ],
    )
    def test_make_move_o_bot(self, board):
        curr_move = self.o_bot.make_move(board)
        board[curr_move] = self.o_bot.sign
        assert check_win(board, "O")


class TestGameBoard:
    game_board = GameBoard()

    @given(st.integers(min_value=0, max_value=8))
    def test_restart_board(self, curr_move):
        self.game_board.cells[curr_move].value = "X"
        self.game_board.restart_board()
        assert self.game_board.cells[curr_move].value is None
        assert self.game_board.free_cells == list(range(9))

    @given(st.integers(min_value=0, max_value=8))
    def test_make_move(self, curr_move):
        self.game_board.make_move(curr_move, "X")
        assert self.game_board.cells[curr_move].value == "X"
        assert curr_move not in self.game_board.free_cells
        self.game_board.restart_board()

    @given(st.integers(min_value=0, max_value=8))
    def test_get_board(self, curr_move):
        self.game_board.make_move(curr_move, "X")
        expected = [None] * 9
        expected[curr_move] = "X"
        assert self.game_board.get_board() == expected
        self.game_board.restart_board()
