"""Application configuration objects."""

from __future__ import annotations

import os


class Config:
    """Base configuration shared across environments."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
    SUPABASE_TIMEOUT = int(os.getenv("SUPABASE_TIMEOUT", "10"))
    TEMPLATES_AUTO_RELOAD = True


class TestingConfig(Config):
    """Configuration used by tests."""

    TESTING = True


CONFIG_MAP = {
    "default": Config,
    "testing": TestingConfig,
}
