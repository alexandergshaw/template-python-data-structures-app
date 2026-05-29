"""Data access layer for portfolio content."""

from __future__ import annotations

from typing import Any

from app.domain.models import PortfolioItem


class SupabasePortfolioRepository:
    """Repository responsible for reading portfolio records from Supabase."""

    def __init__(self, client: Any | None) -> None:
        self._client = client

    def list_items(self) -> list[PortfolioItem]:
        """Return portfolio items, or placeholders if backend is not configured."""
        if self._client is None:
            return []

        response = self._client.table("portfolio_items").select("*").execute()
        records = getattr(response, "data", []) or []
        items: list[PortfolioItem] = []

        for row in records:
            items.append(self._to_item(row))

        return items

    def get_item_by_slug(self, slug: str) -> PortfolioItem | None:
        """Return a single portfolio item by slug."""
        if self._client is None:
            return None

        response = (
            self._client.table("portfolio_items")
            .select("*")
            .eq("slug", slug)
            .limit(1)
            .execute()
        )
        records = getattr(response, "data", []) or []
        if not records:
            return None
        return self._to_item(records[0])

    @staticmethod
    def _to_item(row: dict[str, Any]) -> PortfolioItem:
        return PortfolioItem(
            slug=row.get("slug", "placeholder-project"),
            student_name=row.get("student_name", "Student Name"),
            title=row.get("title", "Project Title"),
            summary=row.get("summary", "Project summary placeholder."),
            project_url=row.get("project_url", "#"),
        )
