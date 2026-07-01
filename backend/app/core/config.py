from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/lms"
    secret_key: str = "change-me"
    jwt_secret: str = "change-me-jwt"
    jwt_refresh_secret: str = "change-me-refresh"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    upload_dir: str = "uploads"
    frontend_url: str = "http://localhost:5173"
    backend_url: str = "http://localhost:8000"
    rate_limit_login: str = "5/minute"
    rate_limit_default: str = "100/minute"
    storage_backend: str = "local"


settings = Settings()
