"""
Apllication configuration and settings 
"""
import os 
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    # Database
    database_url: str ="postgresql+asyncpg://jobfit@localhost:5432/jobfit_coplit"
    database_url_sync: str ="postgresql://jobfit:jobfit@localhost:5432/jobfit_copilot"

    #Application 
    app_name: str = "JobFit Copilot API"
    debug: bool =False
    api_prefix: str = "/api"

    #security
    secret_key: str =" change-me-in-production"
    access_token_expire_minutes: int = 60*24*7 # one week
    
    # Github OAUTH(for v2)
    github_client_id: Optional[str]=None 
    github_client_service: Optional[str]=None 

    #File Storage
    upload_folder: Path =Path("uploads")
    max_upload_size_mb: int= 20

    # Github API
    github_api_base: str ="https://api.github.com"
    github_api_token: Optional[str] = None 
    redis_url: str = "redis://localhost:6379/0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra="ignore"

@lru_cache
def get_settings() -> Settings:
    return Settings()

# Ensure upload folder exists
settings = get_settings()
settings.upload_folder.mkdir(parents=True, exist_ok=True)


