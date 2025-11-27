import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if available
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

class Config:
    APP_NAME = "SentinelLog"
    VERSION = "0.1.0"

    # Logging directories
    LOG_DIR = os.getenv("SENTINEL_LOG_DIR", BASE_DIR / "../logs")
    RULES_FILE = os.getenv("SENTINEL_RULES_FILE", BASE_DIR / "rules/rules.yaml")

    # API settings
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))

    # Security
    API_KEY = os.getenv("API_KEY", "dev-key-change-in-prod")

    # Optional database URL for analytics
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///sentinel.db")

config = Config()