from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField


class BalanceFrom(FlaskForm):
    balance = StringField("Сумма пополнения")
    submit = SubmitField("Подтвердить")
