"""Business logic for student portfolio views."""

from __future__ import annotations

from app.domain.models import PortfolioItem
from app.repositories.base import PortfolioRepository


class PortfolioService:
    """Coordinates repository calls and applies placeholder defaults."""

    PLACEHOLDER_SLUG = "placeholder-project"

    def __init__(self, repository: PortfolioRepository) -> None:
        self._repository = repository

    def list_portfolios(self) -> list[PortfolioItem]:
        """Return portfolio items with fallback placeholders."""
        items = self._repository.list_items()
        if items:
            return items

        return [
            PortfolioItem(
                slug=self.PLACEHOLDER_SLUG,
                student_name="Student Name",
                title="Project Title",
                summary="Add a short description of the work here.",
                project_url="#",
            )
        ]

    def get_portfolio(self, slug: str) -> PortfolioItem | None:
        """Find a portfolio item by slug."""
        item = self._repository.get_item_by_slug(slug)
        if item is not None:
            return item

        if slug == self.PLACEHOLDER_SLUG:
            return self.list_portfolios()[0]

        return None
