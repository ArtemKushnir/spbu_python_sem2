import abc
import random
from dataclasses import dataclass
from typing import Any, Callable, Optional

from src.homeworks.homework5.observer import Observable


class TicTacToeError(Exception):
    pass


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.sign = ""

    def set_sign(self, sign: str) -> None:
        self.sign = sign


class Bot(Player, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def make_move(self, board: list[Optional[str]]) -> int:
        raise NotImplementedError


class EasyBot(Bot):
    def make_move(self, board: list[Optional[str]]) -> int:
        free_cells = [i for i in range(9) if board[i] is None]
        return random.choice(free_cells)


class HardBot(Bot):
    def make_move(self, board: list[Optional[str]]) -> int:
        best_score = float("-inf")
        best_move = None
        free_cells = [i for i in range(9) if board[i] is None]
        for i in free_cells:
            board[i] = self.sign
            score = self.minimax(board, False)
            board[i] = None
            if score > best_score:
                best_score = score
                best_move = i
        if best_move is not None:
            return best_move
        raise TicTacToeError("Bot malfunction")

    def minimax(self, curr_board: list[Optional[str]], is_bot: bool) -> int | float:
        if check_win(curr_board, self.sign):
            return 1
        if check_win(curr_board, "X" if self.sign == "O" else "O"):
            return -1
        if all(cell is not None for cell in curr_board):
            return 0
        free_cells = [i for i in range(9) if curr_board[i] is None]
        if is_bot:
            best_score = float("-inf")
            for i in free_cells:
                curr_board[i] = self.sign
                best_score = max(best_score, self.minimax(curr_board, False))
                curr_board[i] = None
            return best_score

        worse_score = float("inf")
        for i in free_cells:
            curr_board[i] = "X" if self.sign == "O" else "O"
            worse_score = min(worse_score, self.minimax(curr_board, True))
            curr_board[i] = None
        return worse_score


@dataclass
class Session:
    name: str
    data: Any


class GameBoard:
    def __init__(self) -> None:
        self.cells: list[Observable] = [Observable() for _ in range(9)]
        self.free_cells = list(range(9))

    def get_board(self) -> list[Optional[str]]:
        return [cell.value for cell in self.cells]

    def make_move(self, coord: int, sign: str) -> None:
        self.cells[coord].value = sign
        self.free_cells.remove(coord)

    def restart_board(self) -> None:
        for cell in self.cells:
            del cell.value
        self.free_cells = list(range(9))


def check_win(board: list[Optional[str]], sign: str) -> bool:
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] == sign:
            return True
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] == sign:
            return True
    if board[0] == board[4] == board[8] == sign:
        return True
    if board[2] == board[4] == board[6] == sign:
        return True
    return False


class GameModel:
    def __init__(self) -> None:
        self.board: GameBoard = GameBoard()
        self.first_player: Optional[Player] = None
        self.second_player: Optional[Player] = None
        self.current_player: Optional[Player] = None
        self.current_session: Observable = Observable()

    def make_bot_move(self) -> None:
        if isinstance(self.current_player, EasyBot):
            self.make_move(self.current_player.make_move(self.board.get_board()))
        if isinstance(self.current_player, HardBot):
            self.make_move(self.current_player.make_move(self.board.get_board()))

    def make_move(self, coord: int) -> None:
        if coord in self.board.free_cells and self.current_player is not None:
            self.board.make_move(coord, self.current_player.sign)
            if check_win(self.board.get_board(), self.current_player.sign):
                self.current_session.value = Session("game_result", self.current_player.name)
                return
            if len(self.board.free_cells) == 0:
                self.current_session.value = Session("game_result", None)
                return
            if self.current_player == self.first_player:
                self.current_player = self.second_player
            else:
                self.current_player = self.first_player
            self.make_bot_move()

    def choose_side(self, type_game: str) -> None:
        if type_game == "easy":
            players: tuple[Player, Player] = (Player("Player1"), EasyBot("Easy bot"))
        elif type_game == "hard":
            players = (Player("Player1"), HardBot("Hard bot"))
        else:
            players = (Player("Player1"), Player("Player2"))
        self.current_session.value = Session("choose_side", players)

    def start_game(self, player1: Player, player2: Player) -> None:
        self.first_player = player1
        self.second_player = player2
        self.current_player = player1
        self.current_session.value = Session("game_field", (player1, player2))
        self.make_bot_move()

    def restart_game(self) -> None:
        self.board.restart_board()
        self.current_session.value = Session("main", None)

    def add_session_listener(self, callback: Callable) -> Callable:
        return self.current_session.add_callback(callback)
