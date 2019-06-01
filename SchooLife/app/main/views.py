from flask import render_template, redirect, url_for, request, flash
from . import main
from .. import db
from ..models import User, Share, Question
import random
from app import login_manager
from app.main.forms import ShareForm, QuestionForm, ProfileForm
from ..email import send_email

from flask_login import login_required, current_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@main.route('/index/shares', methods=['GET', 'POST'])
@login_required
def index():
    user = current_user
    share_form = ShareForm()
    if request.method == "POST":
        s_label = request.form.get('label')
        s_content = request.form.get('content')
        print(s_label)
        print(s_content)
        share = Share(label=s_label,
                      content=s_content,
                      writer=user)
        try:
            flash("发布成功")
            db.session.add(share)
            db.session.commit()
            return redirect(url_for('main.index'))
        except Exception as e:
            print(e)
            flash("发布失败")
            db.session.rollback()
    return render_template('user/index.html',
                           user=user,
                           share_form=share_form,
                           rand=random.randint(1000, 9999))


@main.route('/index', methods=['GET', 'POST'])
@login_required
def shares():
    user = current_user
    shares = [1, 2, 3, 4, 5, 6]
    return render_template('user/index.html', user=user, shares=shares)


@main.route('/index/QandAs', methods=['GET', 'POST'])
@login_required
def QandAs():
    user = current_user
    questions = [1, 2, 3, 4, 5, 6]
    return render_template('user/Q&As.html', user=user,questions=questions)


@main.route('/index/following', methods=['GET', 'POST'])
@login_required
def following():
    user = current_user
    followings = [1, 2, 3, 4, 5, 6]
    return render_template('user/following.html', user=user,followings=followings)


@main.route('/index/follower', methods=['GET', 'POST'])
@login_required
def follower():
    user = current_user
    followers = [1, 2, 3, 4, 5, 6]
    return render_template('user/follower.html', user=user,followers=followers)


@main.route('/index/explore', methods=['GET', 'POST'])
@login_required
def explore():
    user = current_user
    return render_template('explore/index.html', user=user)


@main.route('/index/pub_share', methods=['GET', 'POST'])
@login_required
def pub_share():
    user = current_user
    return render_template('user/pub_share.html', user=user)


@main.route('/index/pub_question', methods=['GET', 'POST'])
@login_required
def pub_question():
    user = current_user
    question_form = QuestionForm()
    if request.method == "POST":
        q_label = request.form.get('label')
        q_content = request.form.get('content')
        print(q_label)
        print(q_content)
        question = Question(label=q_label,
                            content=q_content,
                            writer=user)
        try:
            db.session.add(question)
            db.session.commit()
            flash("发布成功")
        except Exception as e:
            print(e)
            flash("发布失败")
            db.session.rollback()
    return render_template('user/pub_Q&A.html', user=user, question_form=question_form)


@main.route('/index/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user
    profile_form = ProfileForm()
    if profile_form.validate_on_submit():
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        realname = request.form.get('realname')
        gender = request.form.get('gender')
        age = request.form.get('age')
        school = request.form.get('school')
        selfinfo = request.form.get('selfinfo')
        test_user = User.query.filter_by(email=email).first()
        if test_user:
            flash('邮箱已被注册')
        else:
            # 丑陋的代码
            send_email(email, name)
            if email:
                user.email = profile_form.email.data
            if name:
                user.name = profile_form.name.data
            if password:
                user.password = profile_form.password.data
            if realname:
                user.realname = profile_form.realname.data
            if gender:
                user.gender = profile_form.gender.data
            if age:
                user.age = profile_form.age.data
            if school:
                user.school = profile_form.school.data
            if selfinfo:
                user.selfinfo = profile_form.selfinfo.data
            try:
                db.session.commit()
                flash("修改成功")
            except Exception as e:
                print(e)
                flash("发布失败")
                db.session.rollback()
    else:
        if request.method == "POST":
            flash("两次输入密码不一致 或 填写不合法")
    return render_template('user/edit_profile.html', user=user, form=profile_form)


@main.route('/index/delete_share/<uid>/<sid>', methods=['GET', 'POST'])
def delete_share(uid, sid):
    share = Share.query.get(sid)
    if share:
        try:
            db.session.delete(share)
            db.session.commit()
        except Exception as e:
            print(e)
            flash('删除分享出错')
            db.session.rollback()
    else:
        flash('没有这条分享')
    return redirect(url_for('main.index', uid=uid))


@main.route('/index/delete_question/<uid>/<qid>', methods=['GET', 'POST'])
def delete_question(uid, qid):
    question = Question.query.get(qid)
    if question:
        try:
            db.session.delete(question)
            db.session.commit()
        except Exception as e:
            print(e)
            flash('删除问题出错')
            db.session.rollback()
    else:
        flash('没有这条问题')
    return redirect(url_for('main.index', uid=uid))
