"""Application configuration objects."""

from __future__ import annotations

import os


class Config:
    """Base configuration shared across environments."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")

    # Single-student personalization. These power the headings, hero copy,
    # and contact section so the portfolio reads as one person's site.
    STUDENT_NAME: str = os.getenv("STUDENT_NAME", "Your Name")
    STUDENT_TAGLINE: str = os.getenv(
        "STUDENT_TAGLINE", "Student developer building things I'm proud of."
    )
    STUDENT_BIO: str = os.getenv(
        "STUDENT_BIO",
        "I'm a student developer using this portfolio to share the projects "
        "I've built, the things I'm learning, and the ideas I'm exploring.",
    )
    STUDENT_CONTACT_EMAIL: str = os.getenv("STUDENT_CONTACT_EMAIL", "hello@example.com")

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
