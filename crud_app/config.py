from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    env_name: str = "Local Environment"
    Test_url: str = "http://localhost:8000"
    db_url: str = "BD_URI"

    class Config:
        env_file = ".env"
        
@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    return settings
    