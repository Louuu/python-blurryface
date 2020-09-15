import os
import sys
import yaml

from flask import Flask, flash, request, render_template
from PIL import Image
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/config')
def show_config():
    return config

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file in request")
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(config['settings']['path_uploads'], filename))
            flash('File uploaded successfully')
            flash(process_image(filename))
        else:
            flash('File uploaded failed')
    return render_template("upload.html")

def load_config():
    with open(r'config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    return config

def process_image(imageName):
        
    #Set Paths
    imagePath = config['settings']['path_uploads'] + imageName
    outputPath = config['settings']['path_processed']

    #Open Logo and Get Attributes
    logo = Image.open(config['settings']['path_logo'])
    logoWidth = logo.width
    logoHeight = logo.height
    logoPosition = config['settings']['logo_position']

    #Open Image and Get Attributes
    image = Image.open(imagePath)
    imageWidth = image.width
    imageHeight = image.height

    try:
        if logoPosition == "top_left":
            image.paste(logo, (0, 0), logo)
        elif logoPosition == "top_right":
            image.paste(logo, (imageWidth - logoWidth, 0), logo)
        elif logoPosition == "bottom_right":
            image.paste(logo, (imageWidth - logoWidth, imageHeight - logoHeight), logo)
        elif logoPosition == "bottom_left":
            image.paste(logo, (0, imageHeight - logoHeight), logo)
        else:
            output = "Error: Position {0} is not valid".format(logoPosition)

        image.save(outputPath + imageName)
        output = "Image {0} has been processed successfully".format(imagePath)
    except:
        output = "An exception occured"
    return output

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config['settings']['allowed_extensions']

config = load_config()