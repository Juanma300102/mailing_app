from os import path
from common_services import *

def main():
    mailingBox = MailingService('smtp.hostinger.com', 465)
    mailingBox.logIn('no-reply1@poloticmisiones.com', 'Poloticmailing2021')

    csvPath = '/home/juanma/Escritorio/TRABAJO/2021/ADVA/TALLERES/inscriptos_taller3_Adva.csv' #path.join(os.getcwd(),'tests_mails.csv')
    csvLoader = CsvLoader(csvPath, 'r', ['correo', 'nombre', 'apellido', 'dni', 'pdf'])

    recipients = csvLoader.getContentAsList(firstLineHeaders=True)
    # recipients.append(['comunicacionpoloticmisiones@gmail.com', 'Flor', '', '', ''])
    #recipients.append(['recepcionpoloticmisiones@gmail.com', 'polo', '', '', ''])
    #recipients.append(['pedrozo.juanma@gmail.com', 'Juan Martin', 'Pedrozo', '43944733', ''])

    # recipients = 'pedrozo.juanma@gmail.com'
    subject = 'Taller 3 - Programacion de Videojuegos'
    from_= f'PoloTic Misiones <{mailingBox.us}>'
    _content = ''                        
    _footer = 'Equipo PoloTic Misiones'
    
    template = '/home/juanma/Escritorio/PYTHON/mailing_templates/ADVA/ADVA_TALLER_3.html'

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