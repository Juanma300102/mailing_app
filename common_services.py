import email.utils
import smtplib
from email.mime.application import MIMEApplication
from tkinter import messagebox
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
import os
import csv
import configparser
import datetime

"""
autor: Pedrozo Juan Martin
contacto: pedrozo.juanma@gmail.com
Servicios comunes para PoloTic Misiones
Servicios creados actualmente:
    -Mailing service
    -CSVLoader
"""

class MailingService(object):
    mailSendedCounter = 1

    def __init__(self, _host, _port):
        """
        Clase Mailing service de punto de entrada para el uso del servico.
        Setea propiedades del objeto:
            -host
            -port
            -conn: inicia la conexion con el proveedor SMTP
        Parametros obligatorios:
        :param _host: str
        :param _port: int
        """
        self.host = _host
        self.port = _port

    def logIn(self, us, pw):
        """
        Funcion Log in:
        Inicia secion con el par user/password ingresado como paramentros.
        :param us: str
        :param pw: str
        :return:
        """
        try:
            print('Iniciando sesion...')
            self.conn = smtplib.SMTP_SSL(host=self.host, port=self.port)
            self.us = us
            self.pw = pw
            self.conn.connect(host=self.host, port=self.port)
            self.conn.ehlo_or_helo_if_needed()
            self.conn.login(us, pw)
            self.conn.auth_login()
            print('Login exitoso')
        except smtplib.SMTPException as a:
            print(f'Error: Fallo al intentar login\n{a}')
            raise a

    def clasifyAndMakeSendMails(self, subject, from_, recipient, content, multiple_recipients, _template, footer='',
                                _name='', pdf=None, cc='', bcc='', continue_in=0):
        """
        Funcion para clasificar y ejecutar el envio de mails de acuerdo a los parametros recibidos.
        :param template: path to html template
        :param footer: str
        :param subject: str
        :param from_: str
        :param recipient:
        :param content: str
        :param multiple_recipients: bool
        :param name: str
        :param pdf: str
        :return:
        """
        self.conn.auth_login()
        try:
            if not multiple_recipients:
                mail = self.makeMail(_content=content,
                                     name=_name,
                                     from_=from_,
                                     recipient=recipient,
                                     template=_template,
                                     subject=subject,
                                     footer=footer,
                                     _cc=cc,
                                     _bcc=bcc)

                if pdf is not None:
                    with open(pdf, 'rb') as pdf_:
                        part = MIMEApplication(pdf_.read(), Name=os.path.basename(pdf))

                    part['Content-Disposition'] = f'attachment; filename={os.path.basename(pdf)}'
                    mail.attach(part)

                self.conn.ehlo_or_helo_if_needed()
                response = self.conn.send_message(mail)
                del mail
                self.mailSendedCounter += 1
                print(f'{datetime.datetime.now()} {self.mailSendedCounter} Single mail sended to {_name} {recipient}')
                print(f'Respuesta: {response}')
                return response
            
            else: # Caso que se envien a recipientes multiples
                if type(recipient) is list:
                    for email, name_, lastname, dni, pdf in recipient:
                        mail = self.makeMail(subject=subject,
                                             recipient=email,
                                             name=f'{name_} {lastname}',
                                             from_=from_,
                                             template=_template,
                                             _content=content,
                                             footer=footer)
                        # print(pdf)
                        if pdf is not None and pdf != '':
                            with open(pdf, 'rb') as pdf_:
                                part = MIMEApplication(pdf_.read(), Name=os.path.basename(pdf))

                            part['Content-Disposition'] = f'attachment; filename={os.path.basename(pdf)}'
                            mail.attach(part)
                        
                        if self.mailSendedCounter > continue_in: # catch por si ocurre Exception por cantidad de mails enviados 
                            try:
                                self.conn.send_message(mail)
                            except smtplib.SMTPException as e:
                                print(f'Error: {e}\nSe esperara 5 minutos para reanudar')
                                # messagebox.showwarning(f'Error {e.errno}', f'{e}\nSe esperara 5 minutos para reanudar')
                                sleep(300)
                                print('Reanudando...')
                                self.conn.close()
                                self.logIn(self.us, self.pw)
                                self.conn.send_message(mail)

                            del mail
                            print(f'{datetime.datetime.now()} {self.mailSendedCounter} Mail sended to: {email}, {name_} {lastname}')
                        self.mailSendedCounter += 1
                    self.reset_counter()
                else:
                    print('Recipient must be a list')
        except smtplib.SMTPException as err:
            print(f'ERROR: {err}\n\nMail counter: {self.mailSendedCounter - 1}')
            return err

    def makeMail(self, _content: str, from_, subject, recipient, template, footer:str='', name:str='', _cc='', _bcc=''):
        """
        Funcion para crear el objeto mail a enviar. Lo retorna al proceso que lo llama.
        :param template: path to html template for te mail
        :param footer:
        :param name:
        :param _content: str path to html or txt file
        :param from_: str
        :param subject: str
        :param recipient: str
        :return: mail class MIMEMultipart
        """
        mail = MIMEMultipart('alternative')
        msj = self.getTemplate(template)
        msj = Template(msj.safe_substitute(content=_content))
        msj = msj.safe_substitute(nombre=name.title(), pie=footer)

        mail['from'] = from_
        mail['subject'] = subject
        mail['to'] = recipient if _bcc == '' else None
        mail['cc'] = _cc if _cc != '' else None
        mail['bcc'] = _bcc if _bcc != '' else None
        mail['date'] = email.utils.formatdate()

        mail.attach(MIMEText(Template(_content).safe_substitute(nombre=''), 'plain/text'))
        mail.attach(MIMEText(msj, 'html'))

        return mail

    def getTemplate(self, path):
        """
        Funcion para cargar el html/txt pasado como template por su path
        :param path: str path
        :return: Template
        """
        with open(path, 'r', encoding='utf-8') as template:
            templateContent = template.read()
        return Template(templateContent)

    def reset_counter(self):
        self.mailSendedCounter = 1

