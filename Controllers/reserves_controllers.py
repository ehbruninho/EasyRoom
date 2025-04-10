from Models.reserves import Reservas, SessionLocal
from Models.payment import Pagamento


class ReservasController:

    @staticmethod
    def create_reserve(user_id, room_id, date_init, date_end, plan_id):
        if not all ([room_id,date_init,date_end,plan_id]):
            return {"error":"Todos campos são obrigatórios."}

        conflicts = Reservas.findReserves_by_Date(room_id,date_init, date_end)

        if conflicts:
            return {"error":"Já existe uma reserva nas datas informadas"}

        reserva = Reservas.create_reserves(user_id,room_id,date_init,date_end,plan_id)

        if reserva:
            return {"sucess":"Reserva efetuada com sucesso"}, reserva
        return {"error":"Erro ao registrar reserva"}

    @staticmethod
    def get_reserves(user_id):
        return Reservas.findReserves_by_Id(user_id)

    @staticmethod
    def get_reserves_by_date_range(date_init):
        return Reservas.findReserves_by_date_range(date_init)

    @staticmethod
    def att_payments_reserves(reserve_id):
        return Reservas.update_payment_reserve(reserve_id)

    @staticmethod
    def get_reserve_by_id(reserve_id):
        return Reservas.find_reserve_by_ReserveId(reserve_id)

    @staticmethod
    def att_reserves(reserve_id, date_init, date_end, room_id, plan_id, status):
        return Reservas.update_reserve(reserve_id, date_init, date_end, room_id, plan_id, status)

    @staticmethod
    def get_all_reserves():
        return Reservas.view_all_reserves()

    @staticmethod
    def delete_reserve(reserve_id):
        payment = Pagamento.delete_payment_by_Reserveid(reserve_id)
        reserve = Reservas.delete_reserve(reserve_id)
        if reserve and payment:
            return {"sucess":"Reserva deletada com sucesso"}
        return {"error":"Erro ao deletar reserva"}
