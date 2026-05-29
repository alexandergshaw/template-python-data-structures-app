"""Health check endpoint for monitoring app status."""

from __future__ import annotations

from pathlib import Path

from flask import Blueprint, current_app, jsonify

bp = Blueprint("health", __name__)


@bp.get("/health")
def health_check():
    """Return service health including the projects data source status."""
    source_path = Path(current_app.config.get("PROJECTS_JSON_PATH", ""))
    projects_status = "available" if source_path.is_file() else "missing"

    status = {
        "status": "healthy" if projects_status == "available" else "degraded",
        "projects": projects_status,
    }

    http_status = 200 if status["status"] == "healthy" else 503
    return jsonify(status), http_status
