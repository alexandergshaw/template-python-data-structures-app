"""Assignment 3 — Sorting Algorithms.

This module contains starter shells for two classic comparison sorts:

* ``bubble_sort`` — repeatedly swaps adjacent out-of-order pairs.
* ``merge_sort``  — recursively splits and merges sorted halves.

Both implementations return a new sorted list and leave the input untouched.
Fill in the method bodies marked with ``raise NotImplementedError`` as part of
the assignment. The accompanying unit tests in ``tests/test_assignment3.py``
describe the expected behaviour of each function.
"""


class bubble_sort:
    """Bubble sort implementation packaged as a callable class.

    Could be used by ``PortfolioService`` to order a small ``PortfolioItem``
    list alphabetically by title before rendering, when the dataset is tiny
    enough that an O(n^2) sort is acceptable.
    """

    def __init__(self, key=None):
        self.key = key or (lambda x: x)

    def sort(self, items):
        """Return a new list with ``items`` in ascending order.

        Iterates over the list repeatedly, comparing adjacent elements via
        ``self.key`` and swapping them when they are out of order, until a
        full pass produces no swaps.
        """
        result = list(items)
        n = len(result)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if self.key(result[j]) > self.key(result[j + 1]):
                    result[j], result[j + 1] = result[j + 1], result[j]
                    swapped = True
            if not swapped:
                break
        return result


class merge_sort:
    """Merge sort implementation packaged as a callable class.

    Could be used by ``PortfolioService`` to order a larger ``PortfolioItem``
    list (for example, sorted by ``student_name``) in O(n log n) time before
    returning it to the view.
    """

    def __init__(self, key=None):
        self.key = key or (lambda x: x)

    def sort(self, items):
        """Return a new list with ``items`` in ascending order.

        Recursively splits the list in half, sorts each half, and merges the
        two sorted halves back together using ``self.key`` for comparisons.
        """
        if len(items) <= 1:
            return list(items)
        mid = len(items) // 2
        left = self.sort(items[:mid])
        right = self.sort(items[mid:])
        return self._merge(left, right)

    def _merge(self, left, right):
        """Merge two pre-sorted lists into a single sorted list."""
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if self.key(left[i]) <= self.key(right[j]):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged
