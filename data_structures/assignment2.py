"""Assignment 2 — Stacks and Queues.

This module contains starter shells for two fundamental linear data
structures:

* ``stack`` — a last-in, first-out (LIFO) collection.
* ``queue`` — a first-in, first-out (FIFO) collection.

Fill in the method bodies marked with ``raise NotImplementedError`` as part of
the assignment. The accompanying unit tests in ``tests/test_assignment2.py``
describe the expected behaviour of each method.
"""


class stack:
    """A simple last-in, first-out stack."""

    def __init__(self):
        self._items = []

    def __len__(self):
        """Return the number of elements currently on the stack."""
        return len(self._items)

    def push(self, value):
        """Place ``value`` on top of the stack.

        Could be used by ``PortfolioService`` to record the most recently
        viewed portfolio slugs so the user can navigate "back" through their
        browsing history one entry at a time.
        """
        self._items.append(value)

    def pop(self):
        """Remove and return the value on top of the stack.

        Pops the most recently viewed portfolio slug off the navigation
        history so the previous one becomes the new top of the stack.
        """
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        """Return the value on top of the stack without removing it.

        Useful when the service wants to know which portfolio the user is
        currently looking at without altering the history.
        """
        if not self._items:
            raise IndexError("peek from empty stack")
        return self._items[-1]


class queue:
    """A simple first-in, first-out queue."""

    def __init__(self):
        self._items = []

    def __len__(self):
        """Return the number of elements currently in the queue."""
        return len(self._items)

    def enqueue(self, value):
        """Add ``value`` to the back of the queue.

        Could be used by ``PortfolioService`` to schedule portfolio items
        for background processing (e.g. thumbnail generation) in the order
        they were submitted.
        """
        self._items.append(value)

    def dequeue(self):
        """Remove and return the value at the front of the queue.

        Pulls the next portfolio item off the processing queue so the
        service can act on the oldest pending entry first.
        """
        if not self._items:
            raise IndexError("dequeue from empty queue")
        return self._items.pop(0)

    def peek(self):
        """Return the value at the front of the queue without removing it.

        Lets the service inspect which portfolio item will be processed
        next without committing to consuming it.
        """
        if not self._items:
            raise IndexError("peek from empty queue")
        return self._items[0]
