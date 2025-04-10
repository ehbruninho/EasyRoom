from Models.price import Preco

class PriceController:
    @staticmethod
    def create_price(cls,price,plan_id):
        price = Preco.create_price(price,plan_id)
        return price

    @staticmethod
    def get_price_by_plan_id(plan_id):
          return Preco.view_price(plan_id)

