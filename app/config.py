from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    
    GEMINI_API_KEY: str
    
    ENVIRONMENT: str
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
