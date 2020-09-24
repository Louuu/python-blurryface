import os

from flask import render_template, flash, redirect, request, url_for
from app import app
from app.forms import UploadForm
from werkzeug.utils import secure_filename
from tasks import processImage

@app.route('/')
def index():
    print(app.config)
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        files = request.files.getlist("files")
        blur_faces = form.blur_faces.data
        for file in files:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['STORAGE_DIR'] + '/upload/' , filename))
            processImage(app.config['STORAGE_DIR'] + '/upload/' + filename, blur_faces)
        
        flash("{0} file(s) uploaded successfully".format(len(files)))
        return redirect(url_for('index'))

    return render_template('upload.html', form=form)