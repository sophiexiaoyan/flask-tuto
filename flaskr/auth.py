import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.models import User
from flaskr import db

# url_prefix will be prepended to all the URLs associated with the blueprint.
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # request.form is a special type of dict mapping submitted form keys and values.
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif User.query.filter(User.username==username).first() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            # For security, passwords should never be stored in the database directly.
            # generate_password_hash() is used to securely hash the password, and that hash is stored.
            user = User(username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        # flash() stores messages that can be retrieved when rendering the template.
        flash(error)
    # render_template() will render a template containing the HTML
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter(User.username==username).first()
        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password'

        if error is None:
            # session is a dict that stores data across requests.
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

# bp.before_app_request() registers a function that runs before the view function, no matter what URL is requested.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter(User.id==user_id).first()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# This decorator returns a new view function that wraps the original view it’s applied to.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            # When using a blueprint, the name of the blueprint is prepended to the name of the function,
            # so the endpoint for the login function is 'auth.login' because you added it to the 'auth' blueprint.
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
