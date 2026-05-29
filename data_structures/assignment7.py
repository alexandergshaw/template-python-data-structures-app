"""Assignment 7 — Binary Trees and Heaps.

This module contains starter shells for two tree-shaped data structures:

* ``binary_tree`` — a simple binary search tree of comparable values.
* ``min_heap``    — a binary min-heap backed by a list.

Fill in the method bodies marked with ``raise NotImplementedError`` as part of
the assignment. The accompanying unit tests in ``tests/test_assignment7.py``
describe the expected behaviour of each method.
"""


class binary_tree:
    """A binary search tree of comparable values."""

    class Node:
        def __init__(self, value, left=None, right=None):
            self.value = value
            self.left = left
            self.right = right

    def __init__(self):
        self.root = None
        self.size = 0

    def __len__(self):
        """Return the number of nodes in the tree."""
        return self.size

    def insert(self, value):
        """Insert ``value`` into the tree in BST order.

        Could be used by ``PortfolioService`` to build a searchable tree of
        portfolio slugs so that subsequent ``contains`` lookups run in
        average O(log n) time.
        """
        self.root = self._insert(self.root, value)
        self.size += 1

    def _insert(self, node, value):
        if node is None:
            return self.Node(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        else:
            node.right = self._insert(node.right, value)
        return node

    def contains(self, value):
        """Return ``True`` if ``value`` is present in the tree.

        Walks left or right at each node depending on how ``value`` compares
        to the current node. Could be used by ``PortfolioService`` to confirm
        a slug exists before fetching the full record.
        """
        node = self.root
        while node is not None:
            if value == node.value:
                return True
            node = node.left if value < node.value else node.right
        return False

    def inorder(self):
        """Return the values of the tree in ascending order.

        Performs an in-order traversal, which for a BST yields the values
        sorted. Could be used to render portfolio slugs alphabetically.
        """
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.value)
        self._inorder(node.right, result)


class min_heap:
    """A binary min-heap backed by a Python list."""

    def __init__(self):
        self._items = []

    def __len__(self):
        """Return the number of elements in the heap."""
        return len(self._items)

    def push(self, value):
        """Insert ``value`` into the heap.

        Could be used by ``PortfolioService`` to maintain a priority queue
        of portfolio items ordered by, say, ``created_at`` so the next item
        to feature can always be popped in O(log n) time.
        """
        self._items.append(value)
        self._sift_up(len(self._items) - 1)

    def pop(self):
        """Remove and return the smallest element in the heap.

        Removes the root (minimum) element by swapping it with the last
        element, shrinking the list, then sifting the new root down to
        restore the heap property.
        """
        if not self._items:
            raise IndexError("pop from empty heap")
        smallest = self._items[0]
        last = self._items.pop()
        if self._items:
            self._items[0] = last
            self._sift_down(0)
        return smallest

    def peek(self):
        """Return the smallest element without removing it."""
        if not self._items:
            raise IndexError("peek from empty heap")
        return self._items[0]

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self._items[i] < self._items[parent]:
                self._items[i], self._items[parent] = (
                    self._items[parent],
                    self._items[i],
                )
                i = parent
            else:
                break

    def _sift_down(self, i):
        n = len(self._items)
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            smallest = i
            if left < n and self._items[left] < self._items[smallest]:
                smallest = left
            if right < n and self._items[right] < self._items[smallest]:
                smallest = right
            if smallest == i:
                break
            self._items[i], self._items[smallest] = (
                self._items[smallest],
                self._items[i],
            )
            i = smallest
