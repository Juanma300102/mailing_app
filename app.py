from flask import Flask, request, render_template, redirect, flash, url_for
import os
from werkzeug.utils import secure_filename
from classes.common_services import MailingService
from classes.file_checker import FileChecker

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['MAX_CONTENT_PATH'] = 10485760
app.config['SECRET_KEY'] = os.urandom(16)
    
@app.route('/', methods=['GET', 'POST'])
def mailing():
    checker = FileChecker(app)

    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        if checker.check_file('csv', request):
            dest_csv = request.files.get('csv')
            dest_csv.save(os.path.join(app.config['UPLOAD_FOLDER'] ,secure_filename(dest_csv.filename)))
        else:
            flash('Algo salio mal con la lista de  destinatarios', category='error')
            return redirect(request.url)
            
        if checker.check_file('plantilla', request):
            template = request.files.get('plantilla')
            template.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(template.filename)))
        else:
            flash('Algo salio mal con la plantilla', category='error')
            return redirect(request.url)
        return 'Subido correctamente'
        
        

app.run(debug=True)