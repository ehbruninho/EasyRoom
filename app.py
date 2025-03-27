from flask import Flask, render_template
from Models.base import Base, engine
from routes.user_routes import user_bp
from routes.profile_routes import profile_bp
from Models.users import User
from flask_login import LoginManager
from routes.main_routes import main_bp
from routes.rooms_routes import rooms_bp
from routes.reserves_routes import reserves_bp
from routes.reserve_approved_routes import approved_reserves_bp

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
app.register_blueprint(main_bp, url_prefix='/main')
app.register_blueprint(rooms_bp, url_prefix='/room')
app.register_blueprint(reserves_bp, url_prefix='/reserves')
app.register_blueprint(approved_reserves_bp, url_prefix='/approved')


@app.route('/')
def init_app():
    return render_template('login.html')

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(host='0.0.0.0', port=5000, debug=True)

