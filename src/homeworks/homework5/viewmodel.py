import abc
import socket
from threading import Thread
from tkinter import Tk
from typing import Optional

from src.homeworks.homework5.model import GameModel, MultiPlayer, Player, Session
from src.homeworks.homework5.view import *


class IViewModel(metaclass=abc.ABCMeta):
    def __init__(self, model: GameModel) -> None:
        self._model = model

    @abc.abstractmethod
    def start(self, root: Tk, data: Any) -> ttk.Frame:
        raise NotImplementedError


class ViewModel:
    def __init__(self, model: GameModel, root: Tk) -> None:
        self._model = model
        self._root = root

        self._viewmodels: dict[str, IViewModel] = {
            "main": MainViewModel(self._model),
            "choose_side": ChooseSideViewModel(self._model),
            "game_field": PlayingFieldViewModel(self._model),
            "game_result": ResultGameViewModel(self._model),
        }

        self._session_callback_rm = model.add_session_listener(self._session_observer)
        self._current_view: Optional[ttk.Frame] = None

    def _session_observer(self, session: Session) -> None:
        if session.name == "choose_side":
            self.switch("choose_side", session.data)
        if session.name == "game_field":
            self.switch("game_field", session.data)
        if session.name == "game_result":
            self.switch("game_result", session.data)
        if session.name == "main":
            self.switch("main", session.data)

    def switch(self, name: str, data: Any) -> None:
        if name not in self._viewmodels:
            raise RuntimeError(f"Unknown view to switch: {name}")
        if self._current_view is not None:
            self._current_view.destroy()
        self._current_view = self._viewmodels[name].start(self._root, data)
        self._current_view.grid(row=0, column=0)

    def start(self) -> None:
        self.switch("main", None)


class MainViewModel(IViewModel):
    def _bind(self, view: MainView) -> None:
        view.hard_bot_button.config(command=lambda: self._model.choose_side("hard"))
        view.easy_bot_button.config(command=lambda: self._model.choose_side("easy"))
        view.one_pc_button.config(command=lambda: self._model.choose_side("on one pc"))
        view.multiplayer_button.config(command=lambda: self._model.choose_side("multiplayer"))

    def start(self, root: Tk, data: Any) -> ttk.Frame:
        frame = MainView(root)
        self._bind(frame)
        return frame


class PlayingFieldViewModel(IViewModel):
    def _bind(self, view: PlayingFieldView, player1: Player, player2: Player) -> None:
        view.set_greetings(player1.name, player1.sign, player2.name, player2.sign)
        if isinstance(player1, MultiPlayer) and isinstance(player2, MultiPlayer):
            self._bind_multiplayer(view)
            return

        buttons = view.buttons_list
        game_board = self._model.board
        for i in range(9):
            button = buttons[i]
            game_board.cells[i].add_callback(lambda sign, curr_button=button: curr_button.config(text=sign))
            com = lambda coord=i: self._model.make_move(coord)
            button.config(command=com)

    def _bind_multiplayer(self, view: PlayingFieldView) -> None:
        def send_message(client_socket: socket.socket, coord: int) -> None:
            client_socket.sendall(bytes(f"{coord} {client_socket.getsockname()[-1]}", encoding="UTF-8"))

        def get_data(client_sock: socket.socket) -> None:
            while True:
                if not self._model.active:
                    break
                data = client_sock.recv(1024)
                if data:
                    num_cell = int(data.decode())
                    self._model.make_move(num_cell)
            client_sock.close()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("localhost", 8888))

        player_thread = Thread(target=get_data, args=(sock,))
        player_thread.start()

        buttons = view.buttons_list
        game_board = self._model.board
        for i in range(9):
            button = buttons[i]
            game_board.cells[i].add_callback(lambda sign, curr_button=button: curr_button.config(text=sign))
            com = lambda coord=i: send_message(sock, coord)
            button.config(command=com)

    def start(self, root: Tk, data: Any) -> ttk.Frame:
        frame = PlayingFieldView(root)
        self._bind(frame, *data)
        return frame


class ChooseSideViewModel(IViewModel):
    def _bind(self, view: ChooseSideView, player1: Player, player2: Player) -> None:
        view.x_button.config(command=lambda: self.start_game(player1, player2))
        view.o_button.config(command=lambda: self.start_game(player2, player1))

    def start_game(self, player1: Player, player2: Player) -> None:
        player1.set_sign("X")
        player2.set_sign("O")
        self._model.start_game(player1, player2)

    def start(self, root: Tk, data: Any) -> ttk.Frame:
        frame = ChooseSideView(root)
        self._bind(frame, *data)
        return frame


class ResultGameViewModel(IViewModel):
    def _bind(self, view: ResultGameView, data: Any) -> None:
        view.set_greetings(data)
        view.back_button.config(command=lambda: self._model.restart_game())

    def start(self, root: Tk, data: Any) -> ttk.Frame:
        frame = ResultGameView(root)
        self._bind(frame, data)
        return frame
