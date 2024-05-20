import asyncio
from tkinter import DISABLED, END, NORMAL, Tk

from model import CNT_QUOTES, QuotesModel
from view import MainView


class MainViewModel:
    def __init__(self, model: QuotesModel, root: Tk, event_loop: asyncio.AbstractEventLoop):
        self._model = model
        self.root = root
        self.event_loop = event_loop

    def _bind(self, view: MainView) -> None:
        view.rand_btn.config(command=lambda: self.event_loop.create_task(self.button_config(view, "random")))
        view.resc_btn.config(command=lambda: self.event_loop.create_task(self.button_config(view, "last")))
        view.best_btn.config(command=lambda: self.event_loop.create_task(self.button_config(view, "best")))

    async def button_config(self, view: MainView, text_name: str) -> None:
        text = await self._model.parse(CNT_QUOTES, text_name)
        text = "\n".join(text)
        view.entry.configure(state=NORMAL)
        view.entry.delete("1.0", END)
        view.entry.insert("1.0", text)
        view.entry.configure(state=DISABLED)

    def start(self) -> MainView:
        frame = MainView(self.root)
        self._bind(frame)
        frame.grid(row=0, column=0, sticky="NSEW")
        return frame
