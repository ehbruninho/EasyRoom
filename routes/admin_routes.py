from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from sqlalchemy.util import method_is_overridden
from Controllers.payment_controllers import PaymentController
from helpers.auth import admin_required
from Controllers.reserves_controllers import ReservasController
from Controllers.rooms_controllers import RoomController
from Controllers.plans_controllers import PlanesController
from datetime import datetime, timedelta
from Controllers.profile_controllers import ProfileController
from Controllers.price_controllers import PriceController


admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route("/dashboard")
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

@admin_bp.route("/adm_view_rooms")
@admin_required
def view_rooms():
    salas = RoomController.get_rooms_images()
    return render_template('adm_view_rooms.html', salas=salas)

@admin_bp.route("/adm_view_reserves", methods=['GET','POST'])
@admin_required
def view_reserves():
    reserves = ReservasController.get_all_reserves()

    payments = {}
    profile_dict = {}
    #Atualiza o dicionario cada vez que tiver outra inserção, para evitar clonar todas informações
    for reserve in reserves:
        payment = PaymentController.get_payment_by_Reserve_id(reserve.id)
        payments[reserve.id] = payment  # Associa o pagamento à reserva pelo ID
        profile = ProfileController.get_profile(reserve.user_id)
        profile_dict[reserve.user_id] = profile # Associa o perfil à reserva pelo ID

    return render_template('adm_view_reserves.html', reserves=reserves, payments=payments, profiles=profile_dict)

@admin_bp.route("/edit_reserve", methods=['GET','POST'])
@admin_required
def edit_reserves():

    if request.method == 'POST':
        reserve_id = request.form.get('reserve_id')
    else:
        reserve_id = request.args.get('reserve_id')

    price = PaymentController.get_payment_by_Reserve_id(reserve_id)
    rooms = RoomController.get_rooms()
    plans = PlanesController.view_alll_plans()

    reserve = ReservasController.get_reserve_by_id(reserve_id)

    if not reserve:
        flash("Reserva não encontrada!", "danger")
        return redirect(url_for('admin.view_reserves'))

    # Se 'reserves' for uma lista, pegamos o primeiro item
    if isinstance(reserve, list) and len(reserve) > 0:
        reserves = reserve[0]
    else:
        reserves = reserve  # Se já for um único objeto

    if request.method == 'POST':
        try:
            date_init_str  = request.form.get('date_init')
            room_id = request.form.get('room_id')
            plan_id = request.form.get('plan_id')
            date_end_str  = request.form.get('date_end')
            status = request.form.get('states')

            date_format = "%Y-%m-%dT%H:%M"
            date_init = datetime.strptime(date_init_str, date_format)
            date_end = datetime.strptime(date_end_str, date_format)


            amount_paid = PriceController.get_price_by_plan_id(plan_id)


            update_price = PaymentController.att_price_by_reserve_id(reserve_id, amount_paid)

            if update_price:
                flash("O valor da reserva foi alterado!", "success")

            if not date_init or not room_id or not plan_id or not status:
                flash("Dados inválidos!", "danger")
                return redirect(url_for('admin.edit_reserves'))

            updated = ReservasController.att_reserves(reserve_id, date_init, date_end, room_id, plan_id, status)

            if updated:
                flash("Reserva atualizada com sucesso!", "success")
                return redirect(url_for('admin.view_reserves'))

        except Exception as e:
            print(f"Erro ao atualizar reserva: {e}")
            return redirect(url_for('admin.view_reserves'))


    return render_template("edit_reserves.html", reserves=reserves, rooms=rooms, plans=plans, price=price)

@admin_bp.route("/delete_reserves", methods=['POST'])
@admin_required
def delete_reserve():

    reserve_id = request.form.get('reserve_id')
    reserve = ReservasController.delete_reserve(reserve_id)
    return redirect(url_for('admin.view_reserves'))



