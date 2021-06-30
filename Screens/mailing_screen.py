from style import Style
from widgets import *
from Controllers.mailing_controller import MailGUIController
import tkinter as tk


class MailingScreen(tk.Frame):
    def __init__(self, _master=None):
        tk.Frame.__init__(self, master=_master)
        self.grid(column=0, row=0, sticky=tk.NSEW)

        self.style = Style()
        self.controller = MailGUIController(self)

        self.configure(bg=self.style.BG_COLOR, pady=5, padx=5)

        _master.title('Servicio de mailing')
        _master.geometry('650x450')
        _master.resizable(height=False, width=False)

        self._setup_widgets()
        self._set_recipients_frame()
        self._set_mail_frame()

        self.rowconfigure([i for i in range(2, self.grid_size()[1])], weight=3)
        self.rowconfigure(2, weight=1)
        self.columnconfigure([i for i in range(0, self.grid_size()[0])], weight=3)

    def _setup_widgets(self):
        self.title = Title(self, _text='Servicio de Mailing')
        self.title.grid(column=0, row=0, sticky=tk.EW)
        self.sendButton = Button(self, _text='Enviar', _command=lambda: self.controller.evaluate_state_for_sending())
        self.sendButton.grid(column=0, row=4)

    def _set_recipients_frame(self):
        self.recipientsFrame = LabelFrame(self, _text='Destinatarios')
        self.recipientsFrame.configure(fg=self.recipientsFrame.style.TITLE_COLOR)
        self.recipientsFrame.grid(column=0, row=1, sticky=tk.EW)

        self.singleRecipientEntry = Entry(self.recipientsFrame, hint='Destinatario')
        self.singleRecipientEntry.grid(column=0, row=8, sticky=tk.EW)

        self.recipientsFrame.adjust_grid_weight()
        self.recipientsFrame.rowconfigure(0, weight=0)

    def _set_mail_frame(self):
        self.mailFrame = LabelFrame(self, _text='Mail')
        self.mailFrame.configure(fg=self.recipientsFrame.style.TITLE_COLOR)
        self.mailFrame.grid(column=0, row=3, sticky=tk.NSEW)

        self.subjectEntry = Entry(self.mailFrame, hint='Asunto')
        self.subjectEntry.grid(column=0, row=0, sticky=tk.EW)

        self.bodyEntry = Text(self.mailFrame)
        self.bodyEntry.grid(column=0, row=1, sticky=tk.NSEW)

        self.footerEntry = Entry(self.mailFrame, hint='Pie de mail')
        self.footerEntry.grid(column=0, row=2, sticky=tk.EW)

        self.mailFrame.adjust_grid_weight()
