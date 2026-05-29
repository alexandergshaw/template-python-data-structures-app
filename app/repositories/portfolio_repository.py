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
            items.append(
                PortfolioItem(
                    slug=row.get("slug", "placeholder-project"),
                    student_name=row.get("student_name", "Student Name"),
                    title=row.get("title", "Project Title"),
                    summary=row.get("summary", "Project summary placeholder."),
                    project_url=row.get("project_url", "#"),
                )
            )

        return items
