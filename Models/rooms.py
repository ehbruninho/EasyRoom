from datetime import datetime

from sqlalchemy import Column, String,Integer,ForeignKey, Boolean, Enum, DATETIME
from Models.base import Base, SessionLocal

class Salas(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255),nullable=True)
    description = Column(String(255), nullable=True)
    capacity = Column(Integer, nullable=True)
    disp = Column(Boolean, nullable=True)
    type = Column (Enum("Individual","Compartilhada"), default="Individual", nullable=True)
    local = Column(String(255), nullable=True)
    foto = Column(String(255), nullable=True)
    create_in = Column(DATETIME, nullable=True)
    att_in = Column(DATETIME, nullable=True)
    def __init__(self,name,description,capacity,disp,type,local,foto,reserve_id,pag_id):
        self.name = name
        self.description = description
        self.capacity = capacity
        self.disp = disp
        self.type = type
        self.local = local
        self.foto = foto
        self.reserve_id = pag_id
        self.create_in = datetime.now()
        self.att_in = datetime.now()

    @classmethod
    def create_room(cls,name,description,capacity,disp,type,local,foto):
        session = SessionLocal()
        try:
            room = Salas(name,description,capacity,disp,type,local,foto)
            session.add(room)
            session.commit()
            return room
        except Exception as e:
            session.rollback()
            print(f"Erro ao salvar a salva! Error: {e}")
            return False
        finally:
            session.close()

