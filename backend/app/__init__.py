from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    CORS(app, resources={r"/api/*": {"origins": "https://quad-conquerors.vercel.app/"}})

    with app.app_context():
        from .models import volunteer  # Import models
        from .routes import auth, main_routes  # Import routes
        app.register_blueprint(auth.auth)
        app.register_blueprint(main_routes.bp)

    return app

# Make sure to export db here
from app import db
