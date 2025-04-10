from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME, Enum, and_
from sqlalchemy.orm import relationship, joinedload
from Models.base import Base, SessionLocal
from datetime import timedelta


class Reservas(Base):
    __tablename__ = 'reserves'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'),nullable=False)
    date_init = Column(DATETIME, nullable=False)
    date_end = Column(DATETIME, nullable=False)
    states = Column(Enum("Pendente","Confirmada","Cancelada"),default="Pendente",nullable=False)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=False)

    room = relationship("Salas",  backref="reserves")
    plan = relationship("Planos", backref="reserves")
    payment = relationship("Pagamento", backref="reserves", overlaps="reserves")


    def __init__(self, user_id, room_id, date_init, date_end,plan_id):
        self.user_id = user_id
        self.room_id = room_id
        self.date_init = date_init
        self.date_end = date_end
        self.plan_id = plan_id

    @classmethod
    def create_reserves(cls, user_id, room_id, date_init, date_end,plan_id):
        session = SessionLocal()
        try:
            reserves = Reservas(user_id,room_id,date_init,date_end,plan_id)
            session.add(reserves)
            session.commit()
            return reserves.id
        except Exception as e:
            session.rollback()
            print(f"Erro ao registrar reserva! Error: {e}")
        finally:
            session.close()

    @classmethod
    def findReserves_by_Id(cls, user_id):
        session = SessionLocal()
        try:
            reserves = session.query(Reservas).options(joinedload(Reservas.room), joinedload(Reservas.plan)).filter_by(user_id=user_id).all()
            return reserves
        except Exception as e:
            print(f"Erro ao realizar consulta! Error: {e}")
        finally:
            session.close()

    @classmethod
    def findReserves_by_Date(cls, room_id,date_init, date_end):
        session = SessionLocal()
        try:
            reserves = session.query(Reservas).filter(Reservas.room_id == room_id, Reservas.states == "Pago",
            and_(
                Reservas.date_init < date_end,
                Reservas.date_end > date_init
            )
        ).first()
            return reserves
        except Exception as e:
            print(f"Erro ao realizar consulta! Error: {e}")
        finally:
            session.close()

    @classmethod
    def findReserves_by_date_range(cls,date_init):
        session = SessionLocal()
        try:
                reserves = session.query(Reservas).filter(Reservas.states == "Pago",
                                                          Reservas.date_init <= date_init + timedelta(hours=4),
                                                          Reservas.date_end >= date_init - timedelta(hours=4)).all()
                return reserves # Retornará somente id das salas com status de pago
        except Exception as e:
            session.rollback()
            print(f"Erro ao realizar consulta! Error: {e}")
            return []

        finally:
            session.close()

    @classmethod
    def update_payment_reserve(cls, reserve_id):
        session = SessionLocal()
        try:
            update = session.query(Reservas).filter_by(id=reserve_id).first()
            if update:
                update.states = "Pago"
                session.commit()
                return True
            else:
                return False
        except Exception as e:
            session.rollback()
            print(f'Erro ao atualizar reserva: {e}')
            return False
        finally:
            session.close()

    @classmethod
    def find_reserve_by_ReserveId(cls, reserve_id):
        session = SessionLocal()
        try:
            reserves = (
                session.query(Reservas)
                .options(
                    joinedload(Reservas.room),
                    joinedload(Reservas.plan)
                )
                .filter_by(id=reserve_id)
                .all()
            )
            return reserves if reserves else None
        except Exception as e:
            session.rollback()
            print(f'Erro ao listar reservas: {e}')
            return None
        finally:
            session.close()

    @classmethod
    def update_reserve(cls,reserve_id, date_init, date_end, room_id, plan_id, states):
        session = SessionLocal()
        try:
            update = session.query(Reservas).filter_by(id=reserve_id).first()
            if update:
                update.room_id = room_id
                update.date_init = date_init
                update.date_end = date_end
                update.states = states
                update.plan_id = plan_id
                session.commit()
                return True
            else:
                return None

        except Exception as e:
            session.rollback()
            print(f'Erro ao atualizar reserva: {e}')
            return False
        finally:
            session.close()
            

    @classmethod
    def delete_reserve(cls, reserve_id):
        session = SessionLocal()
        try:
            delete = session.query(Reservas).filter_by(id=reserve_id).first()
            if delete:
                session.delete(delete)
                session.commit()
                return True
            else:
                return False
        except Exception as e:
            session.rollback()
            print(f'Erro ao deletar reserva: {e}')
        finally:
            session.close()

    @classmethod
    def view_all_reserves(cls):
        session = SessionLocal()
        try:
            reserves = session.query(Reservas).options(joinedload(Reservas.room), joinedload(Reservas.plan)).all()
            return reserves
        except Exception as e:
            session.rollback()
            print(f'Erro ao listar reservas: {e}')
            return None
        finally:
            session.close()