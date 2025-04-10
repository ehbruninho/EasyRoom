from sqlalchemy import Column, Integer, Float, ForeignKey, String, DATETIME
from Models.base import Base, SessionLocal
from sqlalchemy.orm import relationship

class Pagamento(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    reserve_id = Column(Integer, ForeignKey('reserves.id'), nullable=False)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=False)
    amount_paid = Column(Float, nullable=False)
    states = Column(String(255), nullable=False)
    pay_met = Column(String, nullable=False)
    transition_id = Column(String(255), nullable=False)
    date_payed = Column(DATETIME, nullable=False)

    def __init__(self, user_id, reserve_id, plan_id, amount_paid, states, pay_met, date_payed,transition_id):
        self.user_id = user_id
        self.reserve_id = reserve_id
        self.plan_id = plan_id
        self.amount_paid = amount_paid
        self.states = states
        self.pay_met = pay_met
        self.date_payed = date_payed
        self.transition_id = transition_id

    # reserva = relationship("Reservas", back_populates="payment")

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

    @classmethod
    def view_payment_by_user_id(cls, user_id):
        session = SessionLocal()
        try:
            payment = session.query(Pagamento).filter_by(user_id=user_id).first()
            return payment
        except Exception as e:
            session.rollback()
            print(f"Erro ao buscar pagamento: {e}")
            return None
        finally:
            session.close()

    @classmethod
    def find_Transition_id(cls, preference_id):
        session = SessionLocal()
        try:
            pagamento = session.query(Pagamento).filter(Pagamento.transition_id == preference_id).first()
            return pagamento
        except Exception as e:
            session.rollback()
            print(f"Erro ao buscar pagamento: {e}")
            return None
        finally:
            session.close()

    @classmethod
    def update_payment(cls, status, payment_id, payment_type, preference_id):
        session = SessionLocal()
        try:
            payment = session.query(Pagamento).filter(Pagamento.transition_id == preference_id).first()

            if not payment:
                print(f"Erro: Pagamento com transition_id={payment_id} não encontrado.")
                return False

            print(f"Atualizando pagamento {payment.id} para status {status.capitalize()} com método {payment_type}")

            payment.states = status.capitalize()
            payment.pay_met = payment_type
            session.commit()
            return payment.reserve_id
        except Exception as e:
                session.rollback()
                print(f"Erro ao atualizar pagamento: {e}")
                return False
        finally:
            session.close()

    @classmethod
    def update_payment_by_reserve_id(cls,reserve_id,amount_paid):
        session = SessionLocal()
        try:
            payment = session.query(Pagamento).filter(Pagamento.reserve_id == reserve_id).first()

            if not payment:
                print(f"Erro: Pagamento da Reserva={reserve_id} não encontrado.")

            payment.amount_paid = amount_paid
            session.commit()
            return True

        except Exception as e:
            session.rollback()
            print(f"Erro ao atualizar pagamento: {e}")
            return False
        finally:
            session.close()

    @classmethod
    def find_payment_by_idReserve(cls,reserve_id):
        session = SessionLocal()
        try:
            payment = session.query(Pagamento).filter(Pagamento.reserve_id == reserve_id).first()
            return payment
        except Exception as e:
            print(f"Erro ao buscar pagamento: {e}")
            session.rollback()
            return None
        finally:
            session.close()
    @classmethod
    def delete_payment_by_Reserveid(cls,reserve_id):
        session = SessionLocal()
        try:
            payment = session.query(Pagamento).filter(Pagamento.reserve_id == reserve_id).first()
            session.delete(payment)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Erro ao deletar pagamento: {e}")
            return False
        finally:
            session.close()