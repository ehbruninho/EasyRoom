from flask import session, redirect, url_for, flash
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_role' not in session or session['user_role'] != 'admin':
            flash('Acesso negado! Você não tem permissão para acessar essa pagina!', "danger")
            return redirect(url_for('user.login'))
        return f(*args, **kwargs)
    return decorated_function

