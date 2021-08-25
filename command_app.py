from os import path
from common_services import *

def main():
    mailingBox = MailingService('smtp.hostinger.com', 465)
    mailingBox.logger.setLevel('INFO')
    
    mailingBox.logIn('no-reply4@poloticmisiones.com', 'Poloticmailing2021')

    csvPath = '/home/juanma/Escritorio/TRABAJO/2021/CURSOS/UX_UI_DESGIN EDICION 2/INSCRIPTOS.csv' #path.join(os.getcwd(),'tests_mails.csv')
    csvLoader = CsvLoader(csvPath, 'r', ['correo', 'nombre', 'apellido', 'dni', 'pdf'])

    recipients = csvLoader.getContentAsList(firstLineHeaders=True)
    # recipients.append(['comunicacionpoloticmisiones@gmail.com', 'Flor', '', '', ''])
    #recipients.append(['recepcionpoloticmisiones@gmail.com', 'polo', '', '', ''])
    #recipients.append(['papalucaale20@gmail.com', 'Ale', 'Papaluca', '43944733', ''])

    # recipients = 'pedrozo.juanma@gmail.com'
    subject = 'Curso Diseño UX/UI'
    from_= f'PoloTic Misiones <{mailingBox.us}>'
    _content = ''                        
    _footer = 'Equipo PoloTic Misiones'
    
    template = '/home/juanma/Escritorio/PYTHON/mailing_templates/CURSOS/POLO/Diseño UX-UI avanzado/Recordatorio clases/recordatorio_segunda_clase.html'

    mailingBox.clasifyAndMakeSendMails(subject=subject,
                                       from_=from_,
                                       recipient=recipients,
                                       template_=template,
                                       content=_content,
                                       is_list_of_recipiets=True,
                                       footer=_footer,
                                       #_name='Juan Martin Pedrozo',
                                       continue_in=0)
    csvLoader.close()
    mailingBox.conn.close()


if __name__ == '__main__':
    main()