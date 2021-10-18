from flask import Blueprint, redirect, url_for
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from flaskapp import db, admin
from flaskapp import models

beheer = Blueprint('beheer', __name__)


class MyModelView(ModelView):
    column_list = ('username', 'email', 'roles')
    # column_exclude_list = ('password')


admin.add_view(MyModelView(models.User, db.session))  # admin views
admin.add_view(ModelView(models.Role, db.session))

# admin.add_view(ModelView(dwmodels.Vullingsgraad, db.session))
# admin.add_view(ModelView(dwmodels.Trainingsgraad, db.session))