class CsvLoader(object):
    def __init__(self, csvPath: str, mode: str, fields: list):
        """
        Constructor para la clase CSVLoader.
        :param csvPath: str path del archivo
        :param mode: str r(read)/w(write)/a(append)
        PRECAUCION: w mode sobreescribira un archivo como vacio
        :param fields:
        """

        self.csvFile = open(csvPath, mode=mode, encoding='UTF-8', newline='')
        self.fields = fields

        if self.csvFile.mode == 'r':
            self.reader = csv.DictReader(self.csvFile, fields)
        elif self.csvFile.mode == 'w' or self.csvFile.mode == 'a':
            self.writer = csv.DictWriter(self.csvFile, fields)
            if self.csvFile.mode == 'w':
                self.writer.writeheader()

    def getContentAsList(self, firstLineHeaders=False, verbose=False):
        """
        En caso de que el modo sea r, se crea un reader, con el cual se puede obtener todo el contenido del archivo como
        una lista.
        :param firstLineHeaders: bool
        :return: list
        """
        try:
            contentList: list = []
            row: list = []
            for i in self.reader:
                for field in self.fields:
                    row.append(i[field])
                contentList.append(row)
                row = []
            if firstLineHeaders:
                [print(r) for r in contentList[1:]] if verbose else None
                return contentList[1:]
            else:
                [print(r) for r in contentList] if verbose else None
                return contentList
        except AttributeError as e:
            print(f'there is no reader.\nERROR: {e}')
            return None

    def write_row(self, row: list):
        try:
            dict_row = {}
            
            for key, value in zip(self.fields, row):
                dict_row[key] = value
                
            self.writer.writerow(dict_row)
        except AttributeError as e:
            print(f'there is no writer.\nERROR: {e}')
        
    def close(self):
        """
        Funcion para cerrar archivo leido.
        :return:
        """
        self.csvFile.close()
        

class INIManager(object):
    def __init__(self, path_to_ini):
        self.reader = configparser.ConfigParser()
        self.path = path_to_ini
    
    def get(self, section, option):
        self.reader.read(self.path)
        return self.reader.get(section, option)
        
    
    def set_(self, section, option, value):
        self.reader.read(self.path)
        self.reader.set(section, option, value)
        return value
    
    def sections(self):
        self.reader.read(self.path)
        return self.reader.sections()