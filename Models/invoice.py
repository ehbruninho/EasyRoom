from sqlalchemy import Column, Integer, String, Float, Enum, Date, ForeignKey, Table, create_engine
from Models.base import Base, SessionLocal

class Fatura(Base):
    __tablename__ = 'invoices'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=False)
    ammount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)
    states = Column(Enum("Pendente","Pago","Vencido"), nullable=False)

    def __init__(self, user_id, plan_id, ammount, due_date, states):
        self.user_id = user_id
        self.plan_id = plan_id
        self.ammount = ammount
        self.due_date = due_date
        self.states = states


    @classmethod
    def create_invoice(cls, user_id, plan_id, ammount, due_date, states):
        session = SessionLocal()
        try:
            invoice = Fatura(user_id, plan_id, ammount, due_date, states)
            session.add(invoice)
            session.commit()
            return invoice

        except Exception as e:
            session.rollback()
            print(f"Erro ao registrar fatura! Erro: {e}")
        finally:
            session.close()