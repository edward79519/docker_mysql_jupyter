
from flask import render_template, session, redirect, url_for, current_app, request, flash
from . import main
from ..models import db

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/createdb', methods=['GET', 'POST'])
def createdb():
    db.create_all()
    return redirect(url_for("main.index"))

