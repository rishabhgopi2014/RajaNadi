"""
Configuration settings for Rajanadi Astrology Application
"""
from pydantic import BaseModel
from pathlib import Path

class Settings(BaseModel):
    """Application settings"""
    # Application Settings
    APP_NAME: str = "Rajanadi Astro"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # Ollama Settings
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"
    
    # File Paths
    KNOWLEDGE_BASE_PATH: Path = Path(__file__).parent.parent / "knowledge_base" / "RajaNadiRules.txt"
    
    # Calculation Settings
    LAHIRI_AYANAMSA: bool = True  # Use Lahiri ayanamsa for Vedic calculations
    
    # CORS Settings
    ALLOW_ORIGINS: list = ["*"]  # Update this for production
    
    class Config:
        env_file = ".env"

settings = Settings()
