"""
Configuration settings for Smart NEPSE Investor backend
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Database
    DATABASE_URL: str = "sqlite:///./nepse.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API
    NEPSE_API_BASE_URL: str = "https://api.nepsedata.com"
    STOCK_PRICE_UPDATE_INTERVAL: int = 300  # 5 minutes in seconds
    
    # Notifications
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_CHAT_ID: str = ""
    ENABLE_EMAIL_ALERTS: bool = False
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_EMAIL: str = ""
    SMTP_PASSWORD: str = ""
    
    # Application
    DEBUG: bool = True
    APP_NAME: str = "Smart NEPSE Investor"
    API_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    """Get cached settings instance"""
    return Settings()
