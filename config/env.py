"""
Environment configuration module for Multiagent-manus.
Loads settings from environment variables and YAML configuration.
"""

import os
from typing import Optional, List
from pydantic import BaseSettings, Field
from pathlib import Path
import yaml

class Settings(BaseSettings):
    """Application settings loaded from environment variables and config files."""
    
    # Application Settings
    APP_NAME: str = Field(default="Multiagent-manus", env="APP_NAME")
    APP_VERSION: str = Field(default="1.0.0", env="APP_VERSION")
    APP_ENV: str = Field(default="development", env="APP_ENV")
    DEBUG: bool = Field(default=False, env="DEBUG")
    SECRET_KEY: str = Field(env="SECRET_KEY")
    
    # AI/LLM Configuration
    OPENAI_API_KEY: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4", env="OPENAI_MODEL")
    OPENAI_MAX_TOKENS: int = Field(default=4000, env="OPENAI_MAX_TOKENS")
    
    ANTHROPIC_API_KEY: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    ANTHROPIC_MODEL: str = Field(default="claude-3-sonnet-20240229", env="ANTHROPIC_MODEL")
    
    # Database Configuration
    DATABASE_URL: str = Field(env="DATABASE_URL")
    DB_HOST: str = Field(default="localhost", env="DB_HOST")
    DB_PORT: int = Field(default=5432, env="DB_PORT")
    DB_NAME: str = Field(default="multiagent_manus", env="DB_NAME")
    DB_USER: str = Field(env="DB_USER")
    DB_PASSWORD: str = Field(env="DB_PASSWORD")
    
    # Redis Configuration
    REDIS_URL: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    REDIS_HOST: str = Field(default="localhost", env="REDIS_HOST")
    REDIS_PORT: int = Field(default=6379, env="REDIS_PORT")
    REDIS_PASSWORD: Optional[str] = Field(default=None, env="REDIS_PASSWORD")
    
    # WhatsApp Business Configuration
    WHATSAPP_ENABLED: bool = Field(default=True, env="WHATSAPP_ENABLED")
    WHATSAPP_ACCESS_TOKEN: Optional[str] = Field(default=None, env="WHATSAPP_ACCESS_TOKEN")
    WHATSAPP_PHONE_NUMBER_ID: Optional[str] = Field(default=None, env="WHATSAPP_PHONE_NUMBER_ID")
    WHATSAPP_BUSINESS_ACCOUNT_ID: Optional[str] = Field(default=None, env="WHATSAPP_BUSINESS_ACCOUNT_ID")
    WHATSAPP_WEBHOOK_VERIFY_TOKEN: Optional[str] = Field(default=None, env="WHATSAPP_WEBHOOK_VERIFY_TOKEN")
    WHATSAPP_WEBHOOK_URL: Optional[str] = Field(default=None, env="WHATSAPP_WEBHOOK_URL")
    
    # Facebook/Meta Configuration
    FACEBOOK_APP_ID: Optional[str] = Field(default=None, env="FACEBOOK_APP_ID")
    FACEBOOK_APP_SECRET: Optional[str] = Field(default=None, env="FACEBOOK_APP_SECRET")
    FACEBOOK_PAGE_ACCESS_TOKEN: Optional[str] = Field(default=None, env="FACEBOOK_PAGE_ACCESS_TOKEN")
    FACEBOOK_PAGE_ID: Optional[str] = Field(default=None, env="FACEBOOK_PAGE_ID")
    
    # Payment Gateway Configuration
    UPI_ENABLED: bool = Field(default=True, env="UPI_ENABLED")
    UPI_PROVIDER: str = Field(default="razorpay", env="UPI_PROVIDER")
    
    # Razorpay
    RAZORPAY_KEY_ID: Optional[str] = Field(default=None, env="RAZORPAY_KEY_ID")
    RAZORPAY_KEY_SECRET: Optional[str] = Field(default=None, env="RAZORPAY_KEY_SECRET")
    RAZORPAY_WEBHOOK_SECRET: Optional[str] = Field(default=None, env="RAZORPAY_WEBHOOK_SECRET")
    
    # Cashfree
    CASHFREE_APP_ID: Optional[str] = Field(default=None, env="CASHFREE_APP_ID")
    CASHFREE_SECRET_KEY: Optional[str] = Field(default=None, env="CASHFREE_SECRET_KEY")
    
    # Paytm
    PAYTM_MERCHANT_ID: Optional[str] = Field(default=None, env="PAYTM_MERCHANT_ID")
    PAYTM_MERCHANT_KEY: Optional[str] = Field(default=None, env="PAYTM_MERCHANT_KEY")
    PAYTM_ENVIRONMENT: str = Field(default="staging", env="PAYTM_ENVIRONMENT")
    
    # PhonePe
    PHONEPE_MERCHANT_ID: Optional[str] = Field(default=None, env="PHONEPE_MERCHANT_ID")
    PHONEPE_SALT_KEY: Optional[str] = Field(default=None, env="PHONEPE_SALT_KEY")
    PHONEPE_SALT_INDEX: int = Field(default=1, env="PHONEPE_SALT_INDEX")
    
    # Merchant UPI ID
    MERCHANT_UPI_ID: Optional[str] = Field(default=None, env="MERCHANT_UPI_ID")
    
    # Social Media Configuration
    TWITTER_API_KEY: Optional[str] = Field(default=None, env="TWITTER_API_KEY")
    TWITTER_API_SECRET: Optional[str] = Field(default=None, env="TWITTER_API_SECRET")
    TWITTER_ACCESS_TOKEN: Optional[str] = Field(default=None, env="TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET: Optional[str] = Field(default=None, env="TWITTER_ACCESS_TOKEN_SECRET")
    TWITTER_BEARER_TOKEN: Optional[str] = Field(default=None, env="TWITTER_BEARER_TOKEN")
    
    LINKEDIN_CLIENT_ID: Optional[str] = Field(default=None, env="LINKEDIN_CLIENT_ID")
    LINKEDIN_CLIENT_SECRET: Optional[str] = Field(default=None, env="LINKEDIN_CLIENT_SECRET")
    LINKEDIN_ACCESS_TOKEN: Optional[str] = Field(default=None, env="LINKEDIN_ACCESS_TOKEN")
    
    YOUTUBE_API_KEY: Optional[str] = Field(default=None, env="YOUTUBE_API_KEY")
    YOUTUBE_CHANNEL_ID: Optional[str] = Field(default=None, env="YOUTUBE_CHANNEL_ID")
    
    # Google Services
    GOOGLE_CLIENT_ID: Optional[str] = Field(default=None, env="GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = Field(default=None, env="GOOGLE_CLIENT_SECRET")
    GOOGLE_REFRESH_TOKEN: Optional[str] = Field(default=None, env="GOOGLE_REFRESH_TOKEN")
    
    GOOGLE_ANALYTICS_TRACKING_ID: Optional[str] = Field(default=None, env="GOOGLE_ANALYTICS_TRACKING_ID")
    GOOGLE_ANALYTICS_PROPERTY_ID: Optional[str] = Field(default=None, env="GOOGLE_ANALYTICS_PROPERTY_ID")
    
    GOOGLE_ADS_CUSTOMER_ID: Optional[str] = Field(default=None, env="GOOGLE_ADS_CUSTOMER_ID")
    GOOGLE_ADS_DEVELOPER_TOKEN: Optional[str] = Field(default=None, env="GOOGLE_ADS_DEVELOPER_TOKEN")
    
    # Email Configuration
    EMAIL_ENABLED: bool = Field(default=True, env="EMAIL_ENABLED")
    SMTP_HOST: str = Field(default="smtp.gmail.com", env="SMTP_HOST")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USER: Optional[str] = Field(default=None, env="SMTP_USER")
    SMTP_PASSWORD: Optional[str] = Field(default=None, env="SMTP_PASSWORD")
    SMTP_TLS: bool = Field(default=True, env="SMTP_TLS")
    FROM_EMAIL: Optional[str] = Field(default=None, env="FROM_EMAIL")
    
    # SMS Configuration
    SMS_ENABLED: bool = Field(default=True, env="SMS_ENABLED")
    SMS_PROVIDER: str = Field(default="aws_sns", env="SMS_PROVIDER")
    
    # AWS Configuration
    AWS_ACCESS_KEY_ID: Optional[str] = Field(default=None, env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: Optional[str] = Field(default=None, env="AWS_SECRET_ACCESS_KEY")
    AWS_REGION: str = Field(default="ap-south-1", env="AWS_REGION")
    AWS_S3_BUCKET: Optional[str] = Field(default=None, env="AWS_S3_BUCKET")
    
    # File Storage
    STORAGE_PROVIDER: str = Field(default="local", env="STORAGE_PROVIDER")
    UPLOAD_PATH: str = Field(default="./uploads", env="UPLOAD_PATH")
    MAX_FILE_SIZE_MB: int = Field(default=10, env="MAX_FILE_SIZE_MB")
    
    # Security
    JWT_SECRET_KEY: Optional[str] = Field(default=None, env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field(default="HS256", env="JWT_ALGORITHM")
    JWT_EXPIRATION_HOURS: int = Field(default=24, env="JWT_EXPIRATION_HOURS")
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = Field(default=True, env="RATE_LIMIT_ENABLED")
    RATE_LIMIT_REQUESTS_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_REQUESTS_PER_MINUTE")
    RATE_LIMIT_BURST_LIMIT: int = Field(default=10, env="RATE_LIMIT_BURST_LIMIT")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(default="json", env="LOG_FORMAT")
    LOG_FILE: str = Field(default="./logs/multiagent_manus.log", env="LOG_FILE")
    
    # Indian Business Specific
    BUSINESS_NAME: Optional[str] = Field(default=None, env="BUSINESS_NAME")
    BUSINESS_ADDRESS: Optional[str] = Field(default=None, env="BUSINESS_ADDRESS")
    BUSINESS_PHONE: Optional[str] = Field(default=None, env="BUSINESS_PHONE")
    BUSINESS_EMAIL: Optional[str] = Field(default=None, env="BUSINESS_EMAIL")
    BUSINESS_WEBSITE: Optional[str] = Field(default=None, env="BUSINESS_WEBSITE")
    
    # GST Configuration
    GST_NUMBER: Optional[str] = Field(default=None, env="GST_NUMBER")
    GST_ENABLED: bool = Field(default=True, env="GST_ENABLED")
    
    # Business Hours
    BUSINESS_START_TIME: str = Field(default="09:00", env="BUSINESS_START_TIME")
    BUSINESS_END_TIME: str = Field(default="18:00", env="BUSINESS_END_TIME")
    BUSINESS_TIMEZONE: str = Field(default="Asia/Kolkata", env="BUSINESS_TIMEZONE")
    
    # Languages
    DEFAULT_LANGUAGE: str = Field(default="hi", env="DEFAULT_LANGUAGE")
    SUPPORTED_LANGUAGES: str = Field(default="hi,en", env="SUPPORTED_LANGUAGES")
    
    # Regional Settings
    BUSINESS_STATE: Optional[str] = Field(default=None, env="BUSINESS_STATE")
    BUSINESS_CITY: Optional[str] = Field(default=None, env="BUSINESS_CITY")
    TARGET_REGIONS: Optional[str] = Field(default=None, env="TARGET_REGIONS")
    
    # Feature Flags
    FEATURE_AI_INSIGHTS: bool = Field(default=True, env="FEATURE_AI_INSIGHTS")
    FEATURE_AUTO_CAMPAIGNS: bool = Field(default=True, env="FEATURE_AUTO_CAMPAIGNS")
    FEATURE_BULK_WHATSAPP: bool = Field(default=True, env="FEATURE_BULK_WHATSAPP")
    FEATURE_MULTI_LANGUAGE: bool = Field(default=True, env="FEATURE_MULTI_LANGUAGE")
    FEATURE_FESTIVAL_CAMPAIGNS: bool = Field(default=True, env="FEATURE_FESTIVAL_CAMPAIGNS")
    
    # Quality Control
    QUALITY_CHECK_ENABLED: bool = Field(default=True, env="QUALITY_CHECK_ENABLED")
    
    # Performance
    MAX_CONCURRENT_REQUESTS: int = Field(default=100, env="MAX_CONCURRENT_REQUESTS")
    REQUEST_TIMEOUT_SECONDS: int = Field(default=30, env="REQUEST_TIMEOUT_SECONDS")
    DATABASE_POOL_SIZE: int = Field(default=20, env="DATABASE_POOL_SIZE")
    
    # Cache
    CACHE_ENABLED: bool = Field(default=True, env="CACHE_ENABLED")
    CACHE_TTL_SECONDS: int = Field(default=3600, env="CACHE_TTL_SECONDS")
    
    # API Configuration
    API_VERSION: str = Field(default="v1", env="API_VERSION")
    API_BASE_PATH: str = Field(default="/api/v1", env="API_BASE_PATH")
    
    # CORS
    CORS_ENABLED: bool = Field(default=True, env="CORS_ENABLED")
    CORS_ALLOWED_ORIGINS: str = Field(default="*", env="CORS_ALLOWED_ORIGINS")
    
    @property
    def supported_languages_list(self) -> List[str]:
        """Get list of supported languages."""
        return [lang.strip() for lang in self.SUPPORTED_LANGUAGES.split(",")]
    
    @property
    def target_regions_list(self) -> List[str]:
        """Get list of target regions."""
        if self.TARGET_REGIONS:
            return [region.strip() for region in self.TARGET_REGIONS.split(",")]
        return []
    
    @property
    def cors_allowed_origins_list(self) -> List[str]:
        """Get list of CORS allowed origins."""
        return [origin.strip() for origin in self.CORS_ALLOWED_ORIGINS.split(",")]
    
    def load_yaml_config(self, config_path: str = None) -> dict:
        """Load additional configuration from YAML file."""
        if config_path is None:
            config_path = Path(__file__).parent / "settings.yaml"
        
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            return {}
        except Exception as e:
            print(f"Error loading YAML config: {e}")
            return {}
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Create global settings instance
settings = Settings()

# Load YAML configuration
yaml_config = settings.load_yaml_config()

def get_agent_config(agent_name: str) -> dict:
    """Get configuration for a specific agent."""
    agents_config = yaml_config.get("agents", {})
    return agents_config.get(agent_name, {})

def get_business_config() -> dict:
    """Get business-specific configuration."""
    return yaml_config.get("business", {})

def get_whatsapp_config() -> dict:
    """Get WhatsApp configuration."""
    return yaml_config.get("whatsapp", {})

def get_payment_config() -> dict:
    """Get payment configuration."""
    return yaml_config.get("payments", {})

def get_social_media_config() -> dict:
    """Get social media configuration."""
    return yaml_config.get("social_media", {})

def get_analytics_config() -> dict:
    """Get analytics configuration."""
    return yaml_config.get("analytics", {})

def is_feature_enabled(feature_name: str) -> bool:
    """Check if a feature is enabled."""
    feature_map = {
        "ai_insights": settings.FEATURE_AI_INSIGHTS,
        "auto_campaigns": settings.FEATURE_AUTO_CAMPAIGNS,
        "bulk_whatsapp": settings.FEATURE_BULK_WHATSAPP,
        "multi_language": settings.FEATURE_MULTI_LANGUAGE,
        "festival_campaigns": settings.FEATURE_FESTIVAL_CAMPAIGNS,
    }
    return feature_map.get(feature_name, False)

def get_festival_config() -> dict:
    """Get Indian festival configuration."""
    business_config = get_business_config()
    return business_config.get("festivals", {})

def get_gst_rates() -> dict:
    """Get GST rates configuration."""
    payment_config = get_payment_config()
    return payment_config.get("gst", {}).get("rates", {})

def validate_required_settings():
    """Validate that required settings are present."""
    required_settings = [
        "SECRET_KEY",
        "DATABASE_URL",
        "DB_USER",
        "DB_PASSWORD"
    ]
    
    missing_settings = []
    for setting in required_settings:
        if not getattr(settings, setting, None):
            missing_settings.append(setting)
    
    if missing_settings:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_settings)}")

def get_provider_config(provider_type: str, provider_name: str) -> dict:
    """Get configuration for a specific provider."""
    provider_configs = {
        "payment": {
            "razorpay": {
                "key_id": settings.RAZORPAY_KEY_ID,
                "key_secret": settings.RAZORPAY_KEY_SECRET,
                "webhook_secret": settings.RAZORPAY_WEBHOOK_SECRET
            },
            "cashfree": {
                "app_id": settings.CASHFREE_APP_ID,
                "secret_key": settings.CASHFREE_SECRET_KEY
            },
            "paytm": {
                "merchant_id": settings.PAYTM_MERCHANT_ID,
                "merchant_key": settings.PAYTM_MERCHANT_KEY,
                "environment": settings.PAYTM_ENVIRONMENT
            },
            "phonepe": {
                "merchant_id": settings.PHONEPE_MERCHANT_ID,
                "salt_key": settings.PHONEPE_SALT_KEY,
                "salt_index": settings.PHONEPE_SALT_INDEX
            }
        },
        "social": {
            "facebook": {
                "app_id": settings.FACEBOOK_APP_ID,
                "app_secret": settings.FACEBOOK_APP_SECRET,
                "page_access_token": settings.FACEBOOK_PAGE_ACCESS_TOKEN,
                "page_id": settings.FACEBOOK_PAGE_ID
            },
            "twitter": {
                "api_key": settings.TWITTER_API_KEY,
                "api_secret": settings.TWITTER_API_SECRET,
                "access_token": settings.TWITTER_ACCESS_TOKEN,
                "access_token_secret": settings.TWITTER_ACCESS_TOKEN_SECRET,
                "bearer_token": settings.TWITTER_BEARER_TOKEN
            },
            "linkedin": {
                "client_id": settings.LINKEDIN_CLIENT_ID,
                "client_secret": settings.LINKEDIN_CLIENT_SECRET,
                "access_token": settings.LINKEDIN_ACCESS_TOKEN
            },
            "youtube": {
                "api_key": settings.YOUTUBE_API_KEY,
                "channel_id": settings.YOUTUBE_CHANNEL_ID
            }
        }
    }
    
    return provider_configs.get(provider_type, {}).get(provider_name, {})

# Validate settings on import
if settings.APP_ENV == "production":
    validate_required_settings()
