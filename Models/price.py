from sqlalchemy import Float, Integer, Column, String, ForeignKey
from Models.base import Base, SessionLocal

class Preco(Base):
    __tablename__ = 'price'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    price = Column(Float, nullable=False)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=False)

    def __init__(self, price, plan_id):
        self.price = price
        self.plan_id = plan_id
    @classmethod
    def create_price(cls,price,plan_id):
        session = SessionLocal()
        try:
            price = Preco(price,plan_id)
            session.add(price)
            session.commit()
            return price
        except Exception as e:
            session.rollback()
            print(f"Erro ao adicionar preços! Error: {e}")
        finally:
            session.close()




