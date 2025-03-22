from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash
from Controllers.reserves_controllers import ReservasController
from Controllers.rooms_controllers import RoomController
from Controllers.plans_controllers import PlanesController

from Models.plans import Planos
from datetime import datetime, timedelta

reserves_bp = Blueprint('reserves', __name__, template_folder='templates')

@reserves_bp.route('/create_reserves', methods=['GET', 'POST'])
@login_required
def create_reserves():
    rooms = RoomController.get_rooms() # Comando para pesquisar todas salas cadastradas
    plans = PlanesController.view_alll_plans()


    if request.method == 'POST':
        room_id = request.form.get('room_id')
        date_init = datetime.strptime(request.form['date_init'].replace("T", " "), "%Y-%m-%d %H:%M")
        plan_id = request.form.get('plan_id')

        plan = Planos.get_plan(plan_id)

        date_end = date_init + timedelta(hours=plan.duration)

        if date_end < date_init:
            flash('A data de término não pode ser menor do que á data de inicio','danger')
            return redirect(url_for('reserves.create_reserves'))

        response = ReservasController.create_reserve(current_user.id, room_id, date_init, date_end, plan_id)

        if "error" in response:
            flash(response['error'], "danger")
            return redirect(url_for('reserves.create_reserves'))

        flash ('Reserva efetuada com sucesso!', "success")
        return redirect(url_for('reserves.view_reserves'))

    return render_template('create_reserves.html', rooms=rooms, plans=plans)

@reserves_bp.route('/view_reserves', methods=['GET', 'POST'])
@login_required
def view_reserves():
    reserves = ReservasController.get_reserves(current_user.id)
    return render_template('view_reserves.html', reserves=reserves)




