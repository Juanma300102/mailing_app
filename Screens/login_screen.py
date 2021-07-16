import tkinter as tk
from widgets import *
from style import Style
from Screens.start_options_screen import *
from Controllers.login_controller import LogInGUIController

class LoginScreen(tk.Frame):
    def __init__(self, _master=None, app=None):
        tk.Frame.__init__(self, master=_master)
        self.app = app
        self.master = _master
        self.master.title('Log in')
        self.master.geometry('350x180')
        self.master.resizable(width=True, height=False)

        self.style = Style()
        self.configure(bg=self.style.BG_COLOR)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        self.grid(column=0, row=0, sticky=tk.NSEW)

        self.controller = LogInGUIController(self)
        self.set_login_widgets()

        self.logInButton.config(command=lambda: self.controller._make_login())


    def set_login_widgets(self):
        self.title = Title(self, _text='LogIn')
        self.title.grid(column=0, row=0, sticky=tk.EW)

        self.userEntry = Entry(self, hint='correo@ejemplo.com')
        self.userEntry.grid(column=0, row=1, pady=10)

        self.passEntry = Entry(self, hint='Password', show_='*')
        self.passEntry.grid(column=0, row=2, pady=10)

        self.logInButton = Button(self, _text='Acceder')
        self.logInButton.grid(column=0, row=3, pady=10)
        
        self.config_ = StartOptionsScreen(self)

