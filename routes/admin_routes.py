from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from helpers.auth import admin_required

admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route("/dashboard")
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html')