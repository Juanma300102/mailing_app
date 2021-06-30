from common_services import MailingService, CsvLoader
import configparser
from tkinter import messagebox
import tkinter as tk
from Controllers.login_controller import LogInGUIController
import os
import smtplib

class MailGUIController(object):
    def __init__(self, _master_screen):
        self.master = _master_screen

        self.settings = configparser.ConfigParser()
        self.settings.read(os.path.join(os.getcwd(), 'options.ini'))

        self.logInScreen = LogInGUIController(self.master)
        
        self.mailingService = MailingService(self.settings.get('DEFAULT', 'host'), self.settings.get('DEFAULT', 'port'))
        self.logInScreen.make_login()

    def evaluate_state_for_sending(self):
        # CHECK RECIPIENTS MODE
        self._evaluate_recipient_entry(self.master.singleRecipientEntry)
        self._evaluate_subject_entry(self.master.subjectEntry)
        content = self._evaluate_content(self.master.bodyEntry)
        footer = self._evaluate_footer_entry(self.master.footerEntry)

        if content and footer:
            print('Se enviara el mail')
            response = self.mailingService.clasifyAndMakeSendMails(subject=self.master.subjectEntry.get(),
                                                        from_='equipodesarrollo@poloticmisiones.com',
                                                        recipient=self.master.singleRecipientEntry.get(),
                                                        content=self.master.bodyEntry.get('1.0', tk.END),
                                                        _template=os.path.join(os.getcwd(),
                                                                               'Templates',
                                                                               self.settings['DEFAULT']['template']),
                                                        multiple_recipients=False,
                                                        footer=self.master.footerEntry.get(),
                                                        name='')
            print(response.errno) if type(response) is smtplib.SMTPException else None

    def _evaluate_recipient_entry(self, entry):
        print('Evaluating recipient...')
        content = entry.get()
        if '@' not in content:
            print('El destinatario debe ser una direccion de correo valida')
            messagebox.showwarning('Alerta', 'El destinatario debe ser una direccion de correo valida')
        else:
            print('OK')

    def _evaluate_subject_entry(self, entry):
        print('Evaluating subject...')
        content = entry.get()
        if content == 'Asunto' or content == '':
            print('Debe ingresar un asunto')
            messagebox.showwarning('Alerta', 'Debe ingresar un Asunto')
        else:
            print('OK')

    def _evaluate_content(self, text):
        content: str = text.get('1.0', tk.END)
        #print(content)
        print('Evaluating content...')
        if content.strip() == '':
            response = messagebox.askyesno('Alerta', 'Se esta por enviar un correo sin cuerpo. Desea continuar?')
            if response:
                print('OK')
            return response
        else:
            print('OK')
            return True

    def _evaluate_footer_entry(self, entry):
        print('Evaluating subject...')
        content = entry.get()
        print(type(content))
        if content == 'Pie de mail' or content == '':
            print('Se esta por enviar un correo sin pie')
            response = messagebox.askyesno('Alerta', 'Se esta por enviar un correo sin pie. Desea continuar?')
            if response:
                print('OK')
            return response
        else:
            print('OK')
            return True
