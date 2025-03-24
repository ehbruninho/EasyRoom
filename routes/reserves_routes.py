from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from Controllers.reserves_controllers import ReservasController
from Controllers.rooms_controllers import RoomController
from Controllers.plans_controllers import PlanesController
from Controllers.payment_controllers import PaymentController

from Models.plans import Planos
from datetime import datetime, timedelta

reserves_bp = Blueprint('reserves', __name__, template_folder='templates')

@reserves_bp.route('/create_reserves', methods=['GET', 'POST'])
@login_required
def create_reserves():
    rooms = RoomController.get_rooms()  # Obtém todas as salas
    plans = PlanesController.view_alll_plans()  # Obtém todos os planos

    if request.method == 'GET':
        return render_template('create_reserves.html', rooms=rooms, plans=plans)

    elif request.method == 'POST':
        try:

            room_id = request.form.get('room_id')
            date_init = datetime.strptime(request.form['date_init'].replace("T", " "), "%Y-%m-%d %H:%M")
            plan_id = request.form.get('plan_id')


            if not all([room_id, date_init, plan_id]):
                flash("Todos os campos são obrigatórios!", "danger")
                return redirect(url_for('reserves.create_reserves'))


            plan = PlanesController.view_plans_byId(plan_id)
            date_end = date_init + timedelta(hours=plan.duration)

            if date_end < date_init:
                flash("A data de término não pode ser menor do que a data de início!", "danger")
                return redirect(url_for('reserves.create_reserves'))


            new_reserve = ReservasController.create_reserve(current_user.id, room_id, date_init, date_end, plan_id)
            if not new_reserve:
                flash("Erro ao criar a reserva!", "danger")
                return redirect(url_for('reserves.create_reserves'))

            # Criar pagamento via Mercado Pago
            reserves_id = new_reserve[1]
            payment_data = PaymentController.create_payment(current_user.id, reserves_id, plan_id)


            if payment_data.get("payment_url"):
                return redirect(payment_data["payment_url"])  # Redireciona para a página de pagamento do Mercado Pago
            else:
                flash("Erro ao gerar pagamento!", "danger")
                return redirect(url_for('reserves.create_reserves'))

        except Exception as e:
            print(f"Erro: {e}")
            flash("Erro interno no servidor!", "danger")
            return redirect(url_for('reserves.create_reserves'))

@reserves_bp.route('/view_reserves', methods=['GET', 'POST'])
@login_required
def view_reserves():
    reserves = ReservasController.get_reserves(current_user.id)
    return render_template('view_reserves.html', reserves=reserves)


@reserves_bp.route('/get_available_rooms', methods=['GET'])
@login_required
def get_available_rooms():
    date_init = request.args.get('date_init')

    if not date_init:
        return jsonify({"error": "Campo obrigatório"}), 400

    date_init = datetime.strptime(date_init, "%Y-%m-%dT%H:%M")

    busy_rooms = ReservasController.get_reserves_by_date_range(date_init) #Busca todas salas ocupadas no periodo da data inicial
    all_rooms = RoomController.get_rooms() # Aqui busca todas salas registradas

    occupied_rooms_id = set ()

    for res in busy_rooms:
        get_plan_type = PlanesController.get_TotalTime_by_Id(res.plan_id)
        plan_duration = {"1h": 1, "2h": 2, "Turno": 4}
        block_hours = get_plan_type # Aqui conforme o resultado da busca pelo nome ele seta qual tempo de duração entre as reservas

        block_start = res.date_init - timedelta(hours=block_hours)
        block_end = res.date_init + timedelta(hours=block_hours)

        if block_start <= date_init <= block_end: #Compara se existe reservas no prazo do tempo total da reserva buscada
            occupied_rooms_id.add(res.room_id)

    available_rooms = []
    occupied_rooms = []

    for room in all_rooms:
        room_data = {"id": room.id, "name": room.name, "capacity": room.capacity}
        if room.id in occupied_rooms_id:
            occupied_rooms.append(room_data)
        else:
            available_rooms.append(room_data)

    return jsonify({"available_rooms": available_rooms, "occupied_rooms": occupied_rooms})