from flask import render_template, redirect, url_for, request, flash
from app.email import send_email
from . import auth
from .. import db
from app.auth.forms import LoginForm, SignupForm
from ..models import User, Share, Question
from flask_login import logout_user, login_required, login_user, current_user
import os


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account.Please log in.Thanks!')
        return redirect(url_for('auth.login'))
    else:
        flash('The confirmation link is invalid or has expired.')
        return redirect('auth.unconfirmed')


# 重新发送邮件
@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return render_template('auth/unconfirmed.html')


# 未认证
@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = request.form.get('password')
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(password):
            login_user(user, form.remember_me.data)
            return redirect(url_for('auth.unconfirmed'))
        flash("用户名或密码错误")
    return render_template('auth/login.html', form=form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        print(1)
        email = form.email.data
        name = form.username.data
        password = form.password.data
        user = User(email=email, username=name)
        user.generate_password(password)
        if form.image.data:
            user.has_img = 1
        try:
            db.session.add(user)
            db.session.commit()
            # 存图片
            if form.image.data:
                basedir = os.path.abspath(os.path.dirname(__file__))
                f = request.files['image']
                postfix = str(f.filename).split('.')[1]
                image_name = str(user.id) + '.' + postfix
                f.save(os.path.join(os.path.join(basedir, '..', 'static'), image_name))
            # 发邮件
            # send_email(user.email, user=user, token=user.generate_confirmation_token())
            flash("注册成功")
            return redirect(url_for('auth.login'))
        except Exception as e:
            print(e)
            flash("注册失败")
            db.session.rollback()
    else:
        if request.method == "POST":
            flash("注册失败")
    return render_template('auth/signup.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('登出成功')
    return redirect(url_for('auth.login'))


"""
@auth.route('/index')
@login_required
def index():
    return "这是current_user: "+str(current_user.id)
"""
