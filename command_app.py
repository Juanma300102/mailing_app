from os import path
from common_services import *

def setup(correo, pass_, servidor): 
    # Inicio de sesion en sistema de correos
    mailingBox = MailingService(servidor, 465) # Crea mailing service 
    mailingBox.logger.setLevel('INFO') # Configura logger de info
    mailingBox.logIn(correo, pass_) # Inicia sesion
    return mailingBox

def getContent(csvPath):
    csvLoader = CsvLoader(csvPath, 'r', ['correo', 'nombre', 'apellido', 'dni', 'pdf'])
    content = csvLoader.getContentAsList(firstLineHeaders=True)
    csvLoader.close()
    return content

def main():
    
    #logIn
    mailingBox = setup('no-reply1@poloticmisiones.com', 'Poloticmailing2021', 'smpt.hostinger.com')
    
    # Direccion de CSV de destinatarios (que incluye pdfs)
    csvPath = 'C:\\Users\\pedro\\Desktop\\Polo\\creador_de_certificados\\certificados\\res.csv' #path.join(os.getcwd(),'tests_mails.csv')

    recipients = getContent(csvPath) # Se obtiene el contenido del archivo
    
    
    ## Se configura la info del correo
    subject = 'Certificado de Taller de ADVA - Negocios de Videojuegos'
    from_= f'PoloTic Misiones <{mailingBox.us}>'
    _footer = 'Equipo PoloTic Misiones'
    
    template = 'C:\\Users\\pedro\\Desktop\\Polo\\Mailing_templates\\ADVA\\ADVA_TALLER_5_CERTIFICADOS.html'

    mailingBox.clasifyAndMakeSendMails(subject=subject,
                                       from_=from_,
                                       recipient=recipients,
                                       template_=template,
                                       content='',
                                       is_list_of_recipiets=True,
                                       footer=_footer,
                                       continue_in=0)
    mailingBox.conn.close()


if __name__ == '__main__':
    main()