import tkinter as tk
from widgets import *
from style import Style

class LoginScreen(tk.Frame):
    def __init__(self, Master=None):
        tk.Frame.__init__(self, master=Master)
        Master.geometry('250x200')

        self.style = Style()
        self.configure(bg=self.style.BG_COLOR)
        self.grid(column=0, row=0, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)

        self.set_login_widgets()


    def set_login_widgets(self):
        self.title = Title(self, _text='LogIn')
        self.title.grid(column=0, row=0, sticky=tk.EW)

        self.userEntry = Entry(self, hint='correo@ejemplo.com')
        self.userEntry.grid(column=0, row=1, pady=10)

        self.passEntry = Entry(self, hint='Password', show_='*')
        self.passEntry.grid(column=0, row=2, pady=10)

        self.logInButton = Button(self, _text='Acceder')
        self.logInButton.grid(column=0, row=3, pady=10)

