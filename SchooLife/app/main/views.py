from flask import render_template, redirect, url_for, request, flash, current_app
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


@main.route('/index/shares/', methods=['GET', 'POST'])
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


@main.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    current_user.follow(user)
    return render_template('user/index.html', user=user)


@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    current_user.unfollow(user)
    return render_template('user/index.html', user=user)


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    current_user.follow(user)
    return render_template('followers.html', user=user)


@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)


@main.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    print('------------------')
    print(username)
    print(user)
    return render_template('user/index.html', user=user)


@main.route('/index/<username>/shares', methods=['GET', 'POST'])
@login_required
def shares(username):
    user = User.query.filter_by(username=username).first()
    shares = user.shares
    return render_template('user/index.html', user=user, shares=shares)


@main.route('/index/<username>/QandAs', methods=['GET', 'POST'])
@login_required
def QandAs(username):
    user = User.query.filter_by(username=username).first()
    questions = user.questions
    return render_template('user/Q&As.html', user=user, questions=questions)


@main.route('/index/<username>/following', methods=['GET', 'POST'])
@login_required
def following(username):
    user = User.query.filter_by(username=username).first()
    followings = user.followed
    return render_template('user/following.html', user=user, followings=followings)


@main.route('/index/<username>/follower', methods=['GET', 'POST'])
@login_required
def follower(username):
    user = User.query.filter_by(username=username).first()
    followers = user.followers
    return render_template('user/follower.html', user=user, followers=followers)


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
