"""Assignment 6 — Hashing and Hash Tables.

This module contains a starter shell for a ``hash_table`` that uses separate
chaining (a list of buckets, each a list of ``(key, value)`` pairs) to handle
collisions.

Fill in the method bodies marked with ``raise NotImplementedError`` as part of
the assignment. The accompanying unit tests in ``tests/test_assignment6.py``
describe the expected behaviour of each method.
"""


class hash_table:
    """A separate-chaining hash table mapping keys to values.

    Could be used by ``PortfolioService`` as an in-memory cache mapping a
    portfolio slug to its fully populated ``PortfolioItem``, avoiding extra
    repository round-trips when the same slug is requested repeatedly.
    """

    def __init__(self, capacity=16):
        self.capacity = capacity
        self._buckets = [[] for _ in range(capacity)]
        self.size = 0

    def __len__(self):
        """Return the number of key/value pairs currently stored."""
        return self.size

    def _bucket_for(self, key):
        return self._buckets[hash(key) % self.capacity]

    def put(self, key, value):
        """Insert or update the mapping for ``key`` to ``value``.

        Used by the cache layer to remember the ``PortfolioItem`` associated
        with a slug after the first repository fetch. Subsequent lookups
        via ``get`` can short-circuit the repository call.
        """
        bucket = self._bucket_for(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self.size += 1

    def get(self, key):
        """Return the value associated with ``key``, or ``None`` if absent.

        Looks the cached ``PortfolioItem`` up by slug. Returning ``None``
        signals a cache miss so the caller can fall back to the repository.
        """
        for k, v in self._bucket_for(key):
            if k == key:
                return v
        return None

    def remove(self, key):
        """Remove the mapping for ``key``. Returns ``True`` if removed.

        Used to invalidate a cached ``PortfolioItem`` (for example after an
        edit) so the next ``get`` returns ``None`` and the freshest record
        is loaded from the repository.
        """
        bucket = self._bucket_for(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return True
        return False
