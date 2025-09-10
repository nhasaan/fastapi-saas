from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Config Vault Service"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/config-vault/v1"
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/config_vault"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    BACKEND_CORS_ORIGIN_REGEX: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
