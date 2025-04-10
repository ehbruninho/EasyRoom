from flask import Flask, request,jsonify, Blueprint, render_template, redirect, url_for, flash
from datetime import datetime
from flask_login import current_user, login_required
from Controllers.payment_controllers import PaymentController
from Controllers.reserves_controllers import ReservasController

approved_reserves_bp = Blueprint('approved_reserves_bp', __name__, template_folder='templates')
@approved_reserves_bp.route('/reserve_approved', methods=['GET'])
@login_required
def reserve_approved():
    collection_id = request.args.get('collection_id') # Na produção essa informação é essencial
    payment_status = request.args.get('status')
    payment_id = request.args.get('payment_id')
    payment_type = request.args.get('payment_type')
    merchant_order_id = request.args.get('merchant_order_id') # Na produção essa informação é muito importante
    preference_id = request.args.get('preference_id')

    # Metodo criado para buscar o preference id no banco que esta nomeado como transition_id
    payment = PaymentController.get_by_Transition_id(preference_id)

    if not payment:
        print("Erro: Pagamento não encontrado.")
        return jsonify({'error': 'Pagamento não encontrado'}), 404

    #Aqui ele encontrou o preference_id e irá atualizar a tabela pagamento com as informações puxadas na URL
    update = PaymentController.att_payment(payment_status, payment_id, payment_type, preference_id)
    if not update:
        print("Erro: Falha ao atualizar pagamento.")
        return jsonify({'error': 'Erro ao atualizar pagamento.'}), 400

    # Depois de atualizar tabela de pagamento hora de atualizar a tabela reservas
    update_reserves = ReservasController.att_payments_reserves(update)

    #Criado objeto para enviar informações da reserva para o html
    check_reserve = ReservasController.get_reserve_by_id(update)
    if update_reserves:
        return render_template("approved_reserves.html", reserves=check_reserve)



