"""Business logic for student portfolio views."""

from __future__ import annotations

from app.domain.models import PortfolioItem
from app.repositories.base import PortfolioRepository
from data_structures.assignment1 import array, linked_list


class PortfolioService:
    """Coordinates repository calls and applies placeholder defaults."""

    PLACEHOLDER_SLUG = "placeholder-project"

    def __init__(self, repository: PortfolioRepository) -> None:
        self._repository = repository

    def list_portfolios(self) -> list[PortfolioItem]:
        """Return portfolio items with fallback placeholders.

        Uses the ``array`` data structure to store and retrieve items.
        Falls back to a direct list return until ``array`` is implemented.
        """
        raw = self._repository.list_items()
        if not raw:
            raw = [
                PortfolioItem(
                    slug=self.PLACEHOLDER_SLUG,
                    student_name="Student Name",
                    title="Project Title",
                    summary="Add a short description of the work here.",
                    project_url="#",
                )
            ]

        try:
            items_array = array(len(raw))
            for item in raw:
                items_array.append(item)
            return [items_array.get(i) for i in range(len(items_array))]
        except NotImplementedError:
            return raw

    def get_portfolio(self, slug: str) -> PortfolioItem | None:
        """Find a portfolio item by slug.

        Uses the ``linked_list`` data structure to locate the slug before
        fetching the full record. Falls back to a direct repository lookup
        until ``linked_list`` is implemented.
        """
        all_items = self._repository.list_items()

        try:
            slugs = linked_list()
            for item in all_items:
                slugs.append(item.slug)
            if slugs.find(slug):
                return self._repository.get_item_by_slug(slug)
            if slug == self.PLACEHOLDER_SLUG:
                return self.list_portfolios()[0]
            return None
        except NotImplementedError:
            item = self._repository.get_item_by_slug(slug)
            if item is not None:
                return item
            if slug == self.PLACEHOLDER_SLUG:
                return self.list_portfolios()[0]
            return None
