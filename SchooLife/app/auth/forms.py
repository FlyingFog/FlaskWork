from flask_wtf import FlaskForm, validators
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(FlaskForm):
    name = StringField('name:', validators=[DataRequired()])
    password = PasswordField('password:', validators=[DataRequired()])
    submit = SubmitField('登录')


class SignupForm(FlaskForm):
    name = StringField('name:', validators=[DataRequired()])
    password = PasswordField('password:', validators=[DataRequired()])
    password2 = PasswordField('confirm password:', validators=[DataRequired(), EqualTo('password', "密码不一样")])
    submit = SubmitField('Submit')

