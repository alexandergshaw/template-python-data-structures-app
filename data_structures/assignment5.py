"""Assignment 5 — Recursion and Backtracking.

This module contains starter shells for two classic recursive problems:

* ``factorial``    — computes n! using straight recursion.
* ``permutations`` — generates every ordering of a sequence via backtracking.

Fill in the method bodies marked with ``raise NotImplementedError`` as part of
the assignment. The accompanying unit tests in ``tests/test_assignment5.py``
describe the expected behaviour of each method.
"""


class factorial:
    """Recursive factorial calculator packaged as a callable class.

    Could be used by ``PortfolioService`` (in a contrived example) to compute
    the number of orderings of a small set of portfolio items when generating
    a "random tour" feature.
    """

    def compute(self, n):
        """Return ``n!`` computed recursively.

        Uses the standard base case ``factorial(0) == 1`` and recursive step
        ``factorial(n) == n * factorial(n - 1)``. Raises ``ValueError`` for
        negative ``n``.
        """
        if n < 0:
            raise ValueError("factorial is undefined for negative numbers")
        if n <= 1:
            return 1
        return n * self.compute(n - 1)


class permutations:
    """Backtracking permutation generator.

    Could be used by ``PortfolioService`` to enumerate every possible order
    in which a small list of featured portfolios could be displayed, so the
    view can pick one arrangement at random.
    """

    def generate(self, items):
        """Return a list of every ordering of ``items``.

        Uses backtracking: at each level it picks one of the remaining
        elements, recurses on the rest, and unpicks before trying the next
        choice. Returns ``[[]]`` when ``items`` is empty.
        """
        result = []
        items = list(items)
        used = [False] * len(items)
        current = []
        self._backtrack(items, used, current, result)
        return result

    def _backtrack(self, items, used, current, result):
        if len(current) == len(items):
            result.append(list(current))
            return
        for i, item in enumerate(items):
            if used[i]:
                continue
            used[i] = True
            current.append(item)
            self._backtrack(items, used, current, result)
            current.pop()
            used[i] = False
