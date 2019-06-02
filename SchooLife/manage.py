from app import create_app, db
from app import models

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # db.session.rollback()
        # db.drop_all()
        # db.create_all()

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


        s1 = models.Share(label='u1-s1', writer=u1)
        s2 = models.Share(label='u1-s2', writer=u1)
        s3 = models.Share(label='u2-s1', writer=u2)
        s4 = models.Share(label='u2-s2', writer=u2)

        q1 = models.Question(label='u1-q1', writer=u1)
        q2 = models.Question(label='u1-q2', writer=u1)
        q3 = models.Question(label='u2-q1', writer=u2)
        q4 = models.Question(label='u2-q2', writer=u2)

        db.session.add_all([u1, u2, s1, s2, s3, s4, q1, q2, q3, q4])
        db.session.commit()

        app.run(debug=True)
