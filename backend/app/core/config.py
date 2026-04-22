from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "AutoAiFlow"
    APP_ENV: str = "dev"
    APP_DEBUG: bool = True

    DATABASE_URL: str = "postgresql+psycopg://auto_ai_flow:aiflow2026@172.18.14.8:5432/auto_ai_flow"
    REDIS_URL: str = "redis://172.18.14.8:6379/0"

    JWT_SECRET: str = "dev-secret-change-in-production-2026"
    JWT_EXPIRE_MINUTES: int = 120
    JWT_REFRESH_EXPIRE_DAYS: int = 7
    JWT_ALGORITHM: str = "HS256"

    DEFAULT_TIMEOUT_SEC: int = 300

    OPENAI_API_KEY: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings = Settings()
