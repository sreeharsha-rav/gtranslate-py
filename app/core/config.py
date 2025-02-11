"""
Application Configuration Module

This module defines the application's configuration settings using Pydantic's BaseSettings.
It handles environment variable loading, API versioning, and service-specific settings.

The configuration can be customized through environment variables or a .env file.
All settings are validated at startup to ensure proper configuration.

Environment Variables:
    - API_V1_STR: API version prefix
    - PROJECT_NAME: Name of the project
    - VERSION: API version
    - GOOGLE_PROJECT_ID: Google Cloud project ID
    - GOOGLE_APPLICATION_CREDENTIALS: Path to the Google Cloud service account key file
    """

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application Settings Class
    
    This class defines all configuration settings for the application.
    It uses Pydantic's BaseSettings for automatic environment variable loading
    and validation.
    
    Attributes:
        API_V1_STR (str): API version prefix for all endpoints
        PROJECT_NAME (str): Name of the project for documentation
        VERSION (str): Current API version
        GOOGLE_PROJECT_ID (str): Google Cloud project identifier
        GOOGLE_APPLICATION_CREDENTIALS (str): Path to the Google Cloud service account key file
    
    Note:
        All settings can be overridden through environment variables.
        The .env file is used as a fallback for local development.
    """
    
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Translation Service API"
    VERSION: str = "1.0.0"
    
    # Google Cloud settings
    GOOGLE_PROJECT_ID: str
    GOOGLE_APPLICATION_CREDENTIALS: str
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()


