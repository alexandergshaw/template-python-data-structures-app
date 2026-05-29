"""Assignment 4 — Searching Algorithms.

This module contains starter shells for two classic search algorithms:

* ``linear_search`` — scans elements one-by-one in O(n) time.
* ``binary_search`` — repeatedly halves a sorted range in O(log n) time.

Both implementations return the index of the matching element, or ``-1`` if
the value is not found. Fill in the method bodies marked with
``raise NotImplementedError`` as part of the assignment. The accompanying unit
tests in ``tests/test_assignment4.py`` describe the expected behaviour.
"""


class linear_search:
    """Linear search packaged as a callable class.

    Could be used by ``PortfolioService`` to locate a ``PortfolioItem`` by
    slug in an unsorted in-memory list without requiring the list to be
    sorted first.
    """

    def __init__(self, key=None):
        self.key = key or (lambda x: x)

    def search(self, items, target):
        """Return the index of the first element equal to ``target``.

        Walks the list from index 0, comparing ``self.key(item)`` to
        ``target`` until a match is found. Returns ``-1`` if no element
        matches.
        """
        for i, item in enumerate(items):
            if self.key(item) == target:
                return i
        return -1


class binary_search:
    """Binary search packaged as a callable class.

    Assumes ``items`` is sorted in ascending order by ``self.key``. Could be
    used by ``PortfolioService`` to quickly locate a portfolio item in a
    pre-sorted listing (e.g. sorted by slug) without scanning the whole
    list.
    """

    def __init__(self, key=None):
        self.key = key or (lambda x: x)

    def search(self, items, target):
        """Return the index of an element equal to ``target``.

        Repeatedly narrows the search range to the half that could contain
        ``target`` by comparing it with the middle element. Returns ``-1``
        if no element matches.
        """
        low, high = 0, len(items) - 1
        while low <= high:
            mid = (low + high) // 2
            value = self.key(items[mid])
            if value == target:
                return mid
            if value < target:
                low = mid + 1
            else:
                high = mid - 1
        return -1
