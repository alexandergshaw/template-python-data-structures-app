"""Extensions and external client helpers."""

from __future__ import annotations

import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


class SupabaseClientError(RuntimeError):
    """Raised when the Supabase client cannot be created."""


def create_supabase_client(
    url: str,
    key: str,
    *,
    timeout: int = 10,
    max_retries: int = 3,
) -> Any | None:
    """Return a Supabase client with retry logic and structured logging.

    Returns None when credentials are not provided (e.g. in testing).
    Raises SupabaseClientError if credentials are set but the client fails.
    """
    if not url or not key:
        logger.info("Supabase credentials not configured — running in offline mode.")
        return None

    try:
        from supabase import ClientOptions, create_client
    except ImportError as exc:
        raise SupabaseClientError(
            "The 'supabase' package is required but not installed."
        ) from exc

    last_exc: Exception | None = None
    for attempt in range(1, max_retries + 1):
        try:
            options = ClientOptions(
                postgrest_client_timeout=timeout,
            )
            client = create_client(url, key, options=options)
            logger.info(
                "Supabase client initialized successfully (attempt %d).", attempt
            )
            return client
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            logger.warning(
                "Supabase client creation attempt %d/%d failed: %s",
                attempt,
                max_retries,
                exc,
            )
            if attempt < max_retries:
                time.sleep(min(2**attempt, 8))

    raise SupabaseClientError(
        f"Failed to create Supabase client after {max_retries} attempts."
    ) from last_exc


def validate_supabase_config(url: str, key: str) -> list[str]:
    """Return a list of configuration issues (empty means valid)."""
    issues: list[str] = []

    if url and not url.startswith("https://"):
        issues.append("SUPABASE_URL should use HTTPS.")

    if url and not url.endswith(".supabase.co"):
        issues.append(
            "SUPABASE_URL does not match expected *.supabase.co pattern."
        )

    if key and len(key) < 20:
        issues.append("SUPABASE_KEY appears too short to be a valid key.")

    return issues
