import os
import sys
import yaml
import uuid
import requests

from flask import Flask, flash, request, redirect, render_template
from PIL import Image, ImageFilter
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials

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
        
        files = request.files.getlist("file")
        for file in files:
            
            if 'file' not in request.files:
                flash("No file in request")
                return redirect(request.url)
        
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
        detect_faces(outputPath + imageName, imageName)
        upload_to_azure(outputPath + imageName, imageName)
        
        output = "Image {0} has been processed successfully".format(imagePath)
    except:
        output = "An exception occured"
    return output

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config['settings']['allowed_extensions']

def upload_to_azure(filepath, filename):
    connect_str = config['azure']['storage_connection_string']
    container_name = config['azure']['storage_container_name']
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)

    with open(filepath, "rb") as data:
        blob_client.upload_blob(data)
        blob_client.set_blob_metadata(metadata={"Application":"Image Uploader"})

def detect_faces(filepath, filename):
    ENDPOINT = config['azure']['face_detection_endpoint']
    KEY = config['azure']['face_detection_key']
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

    with open(filepath, "rb") as data:
        detected_faces = face_client.face.detect_with_stream(data)
        if not detected_faces:
            raise Exception('No face detected from image {}'.format(filename))

        img = Image.open(filepath)

        for face in detected_faces:
            left = face.face_rectangle.left
            upper = face.face_rectangle.top
            right = left + face.face_rectangle.width
            lower = upper + face.face_rectangle.height

            cropped_face = img.crop((left, upper, right, lower))
            
            blurred_face = cropped_face.filter(ImageFilter.BoxBlur(radius=100))
            img.paste(blurred_face, ((left, upper, right, lower)))
            print("Faces blurred")
        img.save(filepath)
    return "Done"
    
config = load_config()