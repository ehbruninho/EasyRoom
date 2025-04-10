from sqlalchemy import Column, Integer, String, Enum
from Models.base import Base, SessionLocal
from sqlalchemy.orm import relationship

class Planos(Base):
    __tablename__ = 'plans'
    id = Column(Integer, primary_key=True, autoincrement=True,nullable=False)
    name = Column(String(255), nullable=False)
    total_time = Column(Enum("1h","2h","Turno","Diario","Semanal","Mensal","Anual"), nullable=False)
    num_people = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)


    def __init__(self, name, total_time, num_people, duration):
        self.name = name
        self.total_time = total_time
        self.num_people = num_people
        self.duration = duration


    @classmethod
    def create_plan(cls, name,total_time, num_people, duration):
        session = SessionLocal()
        try:
            plan = Planos(name, total_time, num_people, duration)
            session.add(plan)
            session.commit()
            return plan

        except Exception as e:
            session.rollback()
            print(f"Erro ao criar o plano! Error: {e}")
            return False
        finally:
            session.close()

    @classmethod
    def view_plans(cls):
        session = SessionLocal()
        try:
            plans = session.query(Planos).all()
            return plans
        except Exception as e:
            session.rollback()
            print(f"Erro ao buscar os plano! Error: {e}")
            return None
        finally:
            session.close()

    @classmethod
    def findPlans_by_Id(cls, id):
        session = SessionLocal()
        try:
            session = SessionLocal()
            plan = session.query(Planos.duration).filter_by(id=id).first()
            return plan
        except Exception as e:
            session.rollback()
            print(f"Erro ao buscar o plano! Error: {e}")
            return None
        finally:
            session.close()

    @classmethod
    def findPlansName_by_Id(cls, id):
        session = SessionLocal()
        try:
            plan = session.query(Planos.name).filter_by(id=id).first()
            return plan
        except Exception as e:
            session.rollback()
            print(f"Erro ao buscar o plano! Error: {e}")
            return None
        finally:
            session.close()

    @classmethod
    def compare_plans(cls, name, total_time, duration):
        session = SessionLocal()
        try:
            plans = session.query(Planos).filter(Planos.name == name, Planos.total_time == total_time, Planos.duration == duration).all()
            return plans
        except Exception as e:
            session.rollback()
            print(f"Erro ao buscar o plano! Error: {e}")
            return None
        finally:
            session.close()

    @classmethod
    def findTotalTime_by_Id(cls, plan_id):
        session = SessionLocal()
        try:
            duration = session.query(Planos.duration).filter(Planos.id==plan_id).first()
            return duration[0]
        except Exception as e:
            session.rollback()
            print(f"Erro ao buscar o plano! Error: {e}")
            return None
        finally:
            session.close()