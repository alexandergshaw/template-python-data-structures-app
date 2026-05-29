"""Unit tests for Assignment 7 binary trees and heaps.

The methods under test are shells that initially raise ``NotImplementedError``.
The behaviour tests are marked ``xfail`` so the suite stays green until the
assignment is implemented; once a method is filled in, its test will pass.
"""

import pytest

from data_structures.assignment7 import binary_tree, min_heap


# -- binary_tree tests --


class TestBinaryTree:
    def test_new_tree_is_empty(self):
        t = binary_tree()
        assert len(t) == 0
        assert t.root is None

    @pytest.mark.xfail(reason="binary_tree.insert not yet implemented")
    def test_insert_increases_size(self):
        t = binary_tree()
        t.insert(5)
        t.insert(2)
        assert len(t) == 2

    @pytest.mark.xfail(reason="binary_tree.contains not yet implemented")
    def test_contains_finds_inserted_values(self):
        t = binary_tree()
        for v in [5, 3, 8, 1]:
            t.insert(v)
        assert t.contains(3) is True
        assert t.contains(99) is False

    @pytest.mark.xfail(reason="binary_tree.inorder not yet implemented")
    def test_inorder_returns_sorted_values(self):
        t = binary_tree()
        for v in [5, 3, 8, 1, 4]:
            t.insert(v)
        assert t.inorder() == [1, 3, 4, 5, 8]


# -- min_heap tests --


class TestMinHeap:
    def test_new_heap_is_empty(self):
        h = min_heap()
        assert len(h) == 0

    @pytest.mark.xfail(reason="min_heap.push not yet implemented")
    def test_push_increases_length(self):
        h = min_heap()
        h.push(3)
        h.push(1)
        assert len(h) == 2

    @pytest.mark.xfail(reason="min_heap.peek not yet implemented")
    def test_peek_returns_smallest(self):
        h = min_heap()
        for v in [5, 2, 8, 1, 4]:
            h.push(v)
        assert h.peek() == 1

    @pytest.mark.xfail(reason="min_heap.pop not yet implemented")
    def test_pop_returns_sorted_order(self):
        h = min_heap()
        for v in [5, 2, 8, 1, 4]:
            h.push(v)
        result = [h.pop() for _ in range(5)]
        assert result == [1, 2, 4, 5, 8]
