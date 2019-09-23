from flask_admin import BaseView, expose
from flask import render_template
from flask_login import current_user
from .models import *
from flask_admin.contrib.sqla import ModelView


class AdminView(ModelView):
    # @expose("/")
    # def index(self):
    #    return self.render('admin.html')
    def is_accessible(self):
        return current_user.is_administrator()

    def __init__(self, model, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(AdminView, self).__init__(model, session, **kwargs)


def create_admin_view(adm, db):
    adm.add_view(AdminView(User, db.session, endpoint="admUser"))
