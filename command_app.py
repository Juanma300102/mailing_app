import os.path
from sys import path

from common_services import *

def main():
    mailingBox = MailingService('smtp.gmail.com', 465)
    mailingBox.logIn('cursospoloticmisiones@gmail.com', 'ultraTicStar32')

    csvPath = os.path.join(os.getcwd(),'intro_inscriptosxlsx.csv')
    csvLoader = CsvLoader(csvPath, 'r', ['correo', 'nombre', 'apellido', 'dni', 'pdf'])

    recipients = csvLoader.getContentAsList(firstLineHeaders=True)
    # recipients.append(['polotic.equipopedagogico@gmail.com', 'Julieta', 'Baez', '', ''])
    # recipients.append(['pedrozo.juanma@gmail.com', 'Juan Martin', 'Pedrozo',/home/juanma/Escritorio/PYTHON/Proyectos_Polo/tests_mails.csv' '43944733', ''])

    # recipients = ''
    subject = 'Curso de Introducción a la Programacion'
    from_= 'Equipo Polo Tic'
    _content = ''                        
    _footer = 'Equipo Polo Tic'
    
    template = os.path.join(os.getcwd(), 'Templates', 'CURSOS', 'introduccion_programacion', 'template_original.html')

    mailingBox.clasifyAndMakeSendMails(subject=subject,
                                       from_=from_,
                                       recipient=recipients,
                                       _template=template,
                                       content=_content,
                                       multiple_recipients=True,
                                       footer=_footer,
                                       continue_in=0) 
    csvLoader.close()
    mailingBox.conn.close()


if __name__ == '__main__':
    main()