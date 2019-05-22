from app.models import User
from app import db

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

l = User.query.filter(User.UID == 1).one()
print(l.uid)
