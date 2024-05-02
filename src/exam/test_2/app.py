import asyncio
import tkinter
from tkinter import Tk, messagebox

from model import QuotesModel
from viewmodel import MainViewModel


class App:
    APPLICATION_NAME = "QUOTES"
    START_SIZE = 1024, 1024
    MIN_SIZE = 256, 256

    def __init__(self) -> None:
        self._root = self._setup_root()
        self._quote_model = QuotesModel()
        self._viewmodel = MainViewModel(self._quote_model, self._root, asyncio.get_event_loop())
        self.start()

    def _setup_root(self) -> Tk:
        root = Tk()
        root.geometry("x".join(map(str, self.START_SIZE)))
        root.minsize(*self.MIN_SIZE)
        root.title(self.APPLICATION_NAME)
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        return root

    async def update(self) -> None:
        while True:
            self._root.update()
            try:
                self._root.state()
            except tkinter.TclError:
                break
            await asyncio.sleep(0)

    def start(self) -> None:
        self._viewmodel.start()


class Ex:
    async def exec(self) -> None:
        await App().update()


if __name__ == "__main__":
    asyncio.run(Ex().exec())
