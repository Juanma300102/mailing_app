from flask import Flask, request, render_template, redirect, flash, url_for
import os
from werkzeug.utils import secure_filename
from classes.common_services import MailingService, CsvLoader
from classes.file_checker import Checker
from smtplib import SMTPException
import datetime

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['MAX_CONTENT_PATH'] = 10485760
app.config['SECRET_KEY'] = os.urandom(16)

mailingbox = MailingService('smtp.hostinger.com', 465)

@app.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        return render_template('home.html')
    
@app.route('/mailing', methods=['GET', 'POST'])
def mailing():
    checker = Checker(app)
    
    if request.method == 'GET':
        """try:
            mailingbox"""
        return render_template('mailing.html')
    elif request.method == 'POST':
        if checker.check_file('csv', request):
            dest_csv = request.files.get('csv')
            dest_csv.save(os.path.join(app.config['UPLOAD_FOLDER'] ,secure_filename(dest_csv.filename)))
            csv_path = os.path.join(app.config['UPLOAD_FOLDER'] ,secure_filename(dest_csv.filename))
        else:
            flash('Algo salio mal con la lista de  destinatarios', category='warning')
            return redirect(request.url)
            
        if checker.check_file('plantilla', request):
            template = request.files.get('plantilla')
            template.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(template.filename)))
            template_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(template.filename))
        else:
            flash('Algo salio mal con la plantilla', category='warning')
            return redirect(request.url)
        
        csv = CsvLoader(csv_path, 'r', ['correo', 'nombre', 'apellido', 'dni' ,'pdf']).getContentAsList(firstLineHeaders=True)
        
        try:
            mailingbox.clasifyAndMakeSendMails(subject = request.form.get('asunto'),
                                               from_ = f'{request.form.get("remitente")} <no-reply1@poloticmisiones.com>',
                                               recipient=csv,
                                               content='',
                                               is_list_of_recipiets=True,
                                               template_=template_path,
                                               footer=request.form.get('pie'),
                                               continue_in=0)
        except SMTPException as err:
            flash(f'Algo salio mal: {err}', category='warning')    
            return redirect(request.url)
        
        os.remove(os.path.join(os.getcwd(), 'uploads', secure_filename(dest_csv.filename)))
        os.remove(os.path.join(os.getcwd(), 'uploads', secure_filename(template.filename)))
        flash(f'Datos correctamente cargados.', category='toast-success')
        flash(f'Se enviará el mail a {len(csv)} destinatarios confirmados.  ', category='toast-success')
        return redirect(request.url)

@app.route('/make_login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        validacion_correo = 'correo' not in request.form or request.form.get('correo') == ''
        validacion_contraseña = 'contraseña' not in request.form or request.form.get('contraseña') == ''
        print(validacion_contraseña, validacion_correo)
        
        if validacion_contraseña or validacion_correo:
            flash('Debe ingresar usuario y contraseña', category='warning')
            return redirect(url_for('home'))
        else:
            try:
                mailingbox.logIn(request.form.get('correo'), request.form.get('contraseña'))
                flash('Sesión iniciada correctamente', category='success')
                return render_template('mailing.html')
            except SMTPException as err:
                print(f'{datetime.datetime.now().strftime("%H:%M:%S")}: Error: {err.args[0]}')
                if err.args[0] == 535:
                    flash('Usuario y/o contraseña incorrecta', category='warning')
                    return redirect(url_for('home'))
                flash('Algo salio mal durante el logueo', category='warning')
                return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)