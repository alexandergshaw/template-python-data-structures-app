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
        """Return the element stored at ``index``."""
        raise NotImplementedError

    def set(self, index, value):
        """Store ``value`` at ``index``."""
        raise NotImplementedError

    def append(self, value):
        """Add ``value`` to the end of the array."""
        raise NotImplementedError


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
        """Add ``value`` to the end of the list."""
        raise NotImplementedError

    def prepend(self, value):
        """Add ``value`` to the front of the list."""
        raise NotImplementedError

    def find(self, value):
        """Return ``True`` if ``value`` exists in the list, else ``False``."""
        raise NotImplementedError
