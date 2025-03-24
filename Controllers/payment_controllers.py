import mercadopago
from Models.payment import Pagamento
from datetime import datetime
from Models.price import Preco
import os

class PaymentController:
    @staticmethod
    def create_payment(user_id, reserve_id, plan_id):
        sdk = mercadopago.SDK("TEST-630163749378952-032320-f8ad0b655782a1ccb1152937d6b6a63a-160920539")

        amount_paid = Preco.view_price(plan_id)

        payment_data = {

            "items": [
                {"id": "reserve_id",  "quantity": 1, "currency_id": "BRL", "unit_price": amount_paid ,"description": f"Reserva com plano {plan_id}"}
            ],
            "back_urls": {
                "success": "http://127.0.0.1:5000/compracerta",
                "failure": "http://127.0.0.1:5000/compraerrada",
                "pending": "http://127.0.0.1:5000/compraerrada",
            },
            "auto_return": "all"
        }

        result = sdk.preference().create(payment_data)

        if "id" in result["response"]:
            payment_url = result["response"]["init_point"]
            date_att = datetime.now()

            # Criar pagamento no banco com status "Pendente"
            new_payment = Pagamento.create_payment(
                user_id, reserve_id, plan_id, amount_paid, "Pendente", "Pix", date_att, result["response"]["id"]
            )


            return {"payment_url": payment_url}



        return {"error": "Erro ao criar pagamento no Mercado Pago"}
