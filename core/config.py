from pydantic_settings import BaseSettings
from typing import ClassVar, List

class Settings(BaseSettings):
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite:///./test.db"
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 5  # 5MB
    ALLOWED_CONTENT_TYPES: ClassVar[List[str]] = ["image/jpeg", "image/png"]

    class Config:
        env_file = ".env"

settings = Settings()