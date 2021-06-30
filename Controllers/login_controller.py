from common_services import *
from Screens.login_screen import LoginScreen
import configparser
from tkinter import messagebox
import tkinter as tk


class LogInGUIController(object):
    def __init__(self, _master_screen):
        self.master = _master_screen

    def make_login(self):
        self.topLevel = tk.Toplevel(self.master)
        self.master.master.iconify()
        self.GUI = LoginScreen(self.topLevel)

        self.topLevel.columnconfigure([i for i in range(0, self.topLevel.grid_size()[0])], weight=1)
        self.topLevel.rowconfigure([i for i in range(0, self.topLevel.grid_size()[1])], weight=1)

        self.GUI.logInButton.configure(command=lambda: self._get_data())

    def _get_data(self):
        p1 = self._check_email(self.GUI.userEntry)
        p2 = self._check_password(self.GUI.passEntry)
        if p1 and p2:
            _us = self.GUI.userEntry.get()
            _pw = self.GUI.passEntry.get()
            self.master.controller.mailingService.logIn(us=_us, pw=_pw)
            self.topLevel.destroy()
            self.master.master.deiconify()

    def _check_email(self, entry):
        print('Evaluando correo...')
        if '@' not in entry.get() or entry.get() == '':
            messagebox.showwarning('Correo invalido', 'La direccion de correo debe ser una direccion valida, e incluir'
                                                      '@')
            return False
        else:
            print('OK')
            return True

    def _check_password(self, entry):
        print('Evaluando contrasenia...')
        if entry.get() == '':
            messagebox.showwarning('contraseña requerida', 'Debe ingresar una contraseña')
            return False
        else:
            print('OK')
            return True
