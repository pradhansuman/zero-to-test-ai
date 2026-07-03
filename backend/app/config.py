"""FastAPI configuration."""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    app_name: str = "QA Automation Platform"
    app_version: str = "2.0.0"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/qa_db")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    jwt_secret: str = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24

    cors_origins: list = ["http://localhost:3000", "http://localhost:8000"]

    class Config:
        env_file = ".env"


settings = Settings()
