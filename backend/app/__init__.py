from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    with app.app_context():
        from .routes import auth
        app.register_blueprint(auth.auth)

    @login_manager.user_loader
    def load_user(user_id):
        from .models.User import User
        return User.query.get(int(user_id))

    return app
