from common_services import *
from Screens.mailing_screen import MailingScreen
from tkinter import messagebox
import tkinter as tk


class LogInGUIController(object):
    def __init__(self, _master):
        self.master_GUI = _master
        self.app = self.master_GUI.app

    def _make_login(self):
        p1 = self._check_email(self.master_GUI.userEntry)
        p2 = self._check_password(self.master_GUI.passEntry)
        if p1 and p2:
            login_data = {'host': self.master_GUI.config_.get_host_info()[0],
                          'port': self.master_GUI.config_.get_host_info()[1],
                          'us': self.master_GUI.userEntry.get(),
                          'pw': self.master_GUI.passEntry.get(),
                          'template': self.master_GUI.config_.controller.get_template()}
            self.master_GUI.config_.get_host_info()
            self.master_GUI.grid_forget()
            self.app.mailingScreen = MailingScreen(self.master_GUI.master, login_data) # Se inicializa la pantalla de la app si email y pass son True. _master = app.root
            
            
            # TODO forget this of the root. And stablish the getter from root for login info

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
