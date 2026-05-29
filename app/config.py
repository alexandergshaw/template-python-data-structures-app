"""Application configuration objects."""

from __future__ import annotations

import os


class Config:
    """Base configuration shared across environments."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")

    # Supabase connection settings
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

    # Connection resilience
    SUPABASE_TIMEOUT: int = int(os.getenv("SUPABASE_TIMEOUT", "10"))
    SUPABASE_MAX_RETRIES: int = int(os.getenv("SUPABASE_MAX_RETRIES", "3"))

    TEMPLATES_AUTO_RELOAD = True


class DevelopmentConfig(Config):
    """Configuration for local development."""

    DEBUG = True


class ProductionConfig(Config):
    """Configuration for production deployments."""

    DEBUG = False
    TEMPLATES_AUTO_RELOAD = False


class TestingConfig(Config):
    """Configuration used by tests — no real Supabase connection."""

    TESTING = True
    SUPABASE_URL = ""
    SUPABASE_KEY = ""


CONFIG_MAP = {
    "default": Config,
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
