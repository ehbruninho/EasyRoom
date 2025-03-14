from flask import Flask
from Models.base import Base, engine
from routes.user_routes import user_bp
from routes.profile_routes import profile_bp
from Models.users import User
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = '!@#Nova!@#'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'
@login_manager.user_loader
def load_user(user_id):
    return User.find_by_id(user_id)
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(profile_bp, url_prefix='/profile')

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run()
