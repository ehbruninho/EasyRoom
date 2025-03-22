from flask import Blueprint, render_template, redirect, url_for, request, flash
from Controllers.users_controllers import UserController
from flask_login import login_required
from routes.main_routes import menu

user_bp = Blueprint('user', __name__, template_folder='templates')

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        response = UserController.register_user(
            request.form.get('email'),
            request.form.get('password')
        )

        if "error" in response:
            flash(response["error"], "danger")
            return redirect(url_for('user.register'))

        flash(response["success"], "success")
        return redirect(url_for('user.login'))

    return render_template('register.html')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        response = UserController.login_user(
            request.form.get('email'),
            request.form.get('password')
        )

        if "error" in response:
            flash(response["error"], "danger")
            return redirect(url_for('user.login'))

        flash(response["success"], "success")
        return redirect(url_for('main.menu'))  # Altere para a rota desejada

    return render_template('login.html')

@user_bp.route('/logout')
@login_required
def logout():
    response = UserController.logout_user()
    flash(response["success"], "success")
    return redirect(url_for('user.login'))
