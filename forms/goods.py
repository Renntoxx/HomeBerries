from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.fields.simple import FileField
from wtforms.validators import DataRequired
from forms.flask_upl import UploadSet, configure_uploads, IMAGES, patch_request_class

photos = UploadSet('photos', IMAGES)


class GoodsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    cost = TextAreaField("Цена")
    submit = SubmitField('Применить')
    photo = FileField('Загрузить фото товара', validators=[FileAllowed(photos, 'Images only!')])


class UploadForm(FlaskForm):
    photo = FileField(
        validators=[FileAllowed(photos, 'Image only!'), FileRequired('File was empty!')])
    submit = SubmitField('Upload')
