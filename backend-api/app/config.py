from typing import List, Optional
from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    APP_NAME: str = "TripMind AI Backend"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://tripmind-ai.vercel.app"
    ]

    # Database
    DATABASE_URL: str

    # Agent Engine / LLM
    GROQ_API_KEY: str
    GROQ_MODEL_NAME: str = "llama3-70b-8192"

    # Agent Tools
    SERPER_API_KEY: str
    OPENWEATHER_API_KEY: Optional[str] = None
    GEOAPIFY_API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
