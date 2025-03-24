from Models.plans import Planos

class PlanesController:
    @staticmethod
    def create(name,total_time, num_people, duration):
        if not all:
            return {"error":"Todos os campos são obrigatórios"}

        verif_plans = Planos.compare_plans(name,total_time,duration)
        if verif_plans:
            return {"error":"Esse plano ja foi registrado!"}

        plans = Planos.create_plan(name,total_time,num_people,duration)
        if plans:
            return {"sucess":"Plano registrado com sucesso."}

    @staticmethod
    def view_alll_plans():
       return  Planos.view_plans()

    @staticmethod
    def view_plans_byId(id):
        return Planos.findPlans_by_Id(id)

    @staticmethod
    def get_PlansName_by_Id(plan_id):
        return Planos.findPlansName_by_Id(plan_id)

    @staticmethod
    def get_TotalTime_by_Id(plan_id):
        return Planos.findTotalTime_by_Id(plan_id)

