import os

from pydantic_settings import BaseSettings, SettingsConfigDict

DB_MODE = os.getenv("DB_MODE", "sqlite_example")

ENV_FILES = {
    "sqlite_example": ".env.sqlite.example",
    "sqlite": ".env.sqlite",
    "postgres": ".env.postgres",
    "mysql": ".env.mysql",
}

ENV_FILE = ENV_FILES.get(DB_MODE, ".env.sqlite.example")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8")

    environment: str = "sqlite_example"
    sqlalchemy_database_url: str = "sqlite:///./todosapp.example.db"
    secret_key: str = "change_me"
    algorithm: str = "HS256"


settings = Settings()
