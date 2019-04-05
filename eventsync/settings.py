import os

import spylogger

BASEDIR = os.path.abspath(os.path.dirname(__file__))

LOGGER = spylogger.get_logger()

SECRET_KEY = os.urandom(24)

# DATABASE
# SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
#     os.getenv("DB_USERNAME", "eventadmin"),
#     os.getenv("DB_PASSWORD", "password"),
#     os.getenv("DB_HOST", "localhost"),
#     os.getenv("DB_PORT", "5432"),
#     os.getenv("DB_NAME", "eventSyncDB"),
# )

SQLALCHEMY_DATABASE_URI = f"sqlite:///app.db"

SQLALCHEMY_TRACK_MODIFICATIONS = False
