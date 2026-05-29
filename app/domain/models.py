"""Domain models for portfolio items."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PortfolioItem:
    """Represents a student's project showcased in the portfolio."""

    slug: str
    student_name: str
    title: str
    summary: str
    project_url: str
