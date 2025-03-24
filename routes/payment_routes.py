from flask import Blueprint, request, jsonify
from Controllers.payment_controllers import PaymentController

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/create_payment', methods=['POST'])
def create_payment():
    data = request.json
    reserve_id = data.get('reserve_id')
    title = data.get('title')
    amount = data.get('amount')

    if not all([reserve_id, title, amount]):
        return jsonify({"error": "Dados incompletos"}), 400

    payment_url = PaymentController.make_payment(reserve_id, title, amount)
    return jsonify({"payment_url": payment_url})