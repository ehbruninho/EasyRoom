from Models import User
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask import Bcrypt

bcrypt = Bcrypt()
user = Blueprint('user', __name__)

def login():
    return

def create_user(name, email, password):
    user = User.check_user(email)
    if not user:
        User.create_user(name, email, password)
        return True
    if user:
        return False

def login_user(email, password):
    user = User.login_user(email,password)
    if user:
        return True
    return False

def logout_user():
    return