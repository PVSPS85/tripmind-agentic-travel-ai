from typing import List, Optional
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    APP_NAME: str = "TripMind AI Backend"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://tripmind-ai.vercel.app"
    ]

    # Database — defaults to local SQLite if not provided
    DATABASE_URL: str = "sqlite+aiosqlite:///./tripmind.db"

    # Agent Engine / LLM
    GROQ_API_KEY: str = ""
    GROQ_MODEL_NAME: str = "llama-3.3-70b-versatile"

    # Agent Tools
    SERPER_API_KEY: str = ""
    OPENWEATHER_API_KEY: Optional[str] = None
    GEOAPIFY_API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        case_sensitive=True,
        extra="ignore"
    )

    @field_validator('DATABASE_URL')
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Ensure DATABASE_URL uses asyncpg driver for async operations."""
        if v and 'postgresql' in v and 'asyncpg' not in v:
            v = v.replace('postgresql://', 'postgresql+asyncpg://')
        return v

settings = Settings()
