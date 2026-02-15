"""Application settings loaded from environment variables."""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Centralized config sourced from .env."""

    # OpenAI
    OPENAI_API_KEY = os.getenv("LLM_API_KEY")
    OPENAI_MODEL = "gpt-5.2-2025-12-11"

    # App
    APP_NAME = "MindVault"
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

settings = Settings()
