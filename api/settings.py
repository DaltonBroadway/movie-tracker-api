from functools import lru_cache

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    # General Settings
    enable_metrics: bool = Field(
        True,
        title="Enable Metrics",
        description="Enable prometheus metrics if set to true. Default: True",
        env="ENABLE_METRICS",
    )
    # MongoDB Settings
    mongo_connection_string: str = Field(
        "mongodb://localhost:27017",
        title="MongoDB Connection String",
        description="Connection String for MongoDB",
        env="MONGODB_CONNECTION_STRING",
    )
    mongo_database_name: str = Field(
        "movie_track_db",
        title="MongoDB Movie Database Name",
        description="Database name for MongoDB Movies Database",
        env="MONGODB_DATABASE_NAME",
    )

    def __hash__(self) -> int:
        return 1


@lru_cache()
def settings_instance():
    """
    Settings instance to be used as a FastAPI dependency
    """
    return Settings()
