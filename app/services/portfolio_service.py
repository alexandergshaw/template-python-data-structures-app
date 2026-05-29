"""Business logic for student portfolio views."""

from __future__ import annotations

from app.domain.models import PortfolioItem
from app.repositories.portfolio_repository import SupabasePortfolioRepository


class PortfolioService:
    """Coordinates repository calls and applies placeholder defaults."""

    def __init__(self, repository: SupabasePortfolioRepository) -> None:
        self._repository = repository

    def list_portfolios(self) -> list[PortfolioItem]:
        """Return portfolio items with fallback placeholders."""
        items = self._repository.list_items()
        if items:
            return items

        return [
            PortfolioItem(
                slug="placeholder-project",
                student_name="Student Name",
                title="Project Title",
                summary="Add a short description of the work here.",
                project_url="#",
            )
        ]

    def get_portfolio(self, slug: str) -> PortfolioItem | None:
        """Find a portfolio item by slug."""
        for item in self.list_portfolios():
            if item.slug == slug:
                return item
        return None
