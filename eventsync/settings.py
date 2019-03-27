import spylogger

LOGGER = spylogger.get_logger()

# DATABASE
SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
    os.getenv("DB_USERNAME"),
    os.getenv("DB_PASSWORD"),
    os.getenv("DB_HOST", "localhost"),
    os.getenv("DB_PORT", "5432"),
    os.getenv("DB_NAME"),
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
