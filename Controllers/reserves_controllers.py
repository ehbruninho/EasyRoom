from Models.reserves import Reservas, SessionLocal


class ReservasController:

    @staticmethod
    def create_reserve(user_id, room_id, date_init, date_end, plan_id):
        if not all ([room_id,date_init,date_end,plan_id]):
            return {"error":"Todos campos são obrigatórios."}

        reserva = Reservas.create_reserves(user_id,room_id,date_init,date_end,plan_id)
        if reserva:
            return {"sucess":"Reserva efetuada com sucesso"}
        return {"error":"Erro ao registrar reserva"}

    @staticmethod
    def get_reserves(user_id):
        return Reservas.findReserves_by_Id(user_id)


