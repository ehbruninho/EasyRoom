from flask import session, request
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request or 'user_role' not in session or session.get('user_role') != 'admin':
            return "Acesso negado", 403  # Ou redirecionar para a página de login
        return f(*args, **kwargs)

    return decorated_function