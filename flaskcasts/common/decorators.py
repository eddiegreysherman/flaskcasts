from functools import wraps
from flask import session, redirect, request, flash, url_for


def requires_login(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        if 'user_id' not in session.keys() or session['user_id'] is None:
            flash("You need to be logged in to access this section.", 'danger')
            return redirect(url_for('home.login', next=request.path))  # sends back to edit after login

        return func(*args, **kwargs)

    return decorated_func
