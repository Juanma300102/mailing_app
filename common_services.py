import email.utils
import smtplib
import imaplib
from email.mime.application import MIMEApplication
import ssl
import time
from tkinter import messagebox
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
import os
import csv
import configparser
import datetime
import logging

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
    logging.basicConfig(format='%(asctime)s : %(levelname)s: %(message)s', level=logging.DEBUG, datefmt='%Y/%m/%d %H:%M:%S')
    logger = logging.getLogger(__name__)

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
            self.logger.debug('Buscando conexion anterior en caso de existir...')
            try:
                del self.conn
                self.logger.debug('Conexion anterior eliminada')
            except Exception:
                self.logger.debug('No existe conexion. Procediendo...')
            
            self.logger.info('Iniciando sesion...')
            
            self.conn = smtplib.SMTP_SSL(host=self.host, port=self.port)
            self.us = us
            self.pw = pw
            self.conn.connect(host=self.host, port=self.port)
            self.conn.ehlo_or_helo_if_needed()
            self.conn.login(us, pw)
            self.conn.auth_login()
            self.logger.info('Login exitoso')
        except smtplib.SMTPException as a:
            self.logger.error('Fallo al intentar login\n{a}')
            raise a

    def clasifyAndMakeSendMails(self, subject, from_, recipient, content, is_list_of_recipiets:bool, template_, footer=None,
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
        try:
            if not is_list_of_recipiets:
                response = self._send_single_mail(content=content,
                                                name_=_name,
                                                from_=from_,
                                                recipient=recipient,
                                                template_=template_,
                                                subject=subject,
                                                footer=footer,
                                                cc=cc,
                                                bcc=bcc,
                                                _pdf = pdf)
            
            else: # Caso que se envien a recipientes multiples
                if type(recipient) is list:
                    recipients_stack = []
                    recipients_counting = 0
                    for email, name_, lastname, dni, pdf in recipient:
                        recipients_stack.append(email)
                        recipients_counting+=1
                        if len(recipients_stack) == 30 or recipients_counting == len(recipient):
                            self.logger.debug(f'Recipients length: {len(recipients_stack)}')
                            self._send_single_mail(content=content,
                                                name_='',
                                                from_=from_,
                                                recipient=email,
                                                template_=template_,
                                                subject=subject,
                                                footer=footer,
                                                cc=cc,
                                                bcc=', '.join(recipients_stack),
                                                _pdf=pdf,
                                                continue_in=continue_in)
                            recipients_stack = []
                    self.reset_counter()
                else:
                    self.logger.warning('Recipient must be a list')
        except smtplib.SMTPException as err:
            self.logger.error(f'{err}\n\nMail counter: {self.mailSendedCounter - 1}')
            raise err

    def _send_single_mail(self, content, name_, from_, recipient, template_, subject, footer, cc, bcc, _pdf, continue_in:int = 0):
        mail = self._makeMail(_content=content,
                                     name=name_,
                                     from_=from_,
                                     recipient=recipient,
                                     template=template_,
                                     subject=subject,
                                     footer=footer,
                                     _cc=cc,
                                     _bcc=bcc)

        if _pdf is not None and _pdf != '':
            with open(_pdf, 'rb') as pdf_:
                part = MIMEApplication(pdf_.read(), Name=os.path.basename(_pdf))
            part['Content-Disposition'] = f'attachment; filename={os.path.basename(_pdf)}'
            mail.attach(part)
        
        if self.mailSendedCounter > continue_in: # catch por si ocurre Exception por cantidad de mails enviados 
            try:
                response = self.conn.send_message(mail)
            except smtplib.SMTPException as e:
                if e.args[0] == 421:
                    self.conn.close()
                    self.logIn(self.us, self.pw)
                    response = self.conn.send_message(mail)
                else:
                    self.logger.debug(f'{e}\nSe esperara 5 minutos para reanudar')
                    # messagebox.showwarning(f'Error {e.errno}', f'{e}\nSe esperara 5 minutos para reanudar')
                    sleep(300)
                    self.logger.debug(f'Reanudando...')
                    self.conn.close()
                    self.logIn(self.us, self.pw)
                    response = self.conn.send_message(mail)

            try:
                self._save_copy_of_sent_mail(mail)
            except Exception:
                pass
            
            del mail
            if bcc == '':
                self.logger.info(f'{self.mailSendedCounter} Mail sended to: {recipient}, {name_}')
            elif bcc != '' and cc == '':
                self.logger.info(f'{self.mailSendedCounter} Mail sended to: {bcc} by bcc')
            elif bcc != '' and cc != '':
                self.logger.info(f'{self.mailSendedCounter} Mail sended to: {bcc} by bcc \n and to {cc} by cc')
            self.logger.debug(f'responses: {response}')
        self.mailSendedCounter += 1
    
    def _makeMail(self, _content: str, from_, subject, recipient, template, footer='', name='', _cc='', _bcc=''):
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
        msj = Template(msj.safe_substitute(content=_content.strip()))
        msj = msj.safe_substitute(nombre=name.title(), pie=footer.title())

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
    
    def _save_copy_of_sent_mail(self, mail: MIMEMultipart):
        if 'hostinger' in self.host.lower():
            self.logger.debug('Servidor smtp de hostinger detectado')
            
            context = ssl.create_default_context()
            
            self.logger.debug('Intentando conectar a servidor IMAP para guardar copia de mail enviado')
            
            with imaplib.IMAP4_SSL('imap.hostinger.com', 993, ssl_context=context) as imap_conn:    
                try:
                    data = imap_conn.login(self.us, self.pw)
                    self.logger.debug(f'Iniciada la sesion correctamente {data}')
                    
                    self.logger.debug('Conectado correctamente a servidor IMAP')
                    self.logger.debug('Intentando guardar mail')
                    try: 
                        mail_str = mail.as_string()
                        self.logger.debug(f'Mail a guardar en IMAP: {mail_str}')
                        
                        data = imap_conn.append('INBOX.Sent', '\\Seen', imaplib.Time2Internaldate(time.time()), mail_str.encode('utf8'))
                        self.logger.debug(f'Respuesta de servidor despues de ejecutar append: {data}')
                        
                        self.logger.info('Copia del correo guardada en casilla de enviados')
                    except imaplib.IMAP4_SSL.error as err:
                        self.logger.warning(f'Fallo al intentar guradar el mail en el servidor IMAP {err}')
                except imaplib.IMAP4_SSL.error as err:
                    self.logger.warning(f'Fallo al intentar conectarse al servidor IMAP {err}')
                

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
        

class INIManager(object): #TODO por completar
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
        