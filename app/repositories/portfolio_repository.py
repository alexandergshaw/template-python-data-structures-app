"""Data access layer for portfolio content backed by Supabase."""

from __future__ import annotations

import logging
from typing import Any

from app.domain.models import PortfolioItem
from app.repositories.base import PortfolioRepository

logger = logging.getLogger(__name__)


class SupabasePortfolioRepository(PortfolioRepository):
    """Repository responsible for reading portfolio records from Supabase.

    Implements graceful degradation: returns empty results when the client
    is unavailable rather than raising exceptions to the service layer.
    """

    TABLE_NAME = "portfolio_items"

    def __init__(self, client: Any | None) -> None:
        self._client = client

    def list_items(self) -> list[PortfolioItem]:
        """Return portfolio items ordered by creation date."""
        if self._client is None:
            return []

        try:
            response = (
                self._client.table(self.TABLE_NAME)
                .select("*")
                .order("created_at", desc=True)
                .execute()
            )
            records = getattr(response, "data", []) or []
            logger.debug("Fetched %d portfolio items from Supabase.", len(records))
            return [self._to_item(row) for row in records]
        except Exception:  # noqa: BLE001
            logger.exception("Failed to fetch portfolio items from Supabase.")
            return []

    def get_item_by_slug(self, slug: str) -> PortfolioItem | None:
        """Return a single portfolio item by slug."""
        if self._client is None:
            return None

        try:
            response = (
                self._client.table(self.TABLE_NAME)
                .select("*")
                .eq("slug", slug)
                .limit(1)
                .execute()
            )
            records = getattr(response, "data", []) or []
            if not records:
                return None
            return self._to_item(records[0])
        except Exception:  # noqa: BLE001
            logger.exception(
                "Failed to fetch portfolio item slug=%r from Supabase.", slug
            )
            return None

    @staticmethod
    def _to_item(row: dict[str, Any]) -> PortfolioItem:
        return PortfolioItem(
            slug=row.get("slug", "placeholder-project"),
            student_name=row.get("student_name", "Student Name"),
            title=row.get("title", "Project Title"),
            summary=row.get("summary", "Project summary placeholder."),
            project_url=row.get("project_url", "#"),
        )
