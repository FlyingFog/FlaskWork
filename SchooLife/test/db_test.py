from app.models import User
from app import db
from app import models

session = db.session


class Test():
    def add(self):
        u1 = User("12345@qq.com","123",1)
        u2 = User("23456@qq.com","321",2)
        u3 = User("34567@qq.com","123",3)
        session.add_all([u1,u2,u3])
        session.commit()


    def change(self):
        u = User(login="123456@qq.com")
        u.PASSWORD = "123453"
        u.UID = 1
        u.NAME = "hhhh"
        session.add(u)
        session.commit()


    def changequery(self):
        l = User.query.filter(User.UID == 1).one()
        print(l.PASSWORD , l.UID)
        l.PASSWORD = "123456"
        session.commit()


    def delete(self):
        l = User.query.filter(User.UID == 3).one()
        session.delete(l)
        session.commit()

    def test(self):
        db.session.rollback()
        db.drop_all()
        db.create_all()

        u1 = models.User(email="u1@qq.com", username='u1', password=models.generate_password_hash("123"), confirmed=1)
        u2 = models.User(email="u2@qq.com", username='u2', password=models.generate_password_hash("123"), confirmed=1)
        u3 = models.User(email="u3@qq.com", username='u3', password=models.generate_password_hash("123"), confirmed=1)
        u4 = models.User(email="u4@qq.com", username='u4', password=models.generate_password_hash("123"), confirmed=1)
        u5 = models.User(email="u5@qq.com", username='u5', password=models.generate_password_hash("123"), confirmed=1)
        u6 = models.User(email="u6@qq.com", username='u6', password=models.generate_password_hash("123"), confirmed=1)
        u7 = models.User(email="u7@qq.com", username='u7', password=models.generate_password_hash("123"), confirmed=1)
        u8 = models.User(email="u8@qq.com", username='u8', password=models.generate_password_hash("123"), confirmed=1)
        u9 = models.User(email="u9@qq.com", username='u9', password=models.generate_password_hash("123"), confirmed=1)
        u2.follow(u1)
        u3.follow(u1)
        u4.follow(u1)
        u1.follow(u2)

        s1 = models.Share(label='u1-s1', content='u1-s1-content', writer=u1)
        s2 = models.Share(label='u1-s2', content='u1-s2-content', writer=u1)
        s3 = models.Share(label='u2-s1', content='u2-s1-content', writer=u2)
        s4 = models.Share(label='u2-s2', content='u2-s2-content', writer=u2)

        q1 = models.Question(label='u1-q1', content='u1-q1-content', writer=u1)
        q2 = models.Question(label='u1-q2', content='u1-q1-content', writer=u1)
        q3 = models.Question(label='u2-q1', content='u2-q1-content', writer=u2)
        q4 = models.Question(label='u2-q2', content='u2-q1-content', writer=u2)

        a1 = models.Answer(content="a1-content", writer=u2, question=q1)
        a2 = models.Answer(content="a2-content", writer=u2, question=q1)

        db.session.add_all([u1, u2, s1, s2, s3, s4, q1, q2, q3, q4])
        db.session.commit()
