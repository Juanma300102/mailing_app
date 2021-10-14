from os import path
from common_services import *

def main():
    mailingBox = MailingService('smtp.gmail.com', 465)
    mailingBox.logger.setLevel('INFO')
    
    mailingBox.logIn('cursospoloticmisiones@gmail.com', 'ultraTicStar32')

    csvPath = 'C:\\Users\\pedro\\Desktop\\Polo\\creador_de_certificados\\certificados\\res.csv' #path.join(os.getcwd(),'tests_mails.csv')
    csvLoader = CsvLoader(csvPath, 'r', ['correo', 'nombre', 'apellido', 'dni', 'pdf'])

    recipients = csvLoader.getContentAsList(firstLineHeaders=True)
    # recipients.append(['comunicacionpoloticmisiones@gmail.com', 'Flor', '', '', ''])
    #recipients.append(['recepcionpoloticmisiones@gmail.com', 'polo', '', '', ''])
    #recipients.append(['papalucaale20@gmail.com', 'Ale', 'Papaluca', '43944733', ''])

    # recipients = 'pedrozo.juanma@gmail.com'
    subject = 'Certificado de Taller de ADVA - Negocios de Videojuegos'
    from_= f'PoloTic Misiones <{mailingBox.us}>'
    _content = ''                        
    _footer = 'Equipo PoloTic Misiones'
    
    template = 'C:\\Users\\pedro\\Desktop\\Polo\\Mailing_templates\\ADVA\\ADVA_TALLER_5_CERTIFICADOS.html'

    mailingBox.clasifyAndMakeSendMails(subject=subject,
                                       from_=from_,
                                       recipient=recipients,
                                       template_=template,
                                       content=_content,
                                       is_list_of_recipiets=True,
                                       footer=_footer,
                                       #_name='Juan Martin Pedrozo',
                                       continue_in=1)
    csvLoader.close()
    mailingBox.conn.close()


if __name__ == '__main__':
    main()