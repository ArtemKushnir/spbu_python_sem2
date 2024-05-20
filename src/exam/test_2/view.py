from tkinter import BOTH, DISABLED, EW, LEFT, NS, NSEW, Text, Tk, ttk
from tkinter.scrolledtext import ScrolledText


class MainView(ttk.Frame):
    GREETINGS = 'Welcome to "quotes"!'
    RAND = "Show random quotes"
    RESCENT = "Show rescent quotes"
    BEST = "Show best quotes"

    def __init__(self, root: Tk) -> None:
        super().__init__(root)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.best_btn = ttk.Button(self, text=self.BEST)
        self.best_btn.grid(row=1, column=1, sticky="EW")

        self.rand_btn = ttk.Button(self, text=self.RAND)
        self.rand_btn.grid(row=2, column=1, sticky="EW")

        self.resc_btn = ttk.Button(self, text=self.RESCENT)
        self.resc_btn.grid(row=3, column=1, sticky="EW")

        self.entry = ScrolledText(self)
        self.entry.grid(row=4, column=1, padx=(0, 0), sticky="EW")
