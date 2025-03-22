from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME, Enum
from sqlalchemy.orm import relationship, joinedload
from Models.base import Base, SessionLocal
from Models.rooms import Salas
from Models.plans import Planos


class Reservas(Base):
    __tablename__ = 'reserves'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'),nullable=False)
    date_init = Column(DATETIME, nullable=False)
    date_end = Column(DATETIME, nullable=False)
    states = Column(Enum("Pendente","Pago","Cancelado"),default="Pendente",nullable=False)
    plan_id = Column(Integer, ForeignKey('plans.id'), nullable=False)

    room = relationship("Salas", backref="reserves")
    plan = relationship("Planos", backref="reserves")

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
            return reserves
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
