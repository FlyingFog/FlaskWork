from flask_wtf import FlaskForm, validators
from wtforms import StringField, SubmitField, PasswordField, FileField, TextField, IntegerField
from wtforms.validators import DataRequired, EqualTo


class ShareForm(FlaskForm):
    label=StringField('分享标题：')
    content = StringField('分享内容：')
    submit = SubmitField('发表')


class QuestionForm(FlaskForm):
    label=StringField('问题标题：')
    content = StringField('问题内容：')
    submit = SubmitField('发表')


class ProfileForm(FlaskForm):
    image = FileField('头像：')
    email = StringField('邮箱')
    name = StringField('名称:')
    password = PasswordField('密码:')
    password2 = PasswordField('确认密码:')
    realname = StringField('真实姓名:')
    gender = IntegerField('性别:')
    age = IntegerField('年龄:')
    school = StringField('学校')
    selfinfo = StringField('自我介绍')
    submit = SubmitField('提交修改')
