import os
from kombu.utils.url import safequote

#TODO Get settings from ENV or YAML

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    STORAGE_DIR = os.environ.get('STORAGE_DIR') or 'storage'
    TRANSPORT_PASS = safequote(os.getenv('TRANSPORT_PASS') or ''),
    TRANSPORT_HOST = os.getenv('TRANSPORT_HOST')
    CELERY_BROKER_URL = f'azurestoragequeues://:{TRANSPORT_PASS}@{TRANSPORT_HOST}'
    #CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379',
    #CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379'
    LOGO_POSITION = "bottom_left"
    AZURE_FACES_API_ENDPOINT = os.environ.get('AZURE_FACES_API_ENDPOINT')
    AZURE_FACES_API_KEY = os.environ.get('AZURE_FACES_API_ENDPOINT')
    