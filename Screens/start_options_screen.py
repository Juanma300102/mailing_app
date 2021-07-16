import tkinter as tk
from tkinter import messagebox
from Controllers.start_options_controller import *
from style import *
from widgets import *
import os


class StartOptionsScreen(tk.Frame):
    def __init__(self, _master):
        tk.Frame.__init__(self, master=_master)
        self.master = _master
        self.controller = StartOptionsGUIController(self)
        self.style = Style()
        
        self.config(bg=self.style.BG_COLOR_DARKER)
        self.grid(column=1, row=0, sticky=tk.NSEW,
                  rowspan=self.master.grid_size()[1])
        self.columnconfigure(0, weight=1)
        
        self._set_up_widgets()
    
    def _set_up_widgets(self):
        self.title = Title(self, _text='Opciones')
        self.title.configure(bg = self.style.BG_COLOR_DARKER,
                             font=tk.font.Font(family='Ubuntu', size=16))
        self.title.grid(column=0, row=0, pady=10, sticky=tk.EW)
        
        self.hostMenu = OptionMenu(self, 
                                   _values=self.controller.get_options_sections(), 
                                   default=self.controller.options.get('DEFAULT','host_selected'),
                                   _command=lambda choice: self.controller._act_host_provider(choice))
        self.hostMenu.grid(column=0, row=1, pady=10, padx=10, sticky=tk.EW)

    def get_host_info(self):
            if self.hostMenu.get_current_selection() != 'Elegir servicio':
                host_provider = self.hostMenu.get_current_selection()
                host_info = [self.controller.get_host_of(host_provider),
                             self.controller.get_port_of(host_provider)]
                return host_info
            else:
                try:
                    messagebox.showwarning('Alerta', 'Debe seleccionar un servicio antes de proceder')
                    print('Error: debe elegir un servicio')
                except:                    
                    print('Error: debe elegir un servicio')