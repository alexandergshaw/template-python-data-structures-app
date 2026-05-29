"""HTTP routes for the portfolio website.

Each per-feature value passed to the templates is either the data that
feature produces or ``None`` to indicate that the underlying data structure
has not been implemented yet.  Templates omit any section whose value is
``None`` so the page gradually comes online as students complete each
assignment.
"""

from __future__ import annotations

from flask import Blueprint, abort, current_app, render_template

bp = Blueprint("portfolio", __name__)


@bp.get("/")
def home():
    service = current_app.extensions["portfolio_service"]
    portfolios = service.list_portfolios()
    autocomplete_prefix = portfolios[0].slug[:2] if portfolios else ""

    return render_template(
        "portfolio/index.html",
        portfolios=portfolios,
        # assignment 1
        array_slug_view=service.array_slug_view(),
        linked_slug_chain=service.linked_slug_chain(),
        # assignment 2
        next_in_queue=service.next_in_processing_queue(),
        # assignment 3
        sorted_by_title=service.list_portfolios_sorted_by_title(),
        sorted_by_student=service.list_portfolios_sorted_by_student(),
        # assignment 5
        ordering_count=service.ordering_count(),
        sample_ordering=service.sample_ordering(),
        # assignment 6
        slug_directory=service.slug_directory(),
        # assignment 7
        alphabetical_slugs=service.slugs_alphabetical(),
        featured_next=service.next_featured_slug(),
        # assignment 8
        autocomplete_prefix=autocomplete_prefix,
        autocomplete_hit=service.autocomplete_prefix(autocomplete_prefix),
        # assignment 10
        prerequisite_order=service.prerequisite_order(),
    )


@bp.get("/students/<slug>")
def portfolio_detail(slug: str):
    service = current_app.extensions["portfolio_service"]
    item = service.get_portfolio(slug)
    if item is None:
        abort(404)

    related = service.related_slugs(slug)
    # Pick a chain target from the graph-derived related list if available;
    # otherwise fall back to the slug itself so the BFS feature can still run.
    chain_target = related[0] if related else slug

    return render_template(
        "portfolio/detail.html",
        item=item,
        # assignment 2
        recently_viewed=service.recently_viewed(),
        # assignment 4
        linear_index=service.find_index_linear(slug),
        binary_index=service.find_index_binary(slug),
        # assignment 8
        known_balanced=service.slug_known_balanced(slug),
        # assignment 9
        related=related,
        navigation_chain=service.navigation_chain(slug, chain_target),
        # assignment 10
        distances=service.similarity_distances(slug),
    )
