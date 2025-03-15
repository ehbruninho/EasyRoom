from sqlalchemy import Column, Integer, Float, Enum, ForeignKey, String, Date
from Models.base import Base, SessionLocal

class Pagamento(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    reserve_id = Column(Integer, ForeignKey('reserves.id'), nullable=False)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=False)
    amount_paid = Column(Float, nullable=False)
    states = Column(Enum("Pendente","Aprovado","Recusado"), nullable=False)
    pay_met = Column(Enum("Pix","Boleto","Cartao"), nullable=False)
    transition_id = Column(String(255), nullable=False)
    date_payed = Column(Date, nullable=False)

    def __init__(self, user_id, reserve_id, plan_id, amount_paid, states, pay_met, date_payed,transition_id):
        self.user_id = user_id
        self.reserve_id = reserve_id
        self.plan_id = plan_id
        self.amount_paid = amount_paid
        self.states = states
        self.pay_met = pay_met
        self.date_payed = date_payed
        self.transition_id = transition_id

    @classmethod
    def create_payment(cls,user_id, reserve_id, plan_id, amount_paid, states, pay_met, date_payed,transition_id):
        session = SessionLocal()
        try:
            payment = Pagamento(user_id, reserve_id, plan_id, amount_paid, states, pay_met, date_payed,transition_id)
            session.add(payment)
            session.commit()
            return payment

        except Exception as e:
            session.rollback()
            print(f"Erro ao cadastrar pagamento!Erro: {e}")

        finally:
            session.close()
