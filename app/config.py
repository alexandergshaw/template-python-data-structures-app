"""Application configuration objects."""

from __future__ import annotations

import os
from pathlib import Path


# Repository root (two levels up from this file: app/config.py -> app/ -> repo/)
_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_PROJECTS_PATH = _REPO_ROOT / "data" / "projects.json"


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

    # Path to the JSON file that holds all worked projects.
    PROJECTS_JSON_PATH: str = os.getenv(
        "PROJECTS_JSON_PATH", str(_DEFAULT_PROJECTS_PATH)
    )

    TEMPLATES_AUTO_RELOAD = True


class DevelopmentConfig(Config):
    """Configuration for local development."""

    DEBUG = True


class ProductionConfig(Config):
    """Configuration for production deployments."""

    DEBUG = False
    TEMPLATES_AUTO_RELOAD = False


class TestingConfig(Config):
    """Configuration used by tests."""

    TESTING = True


CONFIG_MAP = {
    "default": Config,
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
