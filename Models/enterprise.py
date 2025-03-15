from sqlalchemy import Column, Integer, String, ForeignKey
from Models.base import Base, SessionLocal

class Empresa(Base):
    __tablename__ = 'enterprises'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False)
    cnpj = Column(String(14), nullable=False)
    master_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    num_members = Column(Integer, nullable=False)

    def __init__(self, name, cnpj, master_id, num_members):
        self.name = name
        self.cnpj = cnpj
        self.master_id = master_id
        self.num_members = num_members

    @classmethod
    def create_enterprise(cls, name, cnpj, master_id, num_members):
        session = SessionLocal()
        try:
            enterprise = Empresa(name, cnpj, master_id, num_members)
            session.add(enterprise)
            session.commit()
            return enterprise

        except Exception as e:
            session.rollback()
            print(f"Erro ao cadastrar empresa! Error: {e}")

        finally:
            session.close()

