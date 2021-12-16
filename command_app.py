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
    csvPath = path.join(os.getcwd(),'tests_mails.csv') # 'C:\\Users\\pedro\\Desktop\\Polo\\creador_de_certificados\\certificados\\curso_React_Native\\res.csv'

    recipients = getContent(csvPath) # Se obtiene el contenido del archivo
    
    
    ## Se configura la info del correo
    subject = 'Curso de React Native - Entrega de Certificado'
    from_= f'PoloTic Misiones <{mailingBox.us}>'
    content = """Por haber finalizado el curso de React Native en el marco del Programa Trabaja Misiones Joven, se hace entrega del correspondiente 
    certificado.
    
    Saludos.
    Cualquier duda o consulta quedamos a disposicion por los canales habilitados."""
    _footer = 'Equipo PoloTic Misiones'
    
    template = 'C:\\Users\\pedro\\Desktop\\Polo\\Mailing_templates\\POLO_MAIL_TEMPLATE_BASIC.html'

    mailingBox.clasifyAndMakeSendMails(subject=subject,
                                       from_=from_,
                                       recipient=recipients,
                                       template_=template,
                                       content=content,
                                       is_list_of_recipiets=True,
                                       footer=_footer,
                                       continue_in=0)
    mailingBox.conn.close()


if __name__ == '__main__':
    main()