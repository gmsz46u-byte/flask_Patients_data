from flask import Blueprint
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_admin import AdminIndexView
from Urology_app import db,admin,bcrypt
from Urology_app.models import Admindb,Patient,deletedPatient

adminbp = Blueprint("adminbp",__name__)

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1
    
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1


class UserModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')


    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == 1


admin.add_view(UserModelView(Admindb,db.session))
admin.add_view(MyModelView(Patient,db.session))
admin.add_view(MyModelView(deletedPatient,db.session))