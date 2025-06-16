"""Application configuration module.

This module provides centralized configuration management for the Data Contracts Studio
application using Pydantic settings with environment variable support.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings with environment variable support.

    This class provides type-safe configuration management with automatic
    environment variable binding and validation.

    Attributes:
        app_name: The application name for display and logging.
        app_version: Current application version.
        debug: Enable debug mode for development.
        database_url: Database connection string.
        allowed_origins: List of allowed CORS origins.
        secret_key: Secret key for JWT token signing.
        algorithm: JWT algorithm for token encoding.
        access_token_expire_minutes: JWT token expiration time in minutes.
    """

    # Application metadata
    app_name: str = "Data Contracts Studio"
    app_version: str = "0.0.4"
    debug: bool = False

    # Database configuration
    database_url: str = "sqlite:///./data_contracts.db"

    # CORS configuration
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]

    # Security configuration
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        """Pydantic configuration for environment variable handling."""

        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
