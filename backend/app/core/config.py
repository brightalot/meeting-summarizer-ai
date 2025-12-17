from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "NoteSync AI"
    DATABASE_URL: str
    OPENAI_API_KEY: Optional[str] = None
    GEMINI_API_KEY: Optional[str] = None
    NOTION_API_KEY: Optional[str] = None
    NOTION_DATABASE_ID: Optional[str] = None
    TEAMS_WEBHOOK_URL: Optional[str] = None
    
    # Postgres variables (needed to avoid extra fields error)
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None

    class Config:
        env_file = ".env"
    
    @property
    def get_database_url(self) -> str:
        # If DATABASE_URL is set (from .env), use it
        # But inside Docker, we might need to override 'localhost' to 'db'
        url = self.DATABASE_URL
        if "localhost" in url:
             # Basic check to see if we are running inside docker (env vars usually hint this)
             # But here, let's just allow .env to be the source of truth.
             # The issue is likely that .env has localhost:5433, but docker needs db:5432
             pass
        return url

settings = Settings()

