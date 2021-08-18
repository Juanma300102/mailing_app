from os import path
from common_services import *

def main():
    mailingBox = MailingService('smtp.hostinger.com', 465)
    mailingBox.logIn('no-reply1@poloticmisiones.com', 'Poloticmailing2021')

    csvPath = '/home/juanma/Escritorio/TRABAJO/2021/CURSOS/JAVA EDICION 2/envios random/java_desaprobados_no_llego_correo.csv' # path.join(os.getcwd(),'tests_mails.csv') # 
    csvLoader = CsvLoader(csvPath, 'r', ['correo', 'nombre', 'apellido', 'dni', 'pdf'])

    recipients = csvLoader.getContentAsList(firstLineHeaders=True)
    # recipients.append(['comunicacionpoloticmisiones@gmail.com', 'Flor', '', '', ''])
    recipients.append(['recepcionpoloticmisiones@gmail.com', 'polo', '', '', ''])
    #recipients.append(['pedrozo.juanma@gmail.com', 'Juan Martin', 'Pedrozo', '43944733', ''])

    # recipients = 'pedrozo.juanma@gmail.com'
    subject = 'Trayecto Desarrollo Web Fullstack con Java'
    from_= 'Silicon Misiones <no-reply1@poloticmisiones.com>'
    _content = ''                        
    _footer = 'Equipo Silicon Misiones'
    
    template = '/home/juanma/Escritorio/PYTHON/mailing_templates/CURSOS/SILICON/JAVA/desaprobados_java_no_les_llego.html'

    mailingBox.clasifyAndMakeSendMails(subject=subject,
                                       from_=from_,
                                       recipient=recipients,
                                       template_=template,
                                       content=_content,
                                       is_list_of_recipiets=True,
                                       footer=_footer,
                                       #_name='Juan Martin Pedrozo',
                                       continue_in=0) #TODO Enviar correo a java SILICON (solo link)
    csvLoader.close()
    mailingBox.conn.close()


if __name__ == '__main__':
    main()