"""Assignment 1 — Data Structures.

This module contains starter shells for two fundamental data structures:

* ``array``       — a fixed-capacity, index-based collection.
* ``linked_list`` — a singly linked list of nodes.

Fill in the method bodies marked with ``raise NotImplementedError`` as part of
the assignment. The accompanying unit tests in ``tests/test_assignment1.py``
describe the expected behaviour of each method.
"""


class array:
    """A simple fixed-capacity array.

    Args:
        capacity: The maximum number of elements the array can hold.
    """

    def __init__(self, capacity):
        self.capacity = capacity
        self._items = [None] * capacity
        self.size = 0

    def __len__(self):
        """Return the number of elements currently stored."""
        return self.size

    def get(self, index):
        """Return the element stored at ``index``.

        Used by ``PortfolioService.list_portfolios`` to read each
        ``PortfolioItem`` back out of the array after all items have been
        loaded, so they can be returned to the route and rendered in the
        portfolio listing page.
        """
        if index < 0 or index >= self.size:
            raise IndexError(f"Index {index} out of range for size {self.size}")
        return self._items[index]

    def set(self, index, value):
        """Store ``value`` at ``index``.

        Allows an individual slot in the array to be updated in-place, which
        is useful if a portfolio item needs to be replaced or corrected
        without rebuilding the entire collection.
        """
        if index < 0 or index >= self.size:
            raise IndexError(f"Index {index} out of range for size {self.size}")
        self._items[index] = value

    def append(self, value):
        """Add ``value`` to the end of the array.

        Called by ``PortfolioService.list_portfolios`` once for each
        ``PortfolioItem`` fetched from the repository, filling the array
        slot-by-slot up to its pre-allocated capacity before the items are
        read back with ``get`` and returned to the view.
        """
        if self.size >= self.capacity:
            raise OverflowError("Array is at full capacity")
        self._items[self.size] = value
        self.size += 1


class linked_list:
    """A singly linked list."""

    class Node:
        """A single node holding a value and a reference to the next node."""

        def __init__(self, value, next=None):
            self.value = value
            self.next = next

    def __init__(self):
        self.head = None
        self.size = 0

    def __len__(self):
        """Return the number of nodes in the list."""
        return self.size

    def append(self, value):
        """Add ``value`` to the end of the list.

        Used by ``PortfolioService.get_portfolio`` to build a linked list of
        all known slugs from the repository.  Each slug is appended in order
        so the list represents every available portfolio item, enabling
        ``find`` to confirm whether the requested slug exists before the
        service delegates to the repository for the full record.
        """
        new_node = self.Node(value)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self.size += 1

    def prepend(self, value):
        """Add ``value`` to the front of the list.

        Inserts a new node before the current head in O(1) time.  This can
        be used when the most-recently added item should appear first — for
        example, if the service wanted to reverse the repository order before
        slug-checking.
        """
        self.head = self.Node(value, next=self.head)
        self.size += 1

    def find(self, value):
        """Return ``True`` if ``value`` exists in the list, else ``False``.

        Called by ``PortfolioService.get_portfolio`` to verify that the
        requested slug was found among the slugs loaded from the repository.
        If the slug is present the service proceeds to fetch the full
        ``PortfolioItem``; otherwise it returns ``None`` (or the placeholder)
        without making an unnecessary database round-trip.
        """
        current = self.head
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False
