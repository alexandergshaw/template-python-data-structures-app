"""Extensions and external client helpers."""

from __future__ import annotations

from typing import Any


def create_supabase_client(url: str, key: str) -> Any | None:
    """Return a Supabase client when credentials are configured."""
    if not url or not key:
        return None

    try:
        from supabase import create_client
    except ImportError:
        return None

    return create_client(url, key)
