from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    DB_NAME: str
    CLAUDE_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()