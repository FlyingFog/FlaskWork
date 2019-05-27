from flask import render_template, redirect, url_for, request, flash
from . import auth
from .. import db
from app.auth.forms import LoginForm, SignupForm
from ..models import User, Share, Question


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
        name = request.form.get('name')
        password = request.form.get('password')
        user = User.query.filter_by(name=signup_form.name.data).first()
        if user:
            flash('用户已存在')
        else:
            new_user = User(name=name, password=password)
            try:
                db.session.add(new_user)
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


