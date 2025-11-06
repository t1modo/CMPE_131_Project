from flask import Blueprint, render_template
from app.forms import LoginForm
from datetime import datetime
from app.models import User

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return

@main.route('/calling_db')
def calling_db():
    users = User.query.first()
    return str(users)

@main.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)