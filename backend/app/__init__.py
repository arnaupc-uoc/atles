from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from flask_restx import Api

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
api = Api(prefix="/api", doc="/api")


# User loader per Flask-Login
@login.user_loader
def load_user(user_id):
    # Importem el model d'usuari aquí a dins per evitar "importacions circulars"
    from app.models import User

    # Busquem l'usuari a la base de dades utilitzant el seu ID (convertit a enter)
    return db.session.get(User, int(user_id))

# Funció per crear l'aplicació Flask
def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    CORS(app)
    api.init_app(app)

    from app.routes import register_routes
    register_routes(api)

    return app
