from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # App
    app_name: str = "Data Contracts Studio"
    app_version: str = "0.0.1"
    debug: bool = False

    # Database
    database_url: str = "sqlite:///./data_contracts.db"

    # CORS
    allowed_origins: list[str] = ["http://localhost:3000", "http://localhost:8080"]

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
