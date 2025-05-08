from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField


class IndexForm(FlaskForm):
    search = TextAreaField("Поиск товаров")
    submit = SubmitField()
