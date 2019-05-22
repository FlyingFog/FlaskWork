from datetime import datetime
from app import db
import sqlite3
from config import basedir

conn = sqlite3.connect(basedir+'/flask.db')

class Follow(db.Model):
    __tablename__ = 'followinfo'

    followuid = db.Column(db.INT, db.ForeignKey('users.uid'),
                            primary_key=True)
    followeruid = db.Column(db.INT, db.ForeignKey('users.uid'),
                            primary_key=True)
    followtime = db.Column(db.DATETIME, default=datetime.utcnow)


class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.INT , primary_key=True)
    email = db.Column(db.VARCHAR(256))
    password = db.Column(db.VARCHAR(256))
    name = db.Column(db.VARCHAR(256))
    realname = db.Column(db.VARCHAR(256))
    portrait = db.Column(db.VARCHAR(256))
    permit = db.Column(db.INT, default=1)
    gender = db.Column(db.INT)
    age = db.Column(db.INT)
    school = db.Column(db.VARCHAR(256))
    selfinfo = db.Column(db.TEXT(65536))
    regtime = db.Column(db.DATETIME,default=datetime.utcnow)
    totshare = db.Column(db.INT,default=0)
    totques = db.Column(db.INT,default=0)
    totans = db.Column(db.INT,default=0)
    """
    Follower = db.relationship("Follow" , foreign_keys=[Follow.FollewerUID],
                               back_populates="FollewerUID")
    Following = db.relationship("Follow",foreign_keys=[Follow.FollowedUID],
                             back_populates="FollowedUID")
    """
    def __init__(self ,login):
        self.LOGIN = login

    def to_dict(self):
        return {c.name: getattr(self, c.name, None)
                for c in self.__table__.columns}




class Share(db.Model):
    __tablename__ = 'share'
    sid = db.Column(db.INT , primary_key=True)
    writeruid = db.Column(db.INT ,db.ForeignKey('users.uid'))
    label = db.Column(db.VARCHAR(256))
    image = db.Column(db.VARCHAR(256))
    content = db.Column(db.TEXT(65536))
    pubtime = db.Column(db.DATETIME,default=datetime.utcnow)
    newnum = db.Column(db.INT,default=0)
    star = db.Column(db.INT,default=0)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None)
                for c in self.__table__.columns}


class Comment(db.Model):
    __tablename__ = 'comment'
    cid = db.Column(db.INT, primary_key=True)
    sid = db.Column(db.INT ,db.ForeignKey('share.sid'))
    writerid = db.Column(db.INT ,db.ForeignKey('users.uid'))
    content = db.Column(db.TEXT(65536))
    pubtime = db.Column(db.DATETIME,default=datetime.utcnow)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None)
                for c in self.__table__.columns}


class Question(db.Model):
    __tablename__ = 'question'
	
    qid = db.Column(db.INT, primary_key=True)
    label = db.Column(db.VARCHAR(256))
    content = db.Column(db.TEXT(65536))
    writeruid = db.Column(db.INT,db.ForeignKey('users.uid'))
    newnum = db.Column(db.INT)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None)
                for c in self.__table__.columns}

class Answer(db.Model):
    __tablename__ = 'answer'
    aid = db.Column(db.INT, primary_key=True)
    qid = db.Column(db.INT, db.ForeignKey('question.qid'))
    content = db.Column(db.TEXT(65536))
    pubtime = db.Column(db.DATETIME , default=datetime.utcnow)


def creatDB():
    db.create_all()


def dropDB():
    db.drop_all()
