from common_services import *
import configparser
from tkinter import messagebox
import tkinter as tk
import os
import smtplib

class MailGUIController(object):
    def __init__(self, _master_screen, _options: dict):
        self.master = _master_screen
        self.options = _options
        self.mailingService = MailingService(_host=self.options['host'],
                                             _port=self.options['port'])
        self.mailingService.logIn(self.options['us'], self.options['pw'])

        # TODO Completar login task y route de los datos desde loginScreen                                        
        

    def evaluate_state_for_sending(self):
        # CHECK RECIPIENTS MODE
        self._evaluate_recipient_entry(self.master.singleRecipientEntry)
        self._evaluate_subject_entry(self.master.subjectEntry)
        content = self._evaluate_content(self.master.bodyEntry)
        footer = self._evaluate_footer_entry(self.master.footerEntry)

        if content and footer:
            print('Se enviara el mail')
            response = self.mailingService.clasifyAndMakeSendMails(subject=self.master.subjectEntry.get(),
                                                        from_=self.options['us'],
                                                        recipient=self.master.singleRecipientEntry.get(),
                                                        content=self.master.bodyEntry.get('1.0', tk.END),
                                                        _template=os.path.join(os.getcwd(),
                                                                               'Templates',
                                                                               self.options['template']),
                                                        multiple_recipients=False,
                                                        footer=self.master.footerEntry.get(),
                                                        _name='')

            #TODO trying to catch session timeout errno
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
