from flask_wtf import FlaskForm, validators
from wtforms import StringField, SubmitField, PasswordField, FileField,TextField
from wtforms.validators import DataRequired, EqualTo


class ShareForm(FlaskForm):
    content = StringField('分享：')
    submit = SubmitField('发表')


class QuestionForm(FlaskForm):
    content = StringField('问题：')
    submit = SubmitField('发表')

