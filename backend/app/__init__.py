from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from flask_restx import Api

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
api = Api()


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
