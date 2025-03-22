from sqlalchemy import Column, Integer, String
from Models.base import Base, create_session
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True,autoincrement=True,nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)


    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    @classmethod
    def create_user(cls,email, password):
        session = create_session()
        try:
            user = cls(email, password)
            session.add(user)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Erro ao cadastrar Usuario! Erro {e}")
            return False
        finally:
            session.close()
    @classmethod
    def check_user (cls,email):
        session = create_session()
        try:
            user = session.query(User).filter_by(email=email).first()
            return user is not None
        except Exception as e:
            session.rollback()
            print(f"Erro ao validar Usuario! Erro {e}")
            return False
        finally:
            session.close()

    @classmethod
    def login(cls,email, password):
        session = create_session()
        try:
            user = session.query(User).filter(User.email==email).first()
            if user and check_password_hash(user.password,password):
                return user
        except Exception as e:
            session.rollback()
            print(f"Erro ao autenticar Usuario!{e}")
            return None
        finally:
            session.close()

    @classmethod
    def update_password(cls,email, password):
        try:
            session = create_session()
            user = session.query(cls).filter_by(email=email).update({'password': generate_password_hash(password)})
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Erro ao atualizar Usuario! Erro {e}")
            return False

        finally:
            session.close()

    def find_by_id(id):
        session = create_session()
        try:
            user = session.query(User).get(int(id))
            return user
        except Exception as e:
            print(f"Erro ao obter Usuario! Erro {e}")
            return False
        finally:
            session.close()
