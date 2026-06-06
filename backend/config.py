import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", "dev_password_salt")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://atles:atles_dev@localhost:5432/atles",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "25"))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "false").lower() in ("true", "1", "yes")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "false").lower() in ("true", "1", "yes")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "Atles <no-reply@localhost>")
    # Logs and backups
    LOG_FILE = os.getenv("LOG_FILE", os.path.join(basedir, "logs", "app.log"))
    BACKUPS_DIR = os.getenv("BACKUPS_DIR", os.path.join(basedir, "backups"))
    PG_DUMP_PATH = os.getenv("PG_DUMP_PATH", "pg_dump")
    PSQL_PATH = os.getenv("PSQL_PATH", "psql")
