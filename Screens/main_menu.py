import tkinter as tk
from style import Style
from widgets import Title


class Menu(tk.Frame):
    def __init__(self, _master):
        tk.Frame.__init__(self, master=_master)
        self.master.geometry('200x200')
        self.grid(column=0, row=0, sticky=tk.NSEW)
        self.style = Style()
        self.configure(bg=self.style.BG_COLOR)
        self.setUpWidgets()
        self.columnconfigure([i for i in range(0, self.grid_size()[0])], weight=1)
        self.rowconfigure([i for i in range(0, self.grid_size()[1])], weight=1)

    def setUpWidgets(self):
        self.title = Title(self, _text='Main Menu')
        self.title.grid(column=0, row=0, columnspan=3, sticky=tk.NSEW)

