"""Data access layer for portfolio content backed by a local JSON file."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from app.domain.models import PortfolioItem
from app.repositories.base import PortfolioRepository

logger = logging.getLogger(__name__)


class JsonPortfolioRepository(PortfolioRepository):
    """Repository that reads portfolio records from a JSON file on disk.

    The JSON file must contain an object with a top-level ``projects`` list,
    where each entry has the keys ``slug``, ``student_name``, ``title``,
    ``summary``, and ``project_url``.

    Implements graceful degradation: returns empty results when the file is
    missing or malformed rather than raising exceptions to the service layer.
    """

    def __init__(self, source_path: str | Path) -> None:
        self._source_path = Path(source_path)

    def list_items(self) -> list[PortfolioItem]:
        """Return every portfolio item from the JSON source, preserving order."""
        records = self._load_records()
        logger.debug("Loaded %d portfolio items from %s.", len(records), self._source_path)
        return [self._to_item(row) for row in records]

    def get_item_by_slug(self, slug: str) -> PortfolioItem | None:
        """Return a single portfolio item matching ``slug`` or ``None``."""
        for row in self._load_records():
            if row.get("slug") == slug:
                return self._to_item(row)
        return None

    def _load_records(self) -> list[dict[str, Any]]:
        if not self._source_path.exists():
            logger.warning("Portfolio JSON file not found at %s.", self._source_path)
            return []

        try:
            with self._source_path.open("r", encoding="utf-8") as fh:
                payload = json.load(fh)
        except (OSError, json.JSONDecodeError):
            logger.exception("Failed to load portfolio JSON from %s.", self._source_path)
            return []

        projects = payload.get("projects") if isinstance(payload, dict) else None
        if not isinstance(projects, list):
            logger.warning(
                "Portfolio JSON at %s is missing a 'projects' list.", self._source_path
            )
            return []
        return [row for row in projects if isinstance(row, dict)]

    @staticmethod
    def _to_item(row: dict[str, Any]) -> PortfolioItem:
        return PortfolioItem(
            slug=row.get("slug", "placeholder-project"),
            student_name=row.get("student_name", "Student Name"),
            title=row.get("title", "Project Title"),
            summary=row.get("summary", "Project summary placeholder."),
            project_url=row.get("project_url", "#"),
        )
