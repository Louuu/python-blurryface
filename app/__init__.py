import os
import yaml

from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

if not os.path.exists(app.config['STORAGE_DIR']):
    os.mkdir(app.config['STORAGE_DIR'])
    os.mkdir(app.config['STORAGE_DIR'] + '/upload')
    os.mkdir(app.config['STORAGE_DIR'] + '/processed')

from app import routes