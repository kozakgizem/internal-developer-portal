from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Projenin çalıştırıldığı ana kök dizini doğrudan baz alıyoruz
BASE_DIR = Path.cwd()

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./portal.db"
    SECRET_KEY: str = "gizli_anahtar"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()