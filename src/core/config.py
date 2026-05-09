"""Application configuration."""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    PROJECT_NAME: str = "AI Agent Chatbot"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    LOG_LEVEL: str = "INFO"
    APP_ENV: str = "local"

    # CORS Configuration
    ALLOWED_ORIGINS: list[str] = ["*"]

    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str
    OPENAI_EMBEDDING_MODEL: str

    # Gemini Configuration
    # GEMINI_API_KEY: str
    # GEMINI_MODEL: str = "gemini-2.5-flash-lite"


    # Langfuse Configuration
    LANGFUSE_PUBLIC_KEY: str
    LANGFUSE_SECRET_KEY: str
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"


    # Backend API Configuration (Node.js API server)
    BACKEND_API_URL: str = "http://localhost:5000"

    # MongoDB Configuration (overridden by .env)
    MONGODB_URI: str
    MONGODB_DB_NAME: str = "project_graduation"


    # class Config:
    #     env_file = ".env"
    #     case_sensitive = True
    #     extra = "ignore"  # Allow extra environment variables
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")


settings = Settings()
