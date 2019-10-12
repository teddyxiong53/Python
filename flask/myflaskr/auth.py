import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    pass

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'username is required'
        elif not password:
            error = 'password is required'
        elif db.execute('select id from user where username= ?', (username,)).fetchone() is not None:
            error = "user {} is already exists".format(username)

        if error is None:
            db.execute('insert into user (username, password) values (?,?)', (username, generate_password_hash(password)))
            db.commit()
            return redirect(url_for('auth.login'))
        flash(error)

    # get method
    return render_template('auth/register.html')

@bp.route('/login', methods=('get', 'post'))
def login():
    if request.method == 'post':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute('select * from user where username=?', (username,)).fetchone()
        if user is None:
            error = 'incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


