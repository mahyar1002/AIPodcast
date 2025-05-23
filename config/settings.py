import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Get the base directory of your project
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')


class Settings(BaseSettings):
    # App settings
    ENV: str = os.getenv("ENV", "development")
    APP_NAME: str = os.getenv("APP_NAME", "AI Podcast")
    DEBUG: str = os.getenv("DEBUG", "False").lower() == "true"
    API_STR: str = "/api"
    ALLOWED_ORIGINS: str = "*"
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = os.getenv("API_PORT", 7878)

    # AI Models
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    OPENAI_LLM_MODEL: str = os.getenv("OPENAI_LLM_MODEL", "gpt-4o-mini")
    OPENAI_EMBEDDING_MODEL: str = os.getenv(
        "OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
    DEFAULT_AI_MODEL: str = os.getenv("DEFAULT_AI_MODEL", "OPENAI")

    # Agent settings
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")

    class Config:
        env_file = ".env"


# Create a settings instance
settings = Settings()

# Export the settings instance for use in other modules
__all__ = ["settings"]
