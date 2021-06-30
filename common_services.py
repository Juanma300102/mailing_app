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
import earthpy as et

"""
autor: Pedrozo Juan Martin
contacto: pedrozo.juanma@gmail.com

Servicios comunes para PoloTic Misiones

Servicios creados actualmente:
    -Mailing service
    -CSVLoader
"""

class MailingService(object):
    mailSendedCounter = 0

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
        self.conn = smtplib.SMTP_SSL(host=self.host, port=self.port)


    def logIn(self, us, pw):
        """
        Funcion Log in:
        Inicia secion con el par user/password ingresado como paramentros.

        :param us: str
        :param pw: str
        :return:
        """
        try:
            self.conn.connect(host=self.host, port=self.port)
            self.conn.ehlo_or_helo_if_needed()
            self.conn.login(us, pw)
            self.conn.auth_login()
            print('Login exitoso')
        except smtplib.SMTPException as a:
            messagebox.showerror('Fallo de LogIn', str(a))

    def clasifyAndMakeSendMails(self, subject, from_, recipient, content, multiple_recipients, _template, footer=None,
                                name=None, pdf=None):
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
                                     name=name,
                                     from_=from_,
                                     recipient=recipient,
                                     template=_template,
                                     subject=subject,
                                     footer=footer)

                if pdf is not None:
                    with open(pdf, 'rb') as pdf_:
                        part = MIMEApplication(pdf_.read(), Name=os.path.basename(pdf))

                    part['Content-Disposition'] = f'attachment; filename={os.path.basename(pdf)}'
                    mail.attach(part)


                self.conn.ehlo_or_helo_if_needed()
                response = self.conn.send_message(mail)
                del mail
                print(f'Single mail sended to {name} {recipient}')
                print(f'Respuesta: {response}')
                return response

            else:
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

                        try:
                            self.conn.send_message(mail)
                        except smtplib.SMTPException as e:
                            print(f'Error: {e}\nSe esperara 5 minutos para reanudar')
                            messagebox.showwarning('Error', f'{e}\nSe esperara 5 minutos para reanudar')
                            sleep(300)
                            print('Reanudando...')
                            self.conn.send_message(mail)

                        self.mailSendedCounter += 1
                        del mail
                        print(f'{self.mailSendedCounter} Mail sended to: {email}, {name_} {lastname}')
                else:
                    print('Recipient must be a list')
        except smtplib.SMTPException as err:
            print(f'ERROR: {err}')
            return err

    def makeMail(self, _content: str, from_, subject, recipient, template, footer='', name=''):
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
        mail = MIMEMultipart()
        msj = self.getTemplate(template)
        msj = Template(msj.safe_substitute(content=_content.strip()))
        msj = msj.safe_substitute(nombre=name.title(), pie=footer.title())

        mail['from'] = from_
        mail['subject'] = subject
        mail['to'] = recipient
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


class CsvLoader(object):
    def __init__(self, csvPath, mode, fields):
        """
        Punto de inicio para la clase CSVLoader.

        :param csvPath: str path del archivo
        :param mode: str r(read)/w(write)/a(append)
        PRECAUCION: w mode sobreescribira un archivo como vacio
        :param fields:
        """
        self.csvFile = open(csvPath, mode=mode, encoding='UTF-8', newline='')
        self.fields = fields
        if self.csvFile.mode == 'r':
            self.reader = csv.DictReader(self.csvFile, fields)
        elif self.csvFile.mode == 'w':
            self.writer = csv.DictWriter(self.csvFile, fields)

    def getContentAsList(self, firstLineHeaders=False):
        """
        En caso de que el modo sea r, se crea un reader, con el cual se puede obtener todo el contenido del archivo como
        una lista.

        :param firstLineHeaders: bool
        :return: list
        """
        try:
            contentList = [[i[self.fields[0]],
                            i[self.fields[1]],
                            i[self.fields[2]],
                            i[self.fields[3]],
                            i[self.fields[4]]] for i in self.reader]
            if firstLineHeaders:
                return contentList[1:]
            else:
                return contentList
        except AttributeError as e:
            print(f'there is no reader.\nERROR: {e}')
            return None

    def close(self):
        """
        Funcion para cerrar archivo leido.

        :return:
        """
        self.csvFile.close()