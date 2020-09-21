from app import app
from PIL import Image, ImageFilter
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials

def processImage(imagePath, detectFaces):

    logo = Image.open('logo.png')
    logoWidth = logo.width
    logoHeight = logo.height
    logoPosition = app.config['LOGO_POSITION']

    image = Image.open(imagePath)
    imageWidth = image.width
    imageHeight = image.height

    if detectFaces:
        ENDPOINT = app.config['AZURE_FACES_API_ENDPOINT']
        KEY = app.config['AZURE_FACES_API_KEY']
        face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

        with open(imagePath, "rb") as data:
            detected_faces = face_client.face.detect_with_stream(data)
            if not detected_faces:
                raise Exception('No face detected from image {}'.format(imagePath))

            image = Image.open(imagePath)

            for face in detected_faces:
                left = face.face_rectangle.left
                upper = face.face_rectangle.top
                right = left + face.face_rectangle.width
                lower = upper + face.face_rectangle.height

                cropped_face = image.crop((left, upper, right, lower))
                small_cropped_face = cropped_face.resize((cropped_face.width // 48, cropped_face.height // 48), resample=Image.BILINEAR)
                pixelated_face = small_cropped_face.resize(cropped_face.size, Image.NEAREST)
                
                #TODO Look at applying circular mask if possible?
                image.paste(pixelated_face, ((left, upper, right, lower)))
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

        image.save(app.config['STORAGE_DIR'] + "/processed/test.jpg")

        output = "Image {0} has been processed successfully".format(imagePath)
    except:
        output = "An exception occured"
    return output