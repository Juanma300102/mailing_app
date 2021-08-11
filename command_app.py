from os import name
import os.path
from sys import path

from common_services import *

def main():
    mailingBox = MailingService('smtp.gmail.com', 465)
    mailingBox.logIn('cursospoloticmisiones@gmail.com', 'ultraTicStar32')

    csvPath =  '/home/juanma/Escritorio/TRABAJO/2021/ADVA/TALLERES/inscriptos_taller3_Adva.csv'  # os.path.join(os.getcwd(),'tests_mails.csv')  
    csvLoader = CsvLoader(csvPath, 'r', ['correo', 'nombre', 'apellido', 'dni', 'pdf'])

    recipients = csvLoader.getContentAsList(firstLineHeaders=True)
    #recipients.append(['comunicacionpoloticmisiones@gmail.com', 'Florencia', '', '', ''])
    # recipients.append(['pedrozo.juanma@gmail.com', 'Juan Martin', 'Pedrozo',/home/juanma/Escritorio/PYTHON/Proyectos_Polo/tests_mails.csv' '43944733', ''])

    #recipients = 'rodriguezmarianela81@gmail.com'
    subject = 'Segundo encuentro - Taller de Programacion de Videojuegos'
    from_= 'Equipo Polo Tic'
    _content = ''                        
    _footer = 'Equipo Polo Tic'
    
    template = os.path.join(os.getcwd(), 'Templates', 'ADVA', 'ADVA_TALLER_3.html')

    mailingBox.clasifyAndMakeSendMails(subject=subject,
                                       from_=from_,
                                       recipient=recipients,
                                       _template=template,
                                       content=_content,
                                       multiple_recipients=True,
                                       footer=_footer,
                                       #_name='Marianela',
                                       continue_in=6) #TODO Enviar correo a java SILICON (solo link)
    csvLoader.close()
    mailingBox.conn.close()


if __name__ == '__main__':
    main()