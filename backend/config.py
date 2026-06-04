import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://atles:atles_dev@localhost:5432/atles",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
