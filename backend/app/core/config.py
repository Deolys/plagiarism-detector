from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_API_BASE_URL: str = None
    PROXY: str = None
    GITHUB_TOKEN: str
    GITHUB_API_URL: str = "https://api.github.com"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
