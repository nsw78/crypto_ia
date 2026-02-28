import os
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Crypto IA Auditor API"
    APP_VERSION: str = "3.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 4
    CORS_ORIGINS: List[str] = ["*"]

    # Security
    SECRET_KEY: str = "change-me-in-production-use-openssl-rand-hex-32"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    BCRYPT_ROUNDS: int = 12

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./crypto_ia.db"

    # Redis (cache + rate limiting)
    REDIS_URL: str = "redis://localhost:6379/0"

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000

    # LLM / OpenAI
    OPENAI_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4-turbo"
    LLM_TEMPERATURE: float = 0.3

    # Blockchain APIs
    ETHERSCAN_API_KEY: str = ""
    BSCSCAN_API_KEY: str = ""

    # News
    NEWSAPI_KEY: str = ""

    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_PUBLIC_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    # Plans
    FREE_CREDITS: int = 3
    BASIC_CREDITS: int = 20
    PRO_CREDITS: int = 100

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


@lru_cache()
def get_settings() -> Settings:
    return Settings()
