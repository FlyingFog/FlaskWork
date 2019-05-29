from flask_wtf import FlaskForm, validators
from wtforms import StringField, SubmitField, PasswordField ,BooleanField ,FileField
from wtforms.validators import DataRequired, EqualTo, ValidationError,Length
from ..models import User

class LoginForm(FlaskForm):
    email = StringField('email:', validators=[DataRequired()])
    password = PasswordField('password:', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in.')
    submit = SubmitField('登录')


class SignupForm(FlaskForm):
    email = StringField('email',validators=[DataRequired(),])
    username = StringField('name:', validators=[DataRequired()])
    password = PasswordField('password:', validators=[DataRequired()])
    password2 = PasswordField('confirm password:', validators=[DataRequired(), EqualTo('password', "密码不一样")])
    # image = FileField(u'Image File', [validators.regexp(u'^[^/\\]\.jpg$')])
    image = FileField(u'image file:')
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

