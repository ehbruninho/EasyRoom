from flask import Blueprint, render_template, request, redirect, url_for, flash
from Controllers.profile_controllers import ProfileController
from flask_login import login_required, current_user

profile_bp = Blueprint('profile', __name__, template_folder='templates')

@profile_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_profile():
    if request.method == 'POST':
        name = request.form.get('name')
        cpf = request.form.get('cpf')
        phone = request.form.get('phone')
        image = request.files.get('image')

        response = ProfileController.create_profile_ct(name, cpf, phone, image)

        if "error" in response:
            flash(response["error"], "danger")
            return redirect(url_for('profile.create_profile'))

        flash(response["success"], "success")
        return redirect(url_for('profile.view_profile'))

    return render_template('create_profile.html')

@profile_bp.route('/view', methods=['GET'])
@login_required
def view_profile():
    profile = Profile.view_profile(current_user.id)
    return render_template('view_profile.html', profile=profile)
