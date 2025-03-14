from Models.base import Base, engine

def create_db():
    Base.metadata.create_all(engine)
    print("Banco de dados e tabelas criados com sucesso.")

if __name__ == '__main__':
    create_db()