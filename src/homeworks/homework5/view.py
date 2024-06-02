from tkinter import DISABLED, Button, ttk
from typing import Any


class MainView(ttk.Frame):
    HARD_BOT = "Play with hard bot"
    EASY_BOT = "Play with easy bot"
    ONE_PC = "Play on one pc"
    MULTIPLAYER = "Play multiplayer"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.hard_bot_button = Button(self, text=self.HARD_BOT, width=15, height=3)
        self.easy_bot_button = Button(self, text=self.EASY_BOT, height=3)
        self.one_pc_button = Button(self, text=self.ONE_PC, height=3)
        self.multiplayer_button = Button(self, text=self.MULTIPLAYER, height=3)

        self.hard_bot_button.grid(row=0, column=1, sticky="NSEW")
        self.easy_bot_button.grid(row=1, column=1, sticky="NSEW")
        self.one_pc_button.grid(row=2, column=1, sticky="NSEW")
        self.multiplayer_button.grid(row=3, column=1, sticky="NSEW")


class PlayingFieldView(ttk.Frame):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.player1_button = Button(self, width=10, state=DISABLED)
        self.player1_button.grid(row=1, column=1)
        self.player2_button = Button(self, width=10, state=DISABLED)
        self.player2_button.grid(row=2, column=1)
        self.buttons_list = []
        for i in range(9):
            button = Button(self, bd=5, height=5, width=10)
            button.grid(row=3 + i // 3, column=i % 3)
            self.buttons_list.append(button)

    def set_greetings(self, player1_name: str, player1_sign: str, player2_name: str, player2_sign: str) -> None:
        self.player1_button.config(text=f"{player1_name}: {player1_sign}")
        self.player2_button.config(text=f"{player2_name}: {player2_sign}")


class ChooseSideView(ttk.Frame):
    SIDE = "Choose side"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.choose_side = ttk.Label(self, text=self.SIDE)
        self.choose_side.grid(row=0, column=1)

        self.x_button = Button(self, text="X")
        self.x_button.grid(row=1, column=0)

        self.o_button = Button(self, text="O")
        self.o_button.grid(row=1, column=2)


class ResultGameView(ttk.Frame):
    WINNER = "{} win the game!"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.winner = ttk.Label(self)
        self.winner.grid(row=0, column=0)

        self.back_button = Button(self, text="Back to menu")
        self.back_button.grid(row=1, column=0)

    def set_greetings(self, winner_name: str) -> None:
        if winner_name is not None:
            self.winner.config(text=self.WINNER.format(winner_name))
        else:
            self.winner.config(text="TIE")
