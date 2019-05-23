from flask import Blueprint

auth = Blueprint("auth" ,__name__)

from . import views

# 表单类


"""

    db.drop_all()
    db.create_all()

    u1 = User(name='u1', password="123")
    u2 = User(name='u2', password="123")

    s1 = Share(label='u1-s1', writer=u1)
    s2 = Share(label='u1-s2', writer=u1)
    s3 = Share(label='u2-s1', writer=u2)
    s4 = Share(label='u2-s2', writer=u2)

    q1 = Question(label='u1-q1', writer=u1)
    q2 = Question(label='u1-q2', writer=u1)
    q3 = Question(label='u2-q1', writer=u2)
    q4 = Question(label='u2-q2', writer=u2)

    db.session.add_all([u1, u2, s1, s2, s3, s4, q1, q2, q3, q4])
    db.session.commit()

    app.run(debug=True)
"""