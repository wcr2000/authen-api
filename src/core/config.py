import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file variables
load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "a_default_secret_key_if_not_set_in_env")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    class Config:
        env_file = ".env" # Though load_dotenv already does this, this is good practice for pydantic-settings
        extra = "ignore"


settings = Settings()