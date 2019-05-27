import os
from flask import render_template, redirect, url_for, request, flash
from . import auth
from .. import db
from app.auth.forms import LoginForm, SignupForm
from ..models import User, Share, Question
from ..email import send_email


@auth.route('/', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        name = request.form.get('name')
        password = request.form.get('password')
        user = User.query.filter_by(name=login_form.name.data).first()
        if user:
            if password == user.password:
                return redirect(url_for('main.index', uid=user.uid))
            else:
                flash("密码错误")
        else:
            flash("用户不存在")
    else:
        if request.method == "POST":
            flash("密码不正确")
    return render_template('auth/login.html', form=login_form)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    if signup_form.validate_on_submit():
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        user = User.query.filter_by(email=signup_form.email.data).first()
        if user:
            flash('邮箱已被注册')
        else:
            if signup_form.image.data:
                has_img=1
            else:
                has_img=0
            new_user = User(name=name, password=password, email=email, has_img=has_img)
            try:
                db.session.add(new_user)
                db.session.commit()
                # 存图片
                if signup_form.image.data:
                    basedir = os.path.abspath(os.path.dirname(__file__))
                    f = request.files['image']
                    postfix = str(f.filename).split('.')[1]
                    image_name=str(new_user.uid) + '.' + postfix
                    f.save(os.path.join(os.path.join(basedir, '..', 'static'), image_name))
                # 发邮件
                send_email(email, name)
                db.session.commit()
                flash("注册成功")
                return redirect(url_for('main.index', uid=new_user.uid))
            except Exception as e:
                print(e)
                flash("注册失败")
                db.session.rollback()
    else:
        if request.method == "POST":
            flash("两次输入密码不一致")
    return render_template('auth/signup.html', form=signup_form)


