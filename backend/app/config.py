import os
from pydantic import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "Task Manager API"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")
    CORS_ORIGINS: str = "https://task-app-frontend-ay5oqkoyoa-ue.a.run.app"
    API_PREFIX: str = "/api"

    class Config:
        env_file = ".env"

settings = Settings()