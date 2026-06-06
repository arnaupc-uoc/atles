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
    login.login_view = "admin.login"
    login.login_message = "Cal iniciar sessió per accedir a l'eina d'administració."
    login.login_message_category = "info"
    login.init_app(app)
    CORS(app)
    api.init_app(app)

    from app.routes import register_routes
    register_routes(api)


    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    # Ensure logs directory and backups directory exist
    import os
    from app.models.user import User

    backups_dir = app.config.get("BACKUPS_DIR")
    logs_dir = os.path.dirname(app.config.get("LOG_FILE"))
    os.makedirs(backups_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)

    # Configure basic file logging if not already configured
    import logging
    if not app.logger.handlers:
        handler = logging.FileHandler(app.config.get("LOG_FILE"))
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s: %(message)s"
        )
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)

    with app.app_context():
        db.create_all()
        if not db.session.query(User).filter_by(username="admin").first():
            admin_user = User(username="admin", email="admin@example.com")
            admin_user.set_password("admin")
            db.session.add(admin_user)
            db.session.commit()

    return app
