from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # CRITICAL IDENTITY: No defaults provided. If missing from .env, the app crashes safely.
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    
    DB_HOST: str = "db"
    DB_PORT: int = 5432

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Instructs Pydantic to search the root directory for a .env file automatically
    model_config = SettingsConfigDict(env_file=(".env", "../.env"), env_file_encoding="utf-8", extra="ignore")

settings = Settings()
