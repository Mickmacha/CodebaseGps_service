import os
from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

# 1. Resolve the path to the project root
# __file__ is app/config.py -> .parent is app/ -> .parent.parent is project_root/
ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT_DIR / ".env"

class Settings(BaseSettings):
    # Required fields
    GEMINI_API_KEY: str
    ENVIRONMENT: str
    
    # Modern Pydantic V2 config style
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=True
    )

@lru_cache()
def get_settings():
    # If .env is missing, this will now raise a clear ValidationError
    # listing exactly which keys are missing.
    return Settings()

settings = get_settings()