from flask import render_template, request, redirect, session, url_for, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import User
from .utils import user_id

auth = Blueprint('auth', __name__)



# registration page
@auth.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        if username == '' or password == '':
            return render_template('register.html', message='Please include a name and/or password.')

        # check no one else has that username
        if db.session.query(User).filter(User.username == username).count() == 0:
            user = User(username, password, password_hash)
            db.session.add(user)
            db.session.commit()
            session['username'] = user.username
            session['user_id'] = user_id(session.get('username'))
            return redirect(url_for('main.get_profile'))
        else:
            return render_template('register.html', message='Sorry, this username is already taken.')

    else:
        return render_template('register.html')


# sign-in page
@auth.route('/sign-in', methods=["GET", "POST"])
def sign_in():
    if request.method == 'POST':
        username_entered = request.form['username']
        password_entered = request.form['password']
        user = db.session.query(User).filter(User.username == username_entered).first()
        if user is not None and check_password_hash(user.password_hash, password_entered):
            session['username'] = user.username
            session['user_id'] = user_id(session.get('username'))
            return redirect(url_for('main.get_profile'))
        return render_template('signin.html',
                               message="Sorry, either your username does not exist or your password does not match.")
    else:
        return render_template('signin.html')


# sign-out page
@auth.route('/sign-out', methods=["GET", "POST"])
def sign_out():
    if request.method == 'POST':
        session.pop('username', None)
        return redirect(url_for('auth.sign_in'))
    else:
        return render_template('signout.html')
