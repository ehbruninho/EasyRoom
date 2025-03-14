from flask import Flask
from Controllers.users_controllers import create_user
from Models.base import Base, engine  # Importando a base e o engine para criar o banco

app = Flask(__name__)

# Criando as tabelas antes de rodar a aplicação
Base.metadata.create_all(engine)

@app.route('/')
def hello_world():
    created = create_user("ssss", "ssss@gmail.com", "12345")
    if created:
        return 'Usuário cadastrado com sucesso!'
    return 'Usuário já existe ou erro ao cadastrar!'

if __name__ == '__main__':
    app.run()
