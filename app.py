from flask import Flask
from flask import render_template
from flask import request
import os
from common_services import MailingService

app = Flask('testapp')
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploaded_files')
app.config['MAX_CONTENT_PATH'] = 10485760


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/single_mail', methods=['GET', 'POST'])
def enviar_mail():
    if request.method == 'GET':
        return render_template('form.html')
    elif request.method == 'POST':
        mailingbox = MailingService('smtp.hostinger.com', 465)
        mailingbox.logIn('no-reply2@poloticmisiones.com', 'Poloticmailing2021')
        
        mailingbox.clasifyAndMakeSendMails(subject=request.form.get('asunto', type=str),
                                           from_='no-reply2@poloticmisiones.com',
                                           recipient=request.form.get('correo', type=str),
                                           content=request.form.get('cuerpo', type=str),
                                           multiple_recipients=False,
                                           _template='templates/mail_template.html',
                                           footer=request.form.get('pie', type=str))
        return 'correo enviado'
    
@app.route('/mailing', methods=['GET', 'POST'])
def mailing():
    if request.method == 'GET':
        return render_template('mailing.html')
    elif request.method == 'POST':
        pass
        

app.run(debug=True)