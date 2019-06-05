import os

from flask import render_template, redirect, url_for, request, flash, current_app
from . import main
from .. import db
from ..models import User, Share, Question, Answer, Comment
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
    return render_template('user/index.html', user=user)


@main.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    current_user.follow(user)
    db.session.commit()
    return render_template('user/index.html', user=user)


@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    current_user.unfollow(user)
    db.session.commit()
    return render_template('user/index.html', user=user)


@main.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    return render_template('user/index.html', user=user)


@main.route('/index/<username>/shares', methods=['GET', 'POST'])
@login_required
def shares(username):
    user = User.query.filter_by(username=username).first()
    shares = user.shares
    return render_template('user/share_index.html', user=user, shares=shares)


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


@main.route('/index/explore/share', methods=['GET', 'POST'])
@login_required
def explore():
    users = current_user.followed
    shares = []
    for user in users:
        for share in user.followed.shares:
            shares.append(share)
    return render_template('explore/share.html', shares=shares)


@main.route('/index/explore/question', methods=['GET', 'POST'])
@login_required
def explore_question():
    users = current_user.followed
    questions = []
    for user in users:
        for question in user.followed.questions:
            questions.append(question)
    return render_template('explore/Q&A.html', questions=questions)


@main.route('/index/look_question/<qid>', methods=['GET', 'POST'])
@login_required
def look_question(qid):
    question = Question.query.get(qid)
    return render_template('explore/look_question.html', question=question)


@main.route('/index/show_share/<sid>', methods=['GET', 'POST'])
@login_required
def show_share(sid):
    share = Share.query.get(sid)
    return render_template('explore/show_share.html', share=share)


@main.route('/index/search/<search>/<category>', methods=['GET', 'POST'])
@login_required
def search2(search, category):
    searchWhat = '%' + search + '%'
    print(search)
    print(type(search))
    print(category)
    print(type(category))
    print('---------------')
    if category == "share":
        shares = Share.query.filter(Share.content.like(searchWhat)).all()
        print(shares)
        return render_template('search/index.html', results=shares, search=search)

    elif category == "question":
        questions = Question.query.filter(Question.content.like(searchWhat)).all()
        print(questions)
        return render_template('search/question.html', results=questions, search=search)

    elif category == "user":
        users = User.query.filter(User.username.like(searchWhat)).all()
        print(users)
        return render_template('search/user.html', results=users, search=search)
    else:
        print("---------search something wrong---------------")
    return render_template('search/index.html')


@main.route('/index/search/share', methods=['GET', 'POST'])
@login_required
def search1():
    if request.method == "POST":
        search = request.form.get('search')
        print('----search1----')
        print(search)
        print(type(search))
        searchWhat = '%' + search + '%'
        shares = Share.query.filter(Share.content.like(searchWhat)).all()
        # print(url_for('main.search2',search="search", category="share"))
        return render_template('search/index.html', results=shares, search=search)
    return render_template('search/index.html')


@main.route('/index/pub_share', methods=['GET', 'POST'])
@login_required
def pub_share():
    user = current_user
    share_form = ShareForm()
    if request.method == "POST":
        s_label = request.form.get('label')
        s_content = request.form.get('content')
        share = Share(label=s_label,
                      content=s_content,
                      writer=user)
        try:
            db.session.add(share)
            db.session.commit()
            if s_content != "":
                # 存图片
                if share_form.image.data:
                    print(share.sid)
                    share.image = str("/static/share_images/"+str(share.sid)+".png")
                    db.session.commit()
                    basedir = os.path.abspath(os.path.dirname(__file__))
                    f = request.files['image']
                    postfix = str(f.filename).split('.')[1]
                    image_name = str(share.sid) + '.' + postfix
                    f.save(os.path.join(os.path.join(basedir, '..', 'static', 'share_images'), image_name))
            return redirect(url_for('main.index'))
        except Exception as e:
            print(e)
            db.session.rollback()
    return render_template('user/pub_share.html', user=user, share_form=share_form)


@main.route('/index/pub_question', methods=['GET', 'POST'])
@login_required
def pub_question():
    user = current_user
    question_form = QuestionForm()
    if request.method == "POST":
        q_label = request.form.get('label')
        q_content = request.form.get('content')
        # print(q_label)
        # print(q_content)
        question = Question(label=q_label,
                            content=q_content,
                            writer=user)
        try:
            if q_label != "":
                db.session.add(question)
                db.session.commit()
            return redirect(url_for('main.index'))
        except Exception as e:
            print(e)
            db.session.rollback()
    return render_template('user/pub_question.html', user=user, question_form=question_form)


@main.route('/index/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user
    profile_form = ProfileForm()
    if request.method == "POST":
        name = request.form.get('name')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        gender = request.form.get('gender')
        age = request.form.get('age')
        school = request.form.get('school')
        selfinfo = request.form.get('selfinfo')
        # print(name, password, gender, age, school, selfinfo)

        if password != password2:
            flash('两次输入密码不一致')
        else:
            test_user_name = User.query.filter_by(username=name).first()
            if test_user_name:
                flash('用户名已被使用')
            else:
                if name:
                    user.username = name
                if password:
                    user.password = password
                if gender:
                    user.gender = gender
                if age:
                    user.age = age
                if school:
                    user.school = school
                if selfinfo:
                    user.selfinfo = selfinfo
                try:
                    db.session.commit()
                    # flash("修改成功")
                    return redirect(url_for('main.index'))
                except Exception as e:
                    print(e)
                    flash("发布失败")
                    db.session.rollback()
    return render_template('user/edit_profile.html', form=profile_form)


@main.route('/index/delete_share/<sid>', methods=['GET', 'POST'])
def delete_share(sid):
    share = Share.query.get(sid)
    db.session.delete(share)
    db.session.commit()
    return redirect(url_for('main.index'))


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


@main.route('/index/explore/like_share/<sid>', methods=['GET', 'POST'])
@login_required
def like_share(sid):
    share = Share.query.get(sid)
    share.like += 1
    db.session.commit()
    return render_template('explore/show_share.html', share=share)


@main.route('/index/explore/like_comment/<cid>', methods=['GET', 'POST'])
@login_required
def like_comment(cid):
    comment = Share.query.get(cid)
    comment.like += 1
    db.session.commit()
    return render_template('explore/show_share.html', share=comment.share)


@main.route('/index/explore/like_answer/<aid>', methods=['GET', 'POST'])
@login_required
def like_answer(aid):
    answer = Answer.query.get(aid)
    answer.like += 1
    db.session.commit()
    return render_template('explore/look_question.html', question=answer.question)


@main.route('/index/explore/pub_comment/<sid>', methods=['GET', 'POST'])
@login_required
def pub_comment(sid):
    share = Share.query.get(sid)
    if request.method == "POST":
        comment_content = request.form.get('content')
        comment = Comment(content=comment_content, share=share,writer=current_user)
        db.session.add(comment)
        db.session.commit()
    return render_template('explore/show_share.html', share=share)



@main.route('/index/explore/question/pub_answer/<qid>', methods=['GET', 'POST'])
@login_required
def pub_answer(qid):
    user = current_user
    question = Question.query.get(qid)
    if request.method == "POST":
        answer_content = request.form.get('content')
        answer = Answer(content=answer_content, writer=user, question=question)
        try:
            db.session.add(answer)
            db.session.commit()
            return render_template('explore/look_question.html', question=question)
        except Exception as e:
            print(e)
            db.session.rollback()
    return render_template('explore/look_question.html', question=question)
