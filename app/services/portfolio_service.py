"""Business logic for student portfolio views.

This module wires every data structure from ``data_structures/assignment1``
through ``assignment10`` into the portfolio flow.  Each integration follows
the same pattern: use the data structure's member functions to derive a
value the templates can render, and fall back to a plain implementation if
the structure has not been implemented yet (``NotImplementedError``).
"""

from __future__ import annotations

from app.domain.models import PortfolioItem
from app.repositories.base import PortfolioRepository
from data_structures.assignment1 import array, linked_list
from data_structures.assignment2 import queue, stack
from data_structures.assignment3 import bubble_sort, merge_sort
from data_structures.assignment4 import binary_search, linear_search
from data_structures.assignment5 import factorial, permutations
from data_structures.assignment6 import hash_table
from data_structures.assignment7 import binary_tree, min_heap
from data_structures.assignment8 import avl_tree, trie
from data_structures.assignment9 import bfs_pathfinder, graph
from data_structures.assignment10 import dijkstra, topological_sort


class PortfolioService:
    """Coordinates repository calls and applies placeholder defaults."""

    PLACEHOLDER_SLUG = "placeholder-project"
    # Caps to keep recursive/exponential structures inexpensive for the view.
    _FACTORIAL_CAP = 10
    _PERMUTATION_CAP = 4

    def __init__(self, repository: PortfolioRepository) -> None:
        self._repository = repository
        # assignment2 — long-lived per-app collections used to back history
        # and a background-processing queue.  They survive between requests
        # because the service is created once during ``create_app``.
        self._history: stack = stack()
        self._processing: queue = queue()
        # assignment6 — in-memory slug → PortfolioItem cache.
        self._cache: hash_table = hash_table()

    # ------------------------------------------------------------------
    # assignment1 — array / linked_list
    # ------------------------------------------------------------------
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

        Combines ``linked_list`` (assignment 1) for slug existence checks
        and ``hash_table`` (assignment 6) as a fetch cache.  Successful
        lookups are pushed onto the ``stack`` (assignment 2) history and
        enqueued on the processing ``queue`` (assignment 2) so other parts
        of the app can observe browsing behaviour.
        """
        all_items = self.list_portfolios()

        try:
            slugs = linked_list()
            for item in all_items:
                slugs.append(item.slug)
            exists = slugs.find(slug)
        except NotImplementedError:
            exists = any(item.slug == slug for item in all_items)

        if not exists:
            if slug == self.PLACEHOLDER_SLUG:
                item = all_items[0]
            else:
                return None
        else:
            item = self._lookup_with_cache(slug, all_items)
            if item is None and slug == self.PLACEHOLDER_SLUG:
                item = all_items[0]
            if item is None:
                return None

        self._record_visit(slug)
        return item

    def _lookup_with_cache(
        self, slug: str, all_items: list[PortfolioItem]
    ) -> PortfolioItem | None:
        """Return a ``PortfolioItem`` by slug, populating the cache."""
        try:
            cached = self._cache.get(slug)
            if cached is not None:
                return cached
        except NotImplementedError:
            cached = None

        fetched = self._repository.get_item_by_slug(slug)
        if fetched is None:
            # Fall back to the in-memory list (covers the placeholder).
            for item in all_items:
                if item.slug == slug:
                    fetched = item
                    break

        if fetched is not None:
            try:
                self._cache.put(slug, fetched)
            except NotImplementedError:
                pass
        return fetched

    def _record_visit(self, slug: str) -> None:
        """Push the visited slug onto the history stack and processing queue."""
        try:
            self._history.push(slug)
        except NotImplementedError:
            pass
        try:
            self._processing.enqueue(slug)
        except NotImplementedError:
            pass

    # ------------------------------------------------------------------
    # assignment2 — stack / queue
    # ------------------------------------------------------------------
    def recently_viewed(self, limit: int = 5) -> list[str]:
        """Return the most recently viewed slugs, newest first.

        Drains the history stack to read every entry (since ``stack`` has
        no iterator), then restores it by re-pushing in original order.
        """
        try:
            buffered: list[str] = []
            while len(self._history) > 0:
                buffered.append(self._history.pop())
            for value in reversed(buffered):
                self._history.push(value)
            return buffered[:limit]
        except NotImplementedError:
            return []

    def next_in_processing_queue(self) -> str | None:
        """Peek at the next slug awaiting background processing."""
        try:
            if len(self._processing) == 0:
                return None
            return self._processing.peek()
        except NotImplementedError:
            return None

    # ------------------------------------------------------------------
    # assignment3 — bubble_sort / merge_sort
    # ------------------------------------------------------------------
    def list_portfolios_sorted_by_title(self) -> list[PortfolioItem]:
        """Sort portfolios alphabetically by title using ``merge_sort``."""
        items = self.list_portfolios()
        try:
            return merge_sort(key=lambda item: (item.title or "").lower()).sort(items)
        except NotImplementedError:
            return sorted(items, key=lambda item: (item.title or "").lower())

    def list_portfolios_sorted_by_student(self) -> list[PortfolioItem]:
        """Sort portfolios alphabetically by student name using ``bubble_sort``."""
        items = self.list_portfolios()
        try:
            return bubble_sort(
                key=lambda item: (item.student_name or "").lower()
            ).sort(items)
        except NotImplementedError:
            return sorted(items, key=lambda item: (item.student_name or "").lower())

    # ------------------------------------------------------------------
    # assignment4 — linear_search / binary_search
    # ------------------------------------------------------------------
    def find_index_linear(self, slug: str) -> int:
        """Return the index of ``slug`` in the unsorted listing, or -1."""
        items = self.list_portfolios()
        try:
            return linear_search(key=lambda item: item.slug).search(items, slug)
        except NotImplementedError:
            for i, item in enumerate(items):
                if item.slug == slug:
                    return i
            return -1

    def find_index_binary(self, slug: str) -> int:
        """Return the index of ``slug`` in the slug-sorted listing, or -1."""
        items = sorted(self.list_portfolios(), key=lambda item: item.slug)
        try:
            return binary_search(key=lambda item: item.slug).search(items, slug)
        except NotImplementedError:
            lo, hi = 0, len(items) - 1
            while lo <= hi:
                mid = (lo + hi) // 2
                if items[mid].slug == slug:
                    return mid
                if items[mid].slug < slug:
                    lo = mid + 1
                else:
                    hi = mid - 1
            return -1

    # ------------------------------------------------------------------
    # assignment5 — factorial / permutations
    # ------------------------------------------------------------------
    def ordering_count(self) -> int:
        """Return ``n!`` for the current portfolio count, capped for safety."""
        n = min(len(self.list_portfolios()), self._FACTORIAL_CAP)
        try:
            return factorial().compute(n)
        except NotImplementedError:
            result = 1
            for i in range(2, n + 1):
                result *= i
            return result

    def sample_ordering(self) -> list[str]:
        """Return one permutation of the first few slugs (demo of ``permutations``)."""
        slugs = [item.slug for item in self.list_portfolios()[: self._PERMUTATION_CAP]]
        if not slugs:
            return []
        try:
            orderings = permutations().generate(slugs)
        except NotImplementedError:
            return list(slugs)
        return orderings[0] if orderings else list(slugs)

    # ------------------------------------------------------------------
    # assignment6 — hash_table  (used inside ``get_portfolio`` cache above)
    # ------------------------------------------------------------------
    def invalidate_cache(self, slug: str) -> bool:
        """Drop ``slug`` from the cache so the next fetch re-reads it."""
        try:
            return self._cache.remove(slug)
        except NotImplementedError:
            return False

    # ------------------------------------------------------------------
    # assignment7 — binary_tree / min_heap
    # ------------------------------------------------------------------
    def slugs_alphabetical(self) -> list[str]:
        """Return every slug in ascending order via a BST in-order walk."""
        slugs = [item.slug for item in self.list_portfolios()]
        try:
            tree = binary_tree()
            for slug in slugs:
                tree.insert(slug)
            return tree.inorder()
        except NotImplementedError:
            return sorted(slugs)

    def next_featured_slug(self) -> str | None:
        """Return the slug that sorts first by ``(student_name, slug)``.

        Uses a ``min_heap`` keyed on ``(student_name, slug)`` tuples so the
        smallest pair sits at the root and can be peeked in O(1) time.
        """
        items = self.list_portfolios()
        if not items:
            return None
        try:
            heap = min_heap()
            for item in items:
                heap.push((item.student_name or "", item.slug))
            return heap.peek()[1]
        except NotImplementedError:
            return min(items, key=lambda item: (item.student_name or "", item.slug)).slug

    # ------------------------------------------------------------------
    # assignment8 — avl_tree / trie
    # ------------------------------------------------------------------
    def slug_known_balanced(self, slug: str) -> bool:
        """Use an ``avl_tree`` of slugs to check membership in O(log n)."""
        try:
            tree = avl_tree()
            for item in self.list_portfolios():
                tree.insert(item.slug)
            return tree.contains(slug)
        except NotImplementedError:
            return any(item.slug == slug for item in self.list_portfolios())

    def autocomplete_prefix(self, prefix: str) -> bool:
        """Return ``True`` if any slug begins with ``prefix`` via a ``trie``."""
        try:
            t = trie()
            for item in self.list_portfolios():
                t.insert(item.slug)
            return t.starts_with(prefix)
        except NotImplementedError:
            return any(item.slug.startswith(prefix) for item in self.list_portfolios())

    # ------------------------------------------------------------------
    # assignment9 — graph / bfs_pathfinder
    # ------------------------------------------------------------------
    def _build_related_graph(self) -> tuple[object, list[PortfolioItem]]:
        """Build an undirected graph that connects items sharing a student."""
        items = self.list_portfolios()
        g = graph()
        for item in items:
            g.add_node(item.slug)
        # Connect items whose ``student_name`` matches.
        by_student: dict[str, list[str]] = {}
        for item in items:
            by_student.setdefault(item.student_name or "", []).append(item.slug)
        for slugs in by_student.values():
            for i in range(len(slugs)):
                for j in range(i + 1, len(slugs)):
                    g.add_edge(slugs[i], slugs[j])
        # Also chain items in listing order so single-student datasets still
        # produce some connectivity for the BFS demo.
        for a, b in zip([i.slug for i in items], [i.slug for i in items][1:]):
            g.add_edge(a, b)
        return g, items

    def related_slugs(self, slug: str) -> list[str]:
        """Return slugs directly connected to ``slug`` in the related graph."""
        try:
            g, _ = self._build_related_graph()
            if slug not in g.nodes():
                return []
            return sorted(g.neighbors(slug))
        except NotImplementedError:
            return []

    def navigation_chain(self, start_slug: str, goal_slug: str) -> list[str]:
        """Return the BFS shortest chain of related slugs from start to goal."""
        try:
            g, _ = self._build_related_graph()
            path = bfs_pathfinder().shortest_path(g, start_slug, goal_slug)
            return path or []
        except NotImplementedError:
            return []

    # ------------------------------------------------------------------
    # assignment10 — dijkstra / topological_sort
    # ------------------------------------------------------------------
    def _build_weighted_adjacency(self) -> dict[str, dict[str, int]]:
        """Build a weighted directed adjacency keyed by slug.

        Weights are the absolute difference in title length between
        neighbours, giving each pair a small non-negative weight.
        """
        items = self.list_portfolios()
        adjacency: dict[str, dict[str, int]] = {item.slug: {} for item in items}
        for i in range(len(items) - 1):
            a, b = items[i], items[i + 1]
            weight = abs(len(a.title or "") - len(b.title or "")) or 1
            adjacency[a.slug][b.slug] = weight
            adjacency[b.slug][a.slug] = weight
        return adjacency

    def similarity_distances(self, start_slug: str) -> dict[str, int]:
        """Return Dijkstra distances from ``start_slug`` to every reachable slug."""
        adjacency = self._build_weighted_adjacency()
        if start_slug not in adjacency:
            return {}
        try:
            return dijkstra().shortest_paths(adjacency, start_slug)
        except NotImplementedError:
            return {start_slug: 0}

    def prerequisite_order(self) -> list[str]:
        """Return a topological ordering of slugs.

        Treats the listing order as a chain of prerequisites
        (``slug_i`` must come before ``slug_{i+1}``) and feeds the resulting
        DAG to ``topological_sort``.
        """
        items = self.list_portfolios()
        if not items:
            return []
        adjacency: dict[str, list[str]] = {item.slug: [] for item in items}
        for i in range(len(items) - 1):
            adjacency[items[i].slug].append(items[i + 1].slug)
        try:
            return topological_sort().order(adjacency)
        except NotImplementedError:
            return [item.slug for item in items]
