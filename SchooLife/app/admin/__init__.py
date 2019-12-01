from flask_admin import Admin
from app.models import User
from flask_admin.contrib.sqla import ModelView
from app import db
admin = Admin(name='内容管理', template_mode='bootstrap3')

class UserModelView(ModelView):
    page_size = 50
    column_exclude_list = ['password','confirmed','has_img','portrait','selfinfo','totshare'
                          ,'totques','totans']
    column_editable_list = ['permit']
    form_choices = {
        'permit':[
            ('1','允许'),('0','不允许')]
    }

admin.add_view(UserModelView(User,db.session,name="用户管理"))