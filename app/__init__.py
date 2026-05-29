"""Flask application factory."""

from __future__ import annotations

import logging
import os
import sys

from flask import Flask

from app.config import CONFIG_MAP
from app.repositories.portfolio_repository import JsonPortfolioRepository
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

    Uses APP_ENV to resolve config when *config_name* is not provided.
    """
    if config_name is None:
        config_name = os.getenv("APP_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(CONFIG_MAP.get(config_name, CONFIG_MAP["default"]))

    _configure_logging(app)

    # Wire up dependencies — projects are loaded from a JSON file on disk.
    repository = JsonPortfolioRepository(app.config["PROJECTS_JSON_PATH"])
    app.extensions["portfolio_repository"] = repository
    app.extensions["portfolio_service"] = PortfolioService(repository)

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
