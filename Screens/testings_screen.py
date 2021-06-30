import tkinter as tk
from style import Style


class TestScreen(tk.Frame):
    def __init__(self, _master=None):
        tk.Frame.__init__(self, master=_master)
        self.style = StyleDark()
        self.grid(column=0, row=0, sticky=tk.NSEW)

        def callback(event, str):
            a = str.get('1.0', tk.END)
            print(a)


        self.text = tk.Text(self)
        self.text.grid(column=0, row=0)

        self.text.bind('<KeyPress-Return>', lambda event, str=self.text: callback(event, str))
