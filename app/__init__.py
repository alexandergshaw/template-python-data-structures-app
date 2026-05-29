"""Flask application factory."""

from __future__ import annotations

from flask import Flask

from app.config import CONFIG_MAP
from app.extensions import create_supabase_client
from app.repositories.portfolio_repository import SupabasePortfolioRepository
from app.services.portfolio_service import PortfolioService
from app.web.routes import bp as portfolio_blueprint


def create_app(config_name: str = "default") -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(CONFIG_MAP[config_name])

    supabase_client = create_supabase_client(
        app.config["SUPABASE_URL"],
        app.config["SUPABASE_KEY"],
    )

    app.extensions["supabase"] = supabase_client
    app.extensions["portfolio_service"] = PortfolioService(
        SupabasePortfolioRepository(supabase_client)
    )

    app.register_blueprint(portfolio_blueprint)

    return app
