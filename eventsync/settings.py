import os

import spylogger

LOGGER = spylogger.get_logger()

SECRET_KEY = os.urandom(24)

# DATABASE
SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
    os.getenv("DB_USERNAME", "eventadmin"),
    os.getenv("DB_PASSWORD", "password"),
    os.getenv("DB_HOST", "localhost"),
    os.getenv("DB_PORT", "5432"),
    os.getenv("DB_NAME", "eventSyncDB"),
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
