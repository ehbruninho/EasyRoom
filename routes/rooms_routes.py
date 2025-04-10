from flask import Blueprint, render_template, request, redirect, url_for, flash
from Controllers.rooms_controllers import RoomController, Salas
from flask_login import login_required, current_user

from helpers.auth import admin_required

rooms_bp = Blueprint('rooms_bp', __name__, template_folder='templates')

@rooms_bp.route('/create_room', methods=['GET', 'POST'])
@login_required
def create_room():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        capacity = int(request.form.get('capacity',0))
        disp = True if request.form.get('disp') == "1" else False
        type = request.form.get('room_type')
        local = request.form.get('local')
        foto = request.files.get('foto')

        response = RoomController.create_room(name, description, capacity, disp, type, local, foto)

        if "error" in response:
            flash(response["error"], "danger")
            return redirect(url_for('rooms_bp.create_room'))

        flash(response["success"], "success")
        return redirect(url_for('rooms_bp.view_rooms'))

    return render_template('create_room.html')

@rooms_bp.route('/view_rooms', methods=['GET'])
@login_required
def view_rooms():
    salas = RoomController.get_rooms_images()
    return render_template('view_rooms.html', salas=salas)


