# coding=utf-8

from datetime import datetime

from . import app
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from urllib import parse


class Follow(db.Model):
    __tablename__ = 'followinfo'

    followuid = db.Column(db.INT, db.ForeignKey('users.id'),
                          primary_key=True)
    followeruid = db.Column(db.INT, db.ForeignKey('users.id'),
                            primary_key=True)
    followtime = db.Column(db.DATETIME, default=datetime.utcnow)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.INT, primary_key=True)
    email = db.Column(db.VARCHAR(256))
    password = db.Column(db.VARCHAR(512))
    confirmed = db.Column(db.BOOLEAN, default=False)
    username = db.Column(db.VARCHAR(256))
    realname = db.Column(db.VARCHAR(256))
    has_img = db.Column(db.INT, default=0)
    portrait = db.Column(db.VARCHAR(256))
    permit = db.Column(db.INT, default=1)
    gender = db.Column(db.INT)
    age = db.Column(db.INT)
    school = db.Column(db.VARCHAR(255))
    selfinfo = db.Column(db.TEXT(65535))
    regtime = db.Column(db.DATETIME, default=datetime.utcnow)
    totshare = db.Column(db.INT, default=0)
    totques = db.Column(db.INT, default=0)
    totans = db.Column(db.INT, default=0)
    has_img = db.Column(db.BOOLEAN, default=0)

    shares = db.relationship('Share', backref='writer')
    questions = db.relationship('Question', backref='writer')

    """
    follower = db.relationship("Follow" , foreign_keys=[Follow.FollewerUID],
                               back_populates="FollewerUID")
    following = db.relationship("Follow", foreign_keys=[Follow.FollowedUID],
                                back_populates="FollowedUID")
    """

    def to_dict(self):
        return {c.name: getattr(self, c.name, None)
                for c in self.__table__.columns}

    def generate_password(self, pwd):
        self.password = generate_password_hash(pwd)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def generate_confirmation_token(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in=3600)
        token = s.dumps({'uid': self.id})
        print(token)
        return token

    def confirm(self, token):
        s = Serializer(app.config['SECRET_KEY'], expires_in=3600)
        token = token[2:-1]
        print(token)
        try:
            data = s.loads(token)
        except:
            print('datafalse')
            return False
        if data.get('uid') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Share(db.Model):
    __tablename__ = 'share'
    sid = db.Column(db.INT, primary_key=True)
    writeruid = db.Column(db.INT, db.ForeignKey('users.id'))
    label = db.Column(db.VARCHAR(256))
    image = db.Column(db.VARCHAR(256))
    content = db.Column(db.TEXT(65536))
    pubtime = db.Column(db.DATETIME, default=datetime.utcnow)
    newnum = db.Column(db.INT, default=0)
    star = db.Column(db.INT, default=0)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None)
                for c in self.__table__.columns}


class Comment(db.Model):
    __tablename__ = 'comment'
    cid = db.Column(db.INT, primary_key=True)

    sid = db.Column(db.INT, db.ForeignKey('share.sid'))
    writerid = db.Column(db.INT, db.ForeignKey('users.id'))
    content = db.Column(db.TEXT(65536))
    pubtime = db.Column(db.DATETIME, default=datetime.utcnow)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None)
                for c in self.__table__.columns}


class Question(db.Model):
    __tablename__ = 'question'

    qid = db.Column(db.INT, primary_key=True)

    label = db.Column(db.VARCHAR(256))
    content = db.Column(db.TEXT(65536))
    writeruid = db.Column(db.INT, db.ForeignKey('users.id'))
    newnum = db.Column(db.INT)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None)
                for c in self.__table__.columns}


class Answer(db.Model):
    __tablename__ = 'answer'
    aid = db.Column(db.INT, primary_key=True)
    qid = db.Column(db.INT, db.ForeignKey('question.qid'))
    content = db.Column(db.TEXT(65535))
    pubtime = db.Column(db.DATETIME, default=datetime.utcnow)


def creatDB():
    db.create_all()


def dropDB():
    db.drop_all()
