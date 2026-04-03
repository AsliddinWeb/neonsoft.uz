from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App
    APP_ENV: str = "local"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Database — injected by Docker compose via environment:, NOT from .env
    DATABASE_URL: str

    # API
    API_PORT: int = 8000

    # CORS — comma-separated string from .env
    ALLOWED_ORIGINS: str = "http://localhost:5173"

    # Media
    MEDIA_DIR: str = "media"
    MEDIA_URL: str = "/media"

    # Superadmin seed
    SUPERADMIN_EMAIL: str = ""
    SUPERADMIN_PASSWORD: str = ""
    SUPERADMIN_NAME: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]


settings = Settings()
