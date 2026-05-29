"""Flask application factory."""

from __future__ import annotations

import logging
import os
import sys

from flask import Flask

from app.config import CONFIG_MAP
from app.extensions import (
    SupabaseClientError,
    create_supabase_client,
    validate_supabase_config,
)
from app.repositories.portfolio_repository import SupabasePortfolioRepository
from app.services.portfolio_service import PortfolioService
from app.web.routes import bp as portfolio_blueprint
from app.web.health import bp as health_blueprint


def _configure_logging(app: Flask) -> None:
    """Set up structured logging with appropriate levels."""
    level = logging.DEBUG if app.debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
    )


def create_app(config_name: str | None = None) -> Flask:
    """Create and configure the Flask application.

    Uses FLASK_ENV to resolve config when *config_name* is not provided.
    """
    if config_name is None:
        config_name = os.getenv("APP_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(CONFIG_MAP.get(config_name, CONFIG_MAP["default"]))

    _configure_logging(app)
    logger = logging.getLogger(__name__)

    # Validate Supabase configuration early
    url: str = app.config["SUPABASE_URL"]
    key: str = app.config["SUPABASE_KEY"]

    config_issues = validate_supabase_config(url, key)
    for issue in config_issues:
        logger.warning("Supabase config: %s", issue)

    # Initialize Supabase client with retry logic
    supabase_client = None
    if not app.config.get("TESTING"):
        try:
            supabase_client = create_supabase_client(
                url,
                key,
                timeout=app.config.get("SUPABASE_TIMEOUT", 10),
                max_retries=app.config.get("SUPABASE_MAX_RETRIES", 3),
            )
        except SupabaseClientError:
            logger.exception("Supabase client initialization failed.")
    else:
        logger.info("Testing mode — Supabase client disabled.")

    # Wire up dependencies
    app.extensions["supabase"] = supabase_client
    app.extensions["portfolio_service"] = PortfolioService(
        SupabasePortfolioRepository(supabase_client)
    )

    # Register blueprints
    app.register_blueprint(portfolio_blueprint)
    app.register_blueprint(health_blueprint)

    # Make single-student personalization available to every template.
    @app.context_processor
    def _inject_student_identity() -> dict:
        return {
            "student_name": app.config.get("STUDENT_NAME", "Your Name"),
            "student_tagline": app.config.get("STUDENT_TAGLINE", ""),
            "student_bio": app.config.get("STUDENT_BIO", ""),
            "student_contact_email": app.config.get(
                "STUDENT_CONTACT_EMAIL", "hello@example.com"
            ),
        }

    return app
