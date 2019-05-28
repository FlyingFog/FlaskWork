from flask import  render_template, redirect, url_for, request, flash
from . import auth
from .. import db
from app.auth.forms import LoginForm, SignupForm
from ..models import User,Share,Question
from flask_login import logout_user
from flask_login import login_required
from flask_login import login_user
from flask_login import current_user

@auth.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        password = request.form.get('password')
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(password):
                login_user(user, form.remember_me.data)
                return redirect(url_for('auth.index', uid=user.id))
        flash("用户名或密码错误")
    return render_template('login.html', form=form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.username.data
        password = form.password.data
        user = User(email=email,username=name)
        user.generate_password(password)
        try:
            db.session.add(user)
            db.session.commit()
            flash("注册成功")
            return redirect(url_for('auth.index'))
        except Exception as e:
            print(e)
            flash("注册失败")
            db.session.rollback()
    else:
        if request.method == "POST":
            flash("两次输入密码不一致")
    return render_template('signup.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('登出成功')
    return redirect(url_for('auth.login'))


@auth.route('/index')
@login_required
def index():
    return "这是current_user: "+str(current_user.id)