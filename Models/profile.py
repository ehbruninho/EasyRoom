from sqlalchemy import Column, String, Integer, ForeignKey
from Models.base import Base, SessionLocal, create_session


class Profile(Base):
    __tablename__ = 'profiles'
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(100), nullable=False)
    cpf = Column(String(11),unique=True, nullable=False)
    phone = Column(String(15), nullable=False)
    image = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __init__(self, name, cpf, phone, image, user_id):
        self.name = name
        self.cpf = cpf
        self.phone = phone
        self.image = image
        self.user_id = user_id

    @classmethod
    def create_profile(cls, name, cpf, phone, image, user_id):
       session = create_session()
       try:
            profile = Profile(name, cpf, phone, image, user_id)
            session.add(profile)
            session.commit()
            return profile
       except Exception as e:
            session.rollback()
            print(f"Erro ao cadastrar perfil! Erro: {e}")
            return None

       finally:
           session.close()

    @classmethod
    def view_profile(cls, user_id):
        session = create_session()
        try:
            profile = session.query(Profile).filter_by(user_id=user_id).first()
            return profile
        except Exception as e:
            session.rollback()
            print(f"Erro ao listar perfil! Erro: {e}")
            return None
        finally:
            session.close()

    @classmethod
    def find_profile_by_User_id(cls, user_id):
        session = create_session()
        try:
            profile = session.query(Profile).filter_by(user_id=user_id).first()
            return profile
        except Exception as e:
            session.rollback()
            print(f"Erro ao listar perfil! Erro: {e}")
            return None
        finally:
            session.close()

    @classmethod
    def view_all_profiles(cls):
        session = create_session()
        try:
            profile = session.query(Profile).all()
            return profile
        except Exception as e:
            session.rollback()
            print(f"Erro ao listar perfil! Erro: {e}")
            return None
        finally:
            session.close()