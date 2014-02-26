"""
Helper functions for views in serve.py
"""

from flask import session, redirect, url_for
from functools import wraps
import json

# Decorator that checks whether user is already logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('root'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator that checks whether user is already logged in but return json message
def ajax_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return json.dumps({'status': 'error', 'message': 'You are not logged in'})
        return f(*args, **kwargs)
    return decorated_function

# Helper function for submit() that processes data into dicts
def build_data_dict(keys, form):
    data_dict = {}
    for key in keys:
        if key in form:
            data_dict[key] = form.get(key)
        else:
            data_dict[key] = ''
    return data_dict

