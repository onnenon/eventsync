import os

import spylogger

BASEDIR = os.path.abspath(os.path.dirname(__file__))

LOGGER = spylogger.get_logger(log_level="DEBUG")

SECRET_KEY = os.urandom(24)

FLASK_ENV = "dev"

DEBUG = True

# DATABASE
postgresql = "postgresql://{}:{}@{}:{}/{}".format(
    os.getenv("DB_USERNAME", "eventadmin"),
    os.getenv("DB_PASSWORD", "password"),
    os.getenv("DB_HOST", "localhost"),
    os.getenv("DB_PORT", "5432"),
    os.getenv("DB_NAME", "eventSyncDB"),
)
sqlite = f"sqlite:///app.db"

SQLALCHEMY_DATABASE_URI = postgresql if os.getenv("DB") == "postgres" else sqlite

SQLALCHEMY_TRACK_MODIFICATIONS = False
