import os.path
from sys import path

from common_services import *

def main():
    mailingBox = MailingService('smtp.gmail.com', 465)
    mailingBox.logIn('recepcionpoloticmisiones@gmail.com', 'polotic30')

    csvPath = '/home/juanma/Escritorio/TRABAJO/2021/CURSOS/JAVA EDICION 2/INSCRIPTOS_JAVA.csv' #os.path.join(os.getcwd(),'tests_mails.csv')
    csvLoader = CsvLoader(csvPath, 'r', ['correo', 'nombre', 'apellido', 'dni', 'pdf'])

    recipients = csvLoader.getContentAsList(firstLineHeaders=True)
    # recipients.append(['comunicacionpoloticmisiones@gmail.com', 'Florencia', '', '', ''])
    # recipients.append(['pedrozo.juanma@gmail.com', 'Juan Martin', 'Pedrozo',/home/juanma/Escritorio/PYTHON/Proyectos_Polo/tests_mails.csv' '43944733', ''])

    # recipients = ''
    subject = 'Primer Clase Desarrollo con JAVA - Fusión Silicon Misiones'
    from_= 'Equipo Polo Tic'
    _content = ''                        
    _footer = 'Equipo Polo Tic'
    
    template = os.path.join(os.getcwd(), 'Templates', 'CURSOS', 'JAVA', 'AVISO_DE_FUSION.html')

    mailingBox.clasifyAndMakeSendMails(subject=subject,
                                       from_=from_,
                                       recipient=recipients,
                                       _template=template,
                                       content=_content,
                                       multiple_recipients=True,
                                       footer=_footer,
                                       continue_in=1191) #TODO seguir con envio de correos de java
    csvLoader.close()
    mailingBox.conn.close()


if __name__ == '__main__':
    main()