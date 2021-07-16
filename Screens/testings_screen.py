import tkinter as tk
from style import Style


class TestScreen(tk.Frame):
    def __init__(self, _master=None):
        tk.Frame.__init__(self, master=_master)
        self.master = _master
        self.style = Style()
        self.grid(column=0, row=0, sticky=tk.NSEW)
        
        self.master.geometry('200x200')
        self.configure(bg=self.style.BG_COLOR)
        

        
