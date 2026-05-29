"""Business logic for student portfolio views.

Each data structure from ``data_structures/assignment1`` through
``assignment10`` is wired into **exactly one** frontend feature.  There is
no stdlib fallback: if a data structure has not been implemented yet (its
methods still raise ``NotImplementedError``), the corresponding feature
returns a sentinel value (``None`` or ``[]``) and the template hides that
section.  As students complete each data structure, its feature gradually
comes online without affecting any other part of the page.

Feature ↔ data-structure mapping:

==========================  ================================================
Data structure              Frontend feature
==========================  ================================================
``array``                   Array view of slugs (index page)
``linked_list``             Linked-list slug chain (index page)
``stack``                   Recently-viewed history (detail page)
``queue``                   Next slug in processing queue (index page)
``bubble_sort``             Portfolios sorted by student name (index page)
``merge_sort``              Portfolios sorted by title — project cards (index)
``linear_search``           Linear-search index lookup (detail page)
``binary_search``           Binary-search index lookup (detail page)
``factorial``               n! possible orderings (index page)
``permutations``            Sample permutation (index page)
``hash_table``              Slug → title directory (index page)
``binary_tree``             Alphabetical slugs via BST in-order (index page)
``min_heap``                Next featured slug via min-heap peek (index page)
``avl_tree``                Slug known to AVL membership check (detail page)
``trie``                    Autocomplete prefix check (index page)
``graph``                   Related projects (detail page)
``bfs_pathfinder``          BFS navigation chain (detail page)
``dijkstra``                Similarity distances (detail page)
``topological_sort``        Prerequisite order (index page)
==========================  ================================================
"""

from __future__ import annotations

from typing import Callable, TypeVar

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


T = TypeVar("T")


def _feature(default: T, fn: Callable[[], T]) -> T:
    """Run ``fn`` and return ``default`` when its data structure isn't ready.

    Catching ``NotImplementedError`` here is **not** a fallback that
    re-computes the feature using stdlib code — it simply signals that the
    feature is offline so the template can omit it.
    """
    try:
        return fn()
    except NotImplementedError:
        return default


