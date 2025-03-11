from flask import abort, session

from db import User

def auth_user(user):
    session['logged_in'] = True
    session['user_id'] = user.id
    session['username'] = user.username

def get_current_user():
    if session.get('logged_in'):
        return User.get(User.id == session['user_id'])

def check_user_logged_in():
     if not session.get('logged_in'):
        abort(403)