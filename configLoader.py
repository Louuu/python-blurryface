import os
import yaml

from kombu.utils.url import safequote

with open(r'config.yaml') as file:
    data = yaml.load(file, Loader=yaml.FullLoader)

class Config(object):

    #Configuration order is env -> yaml -> default

    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    STORAGE_DIR = os.environ.get('STORAGE_DIR') or 'storage'
    #TRANSPORT_PASS = safequote(os.getenv('TRANSPORT_PASS') or ''),
    #TRANSPORT_HOST = os.getenv('TRANSPORT_HOST')
    #CELERY_BROKER_URL = f'azurestoragequeues://:{TRANSPORT_PASS}@{TRANSPORT_HOST}'
    #CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379',
    #CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379'
    LOGO_POSITION = os.environ.get('LOGO_POSITION') or data['settings']['logo_position'] or "bottom_left"
    AZURE_FACES_API_ENDPOINT = os.environ.get('AZURE_FACES_API_ENDPOINT') or data['azure']['face_detection_endpoint'] or None
    AZURE_FACES_API_KEY = os.environ.get('AZURE_FACES_API_ENDPOINT') or data['azure']['face_detection_key'] or None
    