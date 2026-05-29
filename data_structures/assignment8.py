"""Assignment 8 — Advanced Tree Structures.

This module contains starter shells for two advanced tree structures:

* ``avl_tree`` — a self-balancing binary search tree.
* ``trie``     — a prefix tree for strings.

Fill in the method bodies marked with ``raise NotImplementedError`` as part of
the assignment. The accompanying unit tests in ``tests/test_assignment8.py``
describe the expected behaviour of each method.
"""


class avl_tree:
    """A self-balancing binary search tree (AVL).

    Keeps the height of every subtree's left and right children within one
    of each other by rotating after each insert.
    """

    class Node:
        def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None
            self.height = 1

    def __init__(self):
        self.root = None
        self.size = 0

    def __len__(self):
        """Return the number of nodes in the tree."""
        return self.size

    def insert(self, value):
        """Insert ``value`` and re-balance the tree.

        Could be used by ``PortfolioService`` to maintain a balanced index
        of portfolio slugs that guarantees O(log n) lookup even as more
        items are added over time.
        """
        self.root = self._insert(self.root, value)
        self.size += 1

    def contains(self, value):
        """Return ``True`` if ``value`` is in the tree, else ``False``."""
        node = self.root
        while node is not None:
            if value == node.value:
                return True
            node = node.left if value < node.value else node.right
        return False

    def height(self):
        """Return the height of the tree (0 for an empty tree)."""
        return self._height(self.root)

    def _height(self, node):
        return node.height if node is not None else 0

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right)

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _rotate_right(self, y):
        x = y.left
        t = x.right
        x.right = y
        y.left = t
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        y = x.right
        t = y.left
        y.left = x
        x.right = t
        self._update_height(x)
        self._update_height(y)
        return y

    def _insert(self, node, value):
        if node is None:
            return self.Node(value)
        if value < node.value:
            node.left = self._insert(node.left, value)
        else:
            node.right = self._insert(node.right, value)
        self._update_height(node)
        balance = self._balance_factor(node)
        # Left-Left
        if balance > 1 and value < node.left.value:
            return self._rotate_right(node)
        # Right-Right
        if balance < -1 and value >= node.right.value:
            return self._rotate_left(node)
        # Left-Right
        if balance > 1 and value >= node.left.value:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        # Right-Left
        if balance < -1 and value < node.right.value:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node


class trie:
    """A prefix tree storing strings character-by-character.

    Could be used by ``PortfolioService`` to implement fast slug
    autocomplete: given a prefix typed in a search box, the trie can
    enumerate every known slug that starts with it.
    """

    class Node:
        def __init__(self):
            self.children = {}
            self.is_end = False

    def __init__(self):
        self.root = self.Node()
        self.size = 0

    def __len__(self):
        """Return the number of full words stored in the trie."""
        return self.size

    def insert(self, word):
        """Insert ``word`` into the trie.

        Walks the trie one character at a time, creating new child nodes
        for any characters that aren't already there, and marks the final
        node as the end of a word.
        """
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = self.Node()
            node = node.children[ch]
        if not node.is_end:
            node.is_end = True
            self.size += 1

    def contains(self, word):
        """Return ``True`` if ``word`` was previously inserted."""
        node = self._traverse(word)
        return node is not None and node.is_end

    def starts_with(self, prefix):
        """Return ``True`` if any inserted word starts with ``prefix``."""
        return self._traverse(prefix) is not None

    def _traverse(self, text):
        node = self.root
        for ch in text:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node
