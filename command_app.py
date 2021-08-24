from os import name
import os.path
from sys import path
from common_services import *

def main():
    mailingBox = MailingService('smtp.gmail.com', 465)
    mailingBox.logIn('cursossiliconmisiones@gmail.com', 'cursossilicon2021')

    csvPath = '/home/juanma/Escritorio/TRABAJO/2021/SILICON/CHARLAS/charla_prog_para_no_programadores.csv' #os.path.join(os.getcwd(),'tests_mails.csv')# 
    csvLoader = CsvLoader(csvPath, 'r', ['correo', 'nombre', 'apellido', 'dni', 'pdf'])

    recipients = csvLoader.getContentAsList(firstLineHeaders=True)
    # recipients.append(['comunicacionpoloticmisiones@gmail.com', 'Flor', '', '', ''])
    # recipients.append(['recepcionpoloticmisiones@gmail.com', 'polo', '', '', ''])
    recipients.append(['pedrozo.juanma@gmail.com', 'Juan Martin', 'Pedrozo', '43944733', ''])

    # recipients = 'gerardocabraltw@gmail.com'
    subject = 'Ciclo de charlas - Programacion para no programadores'
    from_= f'Silicon Misiones <{mailingBox.us}>'
    _content = ''                        
    _footer = 'Equipo Silicon Misiones'
    #bcc = 'pedrozo.juanma@gmail.com'
    
    template = '/home/juanma/Escritorio/PYTHON/mailing_templates/Charla_silicon/Programación para progrmadores/segunda_clase_charla_silicon.html'

    mailingBox.clasifyAndMakeSendMails(subject=subject,
                                       from_=from_,
                                       recipient=recipients,
                                       template_=template,
                                       content=_content,
                                       is_list_of_recipiets=True,
                                       footer=_footer,
                                       #_name='Marcos Gerardo Cabral',
                                       #bcc=bcc,
                                       continue_in=44) 
    csvLoader.close()
    mailingBox.conn.close()


if __name__ == '__main__':
    main()