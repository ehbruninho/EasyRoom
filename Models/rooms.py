from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Enum, DATETIME
from Models.base import Base, SessionLocal


class Salas(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    capacity = Column(Integer, nullable=False)
    disp = Column(Boolean, default=True, nullable=False)
    type = Column(Enum("Individual", "Compartilhada"), default="Individual", nullable=False)
    local = Column(String(255), nullable=True)
    foto = Column(String(255), nullable=True)
    create_in = Column(DATETIME, default=datetime.now, nullable=False)
    att_in = Column(DATETIME, default=datetime.now, nullable=False)

    def __init__(self, name, description, capacity, disp, type, local, foto):
        self.name = name
        self.description = description
        self.capacity = capacity
        self.disp = disp
        self.type = type
        self.local = local
        self.foto = foto
        self.create_in = datetime.now()
        self.att_in = datetime.now()

    @classmethod
    def create_room(cls, name, description, capacity, disp, type, local, foto):
        session = SessionLocal()
        try:
            room = cls(name, description, capacity, disp, type, local, foto)
            session.add(room)
            session.commit()
            return room
        except Exception as e:
            session.rollback()
            print(f"Erro ao salvar a sala! Error: {e}")
            return False
        finally:
            session.close()

    @classmethod
    def view_room(cls):
        session = SessionLocal()
        try:
            rooms = session.query(Salas).filter_by(disp=True).all()
            return rooms
        except Exception as e:
            session.rollback()
            print(f"Erro ao buscar as salas! Error: {e}")
            return []
        finally:
            session.close()
    @classmethod
    def view_room_by_id(cls, room_id):
        session = SessionLocal()
        try:
            room = session.query(Salas).filter_by(id = room_id).first()
            return room
        except Exception as e:
            session.rollback()
            print(f"Erro ao buscar a sala! Error: {e}")
            return None
        finally:
            session.close()

    @classmethod
    def remove_room(cls, room_id):
        session = SessionLocal()
        try:
            session.query(cls).filter(cls.id == room_id).delete()
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Erro ao remover a sala! Error: {e}")
            return False
        finally:
            session.close()

    @classmethod
    def update_room(cls, room_id, description, capacity, disp, type, local, foto):
        session = SessionLocal()
        try:
            room = session.query(Salas).filter_by(id = room_id).first()
            if room:
                room.description = description
                room.capacity = capacity
                room.disp = disp
                room.type = type
                room.local = local
                room.foto = foto
                session.commit()
                return True
        except Exception as e:
            session.rollback()
            print(f"Erro ao atualizar a sala! Error: {e}")
            return False
        finally:
            session.close()

