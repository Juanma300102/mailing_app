import imaplib
import ssl
import time
from common_services import MailingService


def main():
    
    context = ssl.create_default_context()
    with imaplib.IMAP4_SSL('imap.hostinger.com', 993, ssl_context=context) as conn:
        conn.login('no-reply4@poloticmisiones.com', 'Poloticmailing2021')
        conn.append('INBOX.Sent', '\\Seen', imaplib.Time2Internaldate(time.time()), 'hola'.encode('utf8'))
        

if __name__ == '__main__':
    main()