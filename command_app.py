from os import name
import os.path
from sys import path
from common_services import *

def main():
    mailingBox = MailingService('smtp.hostinger.com', 465)
    mailingBox.logIn('no-reply1@poloticmisiones.com', 'Poloticmailing2021')

    csvPath = '/home/juanma/Escritorio/TRABAJO/2021/CURSOS/INTRO PROG 2 EDICION/SILICON/MISIONEROS_PARA_SILICON.csv' # os.path.join(os.getcwd(),'tests_mails.csv')# 
    csvLoader = CsvLoader(csvPath, 'r', ['correo', 'nombre', 'apellido', 'dni', 'pdf'])

    recipients = csvLoader.getContentAsList(firstLineHeaders=True)
    # recipients.append(['comunicacionpoloticmisiones@gmail.com', 'Flor', '', '', ''])
    # recipients.append(['recepcionpoloticmisiones@gmail.com', 'polo', '', '', ''])
    # recipients.append(['pedrozo.juanma@gmail.com', 'Juan Martin', 'Pedrozo',/home/juanma/Escritorio/PYTHON/Proyectos_Polo/tests_mails.csv' '43944733', ''])

    # recipients = 'gerardocabraltw@gmail.com'
    subject = 'Trayecto Introduccion a la Programacion'
    from_= 'Silicon Misiones <no-reply1@poloticmisiones.com>'
    _content = ''                        
    _footer = 'Equipo Silicon Misiones'
    #bcc = 'pedrozo.juanma@gmail.com'
    
    template = '/home/juanma/Escritorio/PYTHON/mailing_templates/CURSOS/SILICON/introduccion_programacion/AVISO_PRIMERA_CLASE.html'

    mailingBox.clasifyAndMakeSendMails(subject=subject,
                                       from_=from_,
                                       recipient=recipients,
                                       template_=template,
                                       content=_content,
                                       is_list_of_recipiets=True,
                                       footer=_footer,
                                       #_name='Marcos Gerardo Cabral',
                                       #bcc=bcc,
                                       continue_in=0) 
    csvLoader.close()
    mailingBox.conn.close()


if __name__ == '__main__':
    main()