class PortfolioService:
    """Coordinates repository calls and per-feature data-structure usage."""

    PLACEHOLDER_SLUG = "placeholder-project"
    # Caps to keep recursive/exponential structures inexpensive for the view.
    _FACTORIAL_CAP = 10
    _PERMUTATION_CAP = 4

    def __init__(self, repository: PortfolioRepository) -> None:
        self._repository = repository
        # Long-lived per-app collections used to back history (``stack``) and
        # a background-processing queue (``queue``).  They survive between
        # requests because the service is created once during ``create_app``.
        self._history: stack = stack()
        self._processing: queue = queue()

    # ------------------------------------------------------------------
    # Core data flow — pure repository pass-through.
    #
    # Neither of these methods uses a data structure: the page must load
    # even when no assignment has been completed yet.  Data-structure
    # features are layered on top via the methods below.
    # ------------------------------------------------------------------
    def list_portfolios(self) -> list[PortfolioItem]:
        """Return portfolio items, substituting a placeholder when empty."""
        raw = self._repository.list_items()
        if raw:
            return list(raw)
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
        """Look up a portfolio item by slug from the repository.

        Records the visit on the stack/queue collections so the
        stack- and queue-powered features have data to display, but the
        lookup itself never depends on a data structure.
        """
        item = self._repository.get_item_by_slug(slug)
        if item is None:
            for candidate in self.list_portfolios():
                if candidate.slug == slug:
                    item = candidate
                    break
        if item is None:
            return None

        # Best-effort visit recording — these only succeed once the
        # stack / queue assignments are complete.
        _feature(None, lambda: self._history.push(slug))
        _feature(None, lambda: self._processing.enqueue(slug))
        return item

    # ------------------------------------------------------------------
    # assignment1 — ``array``
    # ------------------------------------------------------------------
    def array_slug_view(self) -> list[str] | None:
        """Return slugs round-tripped through a fixed-capacity ``array``."""
        items = self.list_portfolios()

        def build() -> list[str]:
            slots = array(len(items))
            for item in items:
                slots.append(item.slug)
            return [slots.get(i) for i in range(len(slots))]

        return _feature(None, build)

    # ------------------------------------------------------------------
    # assignment1 — ``linked_list``
    # ------------------------------------------------------------------
    def linked_slug_chain(self) -> list[str] | None:
        """Return slugs walked out of a singly ``linked_list``."""
        items = self.list_portfolios()

        def build() -> list[str]:
            chain = linked_list()
            for item in items:
                chain.append(item.slug)
            walked: list[str] = []
            node = chain.head
            while node is not None:
                walked.append(node.value)
                node = node.next
            return walked

        return _feature(None, build)

    # ------------------------------------------------------------------
    # assignment2 — ``stack``
    # ------------------------------------------------------------------
    def recently_viewed(self, limit: int = 5) -> list[str] | None:
        """Return the most recently viewed slugs, newest first."""

        def read() -> list[str]:
            buffered: list[str] = []
            while len(self._history) > 0:
                buffered.append(self._history.pop())
            for value in reversed(buffered):
                self._history.push(value)
            return buffered[:limit]

        return _feature(None, read)

    # ------------------------------------------------------------------
    # assignment2 — ``queue``
    # ------------------------------------------------------------------
    def next_in_processing_queue(self) -> str | None:
        """Peek at the next slug awaiting background processing."""

        def peek() -> str | None:
            if len(self._processing) == 0:
                return None
            return self._processing.peek()

        return _feature(None, peek)

    # ------------------------------------------------------------------
    # assignment3 — ``merge_sort``
    # ------------------------------------------------------------------
    def list_portfolios_sorted_by_title(self) -> list[PortfolioItem] | None:
        """Sort portfolios alphabetically by title using ``merge_sort``."""
        items = self.list_portfolios()
        return _feature(
            None,
            lambda: merge_sort(key=lambda item: (item.title or "").lower()).sort(items),
        )

    # ------------------------------------------------------------------
    # assignment3 — ``bubble_sort``
    # ------------------------------------------------------------------
    def list_portfolios_sorted_by_student(self) -> list[PortfolioItem] | None:
        """Sort portfolios alphabetically by student name using ``bubble_sort``."""
        items = self.list_portfolios()
        return _feature(
            None,
            lambda: bubble_sort(
                key=lambda item: (item.student_name or "").lower()
            ).sort(items),
        )

    # ------------------------------------------------------------------
    # assignment4 — ``linear_search``
    # ------------------------------------------------------------------
    def find_index_linear(self, slug: str) -> int | None:
        """Return the index of ``slug`` in the unsorted listing via linear search."""
        items = self.list_portfolios()
        return _feature(
            None,
            lambda: linear_search(key=lambda item: item.slug).search(items, slug),
        )

    # ------------------------------------------------------------------
    # assignment4 — ``binary_search``
    # ------------------------------------------------------------------
    def find_index_binary(self, slug: str) -> int | None:
        """Return the index of ``slug`` in the slug-sorted listing via binary search."""
        items = sorted(self.list_portfolios(), key=lambda item: item.slug)
        return _feature(
            None,
            lambda: binary_search(key=lambda item: item.slug).search(items, slug),
        )

    # ------------------------------------------------------------------
    # assignment5 — ``factorial``
    # ------------------------------------------------------------------
    def ordering_count(self) -> int | None:
        """Return ``n!`` for the current portfolio count, capped for safety."""
        n = min(len(self.list_portfolios()), self._FACTORIAL_CAP)
        return _feature(None, lambda: factorial().compute(n))

    # ------------------------------------------------------------------
    # assignment5 — ``permutations``
    # ------------------------------------------------------------------
    def sample_ordering(self) -> list[str] | None:
        """Return one permutation of the first few slugs."""
        slugs = [item.slug for item in self.list_portfolios()[: self._PERMUTATION_CAP]]

        def build() -> list[str]:
            if not slugs:
                return []
            orderings = permutations().generate(slugs)
            return orderings[0] if orderings else []

        return _feature(None, build)

    # ------------------------------------------------------------------
    # assignment6 — ``hash_table``
    # ------------------------------------------------------------------
    def slug_directory(self) -> list[tuple[str, str]] | None:
        """Return slug → title pairs loaded out of a ``hash_table``."""
        items = self.list_portfolios()

        def build() -> list[tuple[str, str]]:
            table = hash_table()
            for item in items:
                table.put(item.slug, item.title or "")
            pairs: list[tuple[str, str]] = []
            for item in items:
                title = table.get(item.slug)
                if title is not None:
                    pairs.append((item.slug, title))
            return pairs

        return _feature(None, build)

    # ------------------------------------------------------------------
    # assignment7 — ``binary_tree``
    # ------------------------------------------------------------------
    def slugs_alphabetical(self) -> list[str] | None:
        """Return every slug in ascending order via a BST in-order walk."""
        slugs = [item.slug for item in self.list_portfolios()]

        def build() -> list[str]:
            tree = binary_tree()
            for slug in slugs:
                tree.insert(slug)
            return tree.inorder()

        return _feature(None, build)

    # ------------------------------------------------------------------
    # assignment7 — ``min_heap``
    # ------------------------------------------------------------------
    def next_featured_slug(self) -> str | None:
        """Return the slug that sorts first by ``(student_name, slug)``."""
        items = self.list_portfolios()
        if not items:
            return None

        def build() -> str:
            heap = min_heap()
            for item in items:
                heap.push((item.student_name or "", item.slug))
            return heap.peek()[1]

        return _feature(None, build)

    # ------------------------------------------------------------------
    # assignment8 — ``avl_tree``
    # ------------------------------------------------------------------
    def slug_known_balanced(self, slug: str) -> bool | None:
        """Use an ``avl_tree`` of slugs to check membership in O(log n)."""

        def build() -> bool:
            tree = avl_tree()
            for item in self.list_portfolios():
                tree.insert(item.slug)
            return tree.contains(slug)

        return _feature(None, build)

    # ------------------------------------------------------------------
    # assignment8 — ``trie``
    # ------------------------------------------------------------------
    def autocomplete_prefix(self, prefix: str) -> bool | None:
        """Return ``True`` if any slug begins with ``prefix`` via a ``trie``."""

        def build() -> bool:
            t = trie()
            for item in self.list_portfolios():
                t.insert(item.slug)
            return t.starts_with(prefix)

        return _feature(None, build)

    # ------------------------------------------------------------------
    # assignment9 — ``graph``
    # ------------------------------------------------------------------
    def related_slugs(self, slug: str) -> list[str] | None:
        """Return slugs directly connected to ``slug`` in the related graph."""

        def build() -> list[str]:
            g, _ = self._build_related_graph()
            if slug not in g.nodes():
                return []
            return sorted(g.neighbors(slug))

        return _feature(None, build)

    def _build_related_graph(self) -> tuple[object, list[PortfolioItem]]:
        """Build an undirected ``graph`` that connects items sharing a student."""
        items = self.list_portfolios()
        g = graph()
        for item in items:
            g.add_node(item.slug)
        by_student: dict[str, list[str]] = {}
        for item in items:
            by_student.setdefault(item.student_name or "", []).append(item.slug)
        for slugs in by_student.values():
            for i in range(len(slugs)):
                for j in range(i + 1, len(slugs)):
                    g.add_edge(slugs[i], slugs[j])
        # Also chain items in listing order so single-student datasets still
        # produce some connectivity for downstream BFS / Dijkstra demos.
        for a, b in zip([i.slug for i in items], [i.slug for i in items][1:]):
            g.add_edge(a, b)
        return g, items

    # ------------------------------------------------------------------
    # assignment9 — ``bfs_pathfinder``
    # ------------------------------------------------------------------
    def navigation_chain(self, start_slug: str, goal_slug: str) -> list[str] | None:
        """Return the BFS shortest chain of related slugs from start to goal."""

        def build() -> list[str]:
            g, _ = self._build_related_graph()
            path = bfs_pathfinder().shortest_path(g, start_slug, goal_slug)
            return path or []

        return _feature(None, build)

    # ------------------------------------------------------------------
    # assignment10 — ``dijkstra``
    # ------------------------------------------------------------------
    def similarity_distances(self, start_slug: str) -> dict[str, int] | None:
        """Return Dijkstra distances from ``start_slug`` to every reachable slug."""
        adjacency = self._build_weighted_adjacency()
        if start_slug not in adjacency:
            return None
        return _feature(None, lambda: dijkstra().shortest_paths(adjacency, start_slug))

    def _build_weighted_adjacency(self) -> dict[str, dict[str, int]]:
        """Weighted directed adjacency keyed by slug (title-length deltas)."""
        items = self.list_portfolios()
        adjacency: dict[str, dict[str, int]] = {item.slug: {} for item in items}
        for i in range(len(items) - 1):
            a, b = items[i], items[i + 1]
            weight = abs(len(a.title or "") - len(b.title or "")) or 1
            adjacency[a.slug][b.slug] = weight
            adjacency[b.slug][a.slug] = weight
        return adjacency

    # ------------------------------------------------------------------
    # assignment10 — ``topological_sort``
    # ------------------------------------------------------------------
    def prerequisite_order(self) -> list[str] | None:
        """Return a topological ordering of slugs (listing order as the DAG)."""
        items = self.list_portfolios()
        if not items:
            return _feature(None, lambda: topological_sort().order({}))
        adjacency: dict[str, list[str]] = {item.slug: [] for item in items}
        for i in range(len(items) - 1):
            adjacency[items[i].slug].append(items[i + 1].slug)
        return _feature(None, lambda: topological_sort().order(adjacency))
