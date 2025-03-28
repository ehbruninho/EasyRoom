import random

from Models.users import User
from flask_login import login_user, logout_user
import random

class UserController:
    @staticmethod
    def register_user(email, password):
        if not all([email, password]):
            return {"error": "Todos os campos são obrigatórios!"}

        if len(password) < 8:
            return {"error": "A senha deve ter pelo menos 8 caracteres."}

        exist_user = User.check_user(email)
        if exist_user:
            return {"error": "Usuário já existe."}

        token = random.randint(10000000,99999999)
        user = User.create_user(email, password,token)
        if user:
            return {"success": "Usuário cadastrado com sucesso!"}
        return {"error": "Erro ao cadastrar usuário!"}

    @staticmethod
    def login_user(email, password):
        user = User.login(email, password)
        if user:
            login_user(user)
            return {"success": "Login realizado com sucesso!", 'user_role': user.user_role}
        return {"error": "Usuário ou senha incorretos!"}

    @staticmethod
    def logout_user():
        logout_user()
        return {"success": "Logout realizado com sucesso!"}
