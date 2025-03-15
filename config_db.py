from Models.base import Base, engine
from Models.profile import Profile
from Models.plans import Planos
from Models.price import Preco
from Models.rooms import Salas
from Models.reserves import Reservas
from Models.payment import Pagamento
from Models.enterprise import Empresa
from Models.invoice import Fatura

def create_db():
    Base.metadata.create_all(engine)
    print("Banco de dados e tabelas criados com sucesso.")

if __name__ == '__main__':
    create_db()