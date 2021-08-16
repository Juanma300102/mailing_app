from os import name
import os.path
from sys import path
from common_services import *

def main():
    mailingBox = MailingService('smtp.hostinger.com', 465)
    mailingBox.logIn('no-reply2@poloticmisiones.com', 'Poloticmailing2021')

    csvPath = os.path.join(os.getcwd(),'tests_mails.csv') #' '/home/juanma/Escritorio/TRABAJO/2021/CURSOS/JAVA EDICION 2/aprobados.csv' # 
    csvLoader = CsvLoader(csvPath, 'r', ['correo', 'nombre', 'apellido', 'dni', 'pdf'])

    # recipients = csvLoader.getContentAsList(firstLineHeaders=True)
    # recipients.append(['comunicacionpoloticmisiones@gmail.com', 'Flor', '', '', ''])
    # recipients.append(['recepcionpoloticmisiones@gmail.com', 'polo', '', '', ''])
    # recipients.append(['pedrozo.juanma@gmail.com', 'Juan Martin', 'Pedrozo',/home/juanma/Escritorio/PYTHON/Proyectos_Polo/tests_mails.csv' '43944733', ''])

    recipients = 'pedrozo.juanma@gmail.com'
    subject = 'Trayecto Desarrollo Web Fullstack con Java'
    from_= 'Silicon Misiones <no-reply2@poloticmisiones.com>'
    _content = ''                        
    _footer = 'Equipo Silicon Misiones'
    
    template = '/home/juanma/Escritorio/PYTHON/mailing_templates/CURSOS/SILICON/JAVA/AVISO_SEGUNDA_CLASE.html'

    mailingBox.clasifyAndMakeSendMails(subject=subject,
                                       from_=from_,
                                       recipient=recipients,
                                       template_=template,
                                       content=_content,
                                       is_list_of_recipiets=False,
                                       footer=_footer,
                                       _name='Juan Martin Pedrozo',
                                       continue_in=0) #TODO Enviar correo a java SILICON (solo link)
    csvLoader.close()
    mailingBox.conn.close()


if __name__ == '__main__':
    main()