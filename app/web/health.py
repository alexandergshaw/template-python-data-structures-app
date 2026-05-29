"""Health check endpoint for monitoring Supabase connectivity."""

from __future__ import annotations

from flask import Blueprint, current_app, jsonify

bp = Blueprint("health", __name__)


@bp.get("/health")
def health_check():
    """Return service health including Supabase connection status."""
    supabase = current_app.extensions.get("supabase")

    status = {
        "status": "healthy",
        "supabase": "connected" if supabase is not None else "disconnected",
    }

    # Perform a lightweight connectivity check when client is available
    if supabase is not None:
        try:
            # A minimal query to verify the connection is alive
            supabase.table("portfolio_items").select("slug").limit(1).execute()
        except Exception:  # noqa: BLE001
            status["supabase"] = "error"
            status["status"] = "degraded"

    http_status = 200 if status["status"] == "healthy" else 503
    return jsonify(status), http_status
