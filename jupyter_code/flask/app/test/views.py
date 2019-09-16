
from flask import current_app, render_template, redirect, request, url_for, flash
from flask_login import login_user as flask_login_user
from flask_login import logout_user, login_required, current_user, fresh_login_required

from . import test

@test.route('/testlogin', methods=['GET', 'POST'])
@login_required
def test_login():
    return render_template('test/test.html')
