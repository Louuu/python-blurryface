from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, MultipleFileField, SelectField
from wtforms.validators import ValidationError, DataRequired, StopValidation
from flask_wtf.file import FileRequired, FileAllowed
from werkzeug.datastructures import FileStorage
from collections.abc import Iterable

class MultiFileAllowed(object):
    def __init__(self, upload_set, message=None):
        self.upload_set = upload_set
        self.message = message

    def __call__(self, form, field):

        if not (all(isinstance(item, FileStorage) for item in field.data) and field.data):
            return

        for data in field.data:
            filename = data.filename.lower()

            if isinstance(self.upload_set, Iterable):
                if not any(filename.endswith("." + x) for x in self.upload_set):
                    raise StopValidation(
                        self.message
                        or field.gettext("File does not have an approved extension: {extensions}").format(
                            extensions=", ".join(self.upload_set)
                        )
                    )

class UploadForm(FlaskForm):
    event = StringField('Event Name', [DataRequired()])
    files = MultipleFileField('Images', validators=[
        DataRequired(),
        MultiFileAllowed(['jpg', 'png', 'jpeg'])
    ])
    blur_faces = BooleanField('Blur Faces')
    submit = SubmitField('Upload')