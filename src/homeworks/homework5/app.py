from tkinter import Tk

from model import GameModel
from viewmodel import ViewModel


class App:
    APPLICATION_NAME = "TIC TAC TOE"
    START_SIZE = 620, 640
    MIN_SIZE = 620, 640

    def __init__(self) -> None:
        self._root = self._setup_root()
        self._bank_model = GameModel()
        self._viewmodel = ViewModel(self._bank_model, self._root)

    def _setup_root(self) -> Tk:
        root = Tk()
        root.geometry("x".join(map(str, self.START_SIZE)))
        root.minsize(*self.MIN_SIZE)
        root.title(self.APPLICATION_NAME)
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        return root

    def start(self) -> None:
        self._viewmodel.start()
        self._root.mainloop()


if __name__ == "__main__":
    App().start()
