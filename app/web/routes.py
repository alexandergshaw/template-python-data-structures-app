"""HTTP routes for the portfolio website."""

from __future__ import annotations

from flask import Blueprint, abort, current_app, render_template

bp = Blueprint("portfolio", __name__)


@bp.get("/")
def home():
    service = current_app.extensions["portfolio_service"]
    portfolios = service.list_portfolios()
    return render_template("portfolio/index.html", portfolios=portfolios)


@bp.get("/students/<slug>")
def student_project(slug: str):
    service = current_app.extensions["portfolio_service"]
    item = service.get_portfolio(slug)
    if item is None:
        abort(404)

    return render_template("portfolio/detail.html", item=item)
