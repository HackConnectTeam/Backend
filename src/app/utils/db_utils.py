from src.app.config.config import settings


def get_db_uri():
    """
    Get the database URI from the environment variables.
    :return: Database URI
    """
    return f"postgresql://{settings.db.user}:{settings.db.password}@{settings.db.host}:{settings.db.port}/{settings.db.name}"
