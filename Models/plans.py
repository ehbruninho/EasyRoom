from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from Models.base import Base, SessionLocal

class Planos(Base):
    __tablename__ = 'plans'
    id = Column(Integer, primary_key=True, autoincrement=True,nullable=False)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total_time = Column(Enum("1h","2h","Turno", "Diario","Semanal","Mensal","Anual"), nullable=False)
    num_people = Column(Integer, nullable=False)

    def __init__(self, name, user_id, total_time, num_people):
        self.name = name
        self.user_id = user_id
        self.total_time = total_time
        self.num_people = num_people

    @classmethod
    def create_plan(cls, name, user_id, total_time, num_people):
        session = SessionLocal()
        try:
            plan = Planos(name, user_id, total_time, num_people)
            session.add(plan)
            session.commit()
            return plan

        except Exception as e:
            session.rollback()
            print(f"Erro ao criar o plano! Error: {e}")
            return False
        finally:
            session.close()




    #id, name, user_id ,length_time, num_people