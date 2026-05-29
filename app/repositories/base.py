"""Abstract base interfaces for repositories."""

from __future__ import annotations

import abc

from app.domain.models import PortfolioItem


class PortfolioRepository(abc.ABC):
    """Contract for any portfolio data-access implementation."""

    @abc.abstractmethod
    def list_items(self) -> list[PortfolioItem]:
        """Return all portfolio items."""

    @abc.abstractmethod
    def get_item_by_slug(self, slug: str) -> PortfolioItem | None:
        """Return a single portfolio item by slug, or None if not found."""
