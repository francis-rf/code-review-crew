"""
Configuration settings for Code Review Crew
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)


class Settings:
    """Application settings"""

    # Application
    APP_NAME: str = "Code Review Crew API"
    APP_DESCRIPTION: str = "AI-Powered Code Review System with Multi-Agent Analysis"
    APP_VERSION: str = "1.0.0"

    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    RELOAD: bool = os.getenv("RELOAD", "true").lower() == "true"

    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    # LLM Configuration
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")  # openai or anthropic
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-5-nano")

    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    SRC_DIR: Path = Path(__file__).parent.parent
    CONFIG_DIR: Path = Path(__file__).parent
    OUTPUT_DIR: Path = BASE_DIR / "output"
    LOGS_DIR: Path = BASE_DIR / "logs"
    STATIC_DIR: Path = SRC_DIR / "static"

    # File Upload
    MAX_UPLOAD_SIZE: int = int(os.getenv("MAX_UPLOAD_SIZE", "10485760"))  # 10MB
    ALLOWED_EXTENSIONS: list = [".py"]

    # GitHub
    GITHUB_MAX_FILES: int = int(os.getenv("GITHUB_MAX_FILES", "50"))
    GITHUB_DEFAULT_FILES: int = int(os.getenv("GITHUB_DEFAULT_FILES", "5"))

    # CORS
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "*").split(",")

    # CrewAI
    CREW_VERBOSE: bool = os.getenv("CREW_VERBOSE", "true").lower() == "true"
    CREW_MEMORY: bool = os.getenv("CREW_MEMORY", "true").lower() == "true"
    CREW_CACHE: bool = os.getenv("CREW_CACHE", "true").lower() == "true"

    @classmethod
    def validate(cls) -> bool:
        """Validate required settings"""
        errors = []

        if not cls.OPENAI_API_KEY and not cls.ANTHROPIC_API_KEY:
            errors.append("At least one API key (OPENAI_API_KEY or ANTHROPIC_API_KEY) must be set")

        if cls.LLM_PROVIDER not in ["openai", "anthropic"]:
            errors.append(f"LLM_PROVIDER must be 'openai' or 'anthropic', got '{cls.LLM_PROVIDER}'")

        if cls.LLM_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required when LLM_PROVIDER is 'openai'")

        if cls.LLM_PROVIDER == "anthropic" and not cls.ANTHROPIC_API_KEY:
            errors.append("ANTHROPIC_API_KEY is required when LLM_PROVIDER is 'anthropic'")

        if errors:
            for error in errors:
                print(f"❌ Configuration Error: {error}")
            return False

        return True

    @classmethod
    def create_directories(cls) -> None:
        """Create necessary directories"""
        cls.OUTPUT_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)
        cls.STATIC_DIR.mkdir(exist_ok=True)



# Create singleton instance
settings = Settings()
