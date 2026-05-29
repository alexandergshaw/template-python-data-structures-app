"""HTTP routes for the portfolio website."""

from __future__ import annotations

from flask import Blueprint, abort, current_app, render_template

bp = Blueprint("portfolio", __name__)


@bp.get("/")
def home():
    service = current_app.extensions["portfolio_service"]
    portfolios = service.list_portfolios()

    # Extra context derived from the assignment 2-10 data structures.
    sorted_by_title = service.list_portfolios_sorted_by_title()
    sorted_by_student = service.list_portfolios_sorted_by_student()
    alphabetical_slugs = service.slugs_alphabetical()
    prerequisite_order = service.prerequisite_order()
    featured_next = service.next_featured_slug()
    ordering_count = service.ordering_count()
    sample_ordering = service.sample_ordering()
    autocomplete_prefix = (portfolios[0].slug[:2] if portfolios else "")
    autocomplete_hit = service.autocomplete_prefix(autocomplete_prefix)
    next_in_queue = service.next_in_processing_queue()

    return render_template(
        "portfolio/index.html",
        portfolios=portfolios,
        sorted_by_title=sorted_by_title,
        sorted_by_student=sorted_by_student,
        alphabetical_slugs=alphabetical_slugs,
        prerequisite_order=prerequisite_order,
        featured_next=featured_next,
        ordering_count=ordering_count,
        sample_ordering=sample_ordering,
        autocomplete_prefix=autocomplete_prefix,
        autocomplete_hit=autocomplete_hit,
        next_in_queue=next_in_queue,
    )


@bp.get("/students/<slug>")
def portfolio_detail(slug: str):
    service = current_app.extensions["portfolio_service"]
    item = service.get_portfolio(slug)
    if item is None:
        abort(404)

    # Extra context derived from the assignment 2-10 data structures.
    recently_viewed = service.recently_viewed()
    related = service.related_slugs(slug)
    distances = service.similarity_distances(slug)
    linear_index = service.find_index_linear(slug)
    binary_index = service.find_index_binary(slug)
    known_balanced = service.slug_known_balanced(slug)
    chain_target = related[0] if related else slug
    navigation_chain = service.navigation_chain(slug, chain_target)

    return render_template(
        "portfolio/detail.html",
        item=item,
        recently_viewed=recently_viewed,
        related=related,
        distances=distances,
        linear_index=linear_index,
        binary_index=binary_index,
        known_balanced=known_balanced,
        navigation_chain=navigation_chain,
    )
