"""Unit tests for Assignment 3 sorting algorithms.

The methods under test are shells that initially raise ``NotImplementedError``.
The behaviour tests are marked ``xfail`` so the suite stays green until the
assignment is implemented; once a method is filled in, its test will pass.
"""

import pytest

from data_structures.assignment3 import bubble_sort, merge_sort


# -- bubble_sort tests --


class TestBubbleSort:
    def test_constructible(self):
        sorter = bubble_sort()
        assert sorter is not None

    @pytest.mark.xfail(reason="bubble_sort.sort not yet implemented")
    def test_sorts_integers(self):
        assert bubble_sort().sort([3, 1, 2]) == [1, 2, 3]

    @pytest.mark.xfail(reason="bubble_sort.sort not yet implemented")
    def test_empty_list_returns_empty(self):
        assert bubble_sort().sort([]) == []

    @pytest.mark.xfail(reason="bubble_sort.sort not yet implemented")
    def test_uses_key_function(self):
        items = [{"n": 3}, {"n": 1}, {"n": 2}]
        result = bubble_sort(key=lambda d: d["n"]).sort(items)
        assert [d["n"] for d in result] == [1, 2, 3]


# -- merge_sort tests --


class TestMergeSort:
    def test_constructible(self):
        sorter = merge_sort()
        assert sorter is not None

    @pytest.mark.xfail(reason="merge_sort.sort not yet implemented")
    def test_sorts_integers(self):
        assert merge_sort().sort([5, 2, 4, 1, 3]) == [1, 2, 3, 4, 5]

    @pytest.mark.xfail(reason="merge_sort.sort not yet implemented")
    def test_single_element(self):
        assert merge_sort().sort([42]) == [42]

    @pytest.mark.xfail(reason="merge_sort.sort not yet implemented")
    def test_uses_key_function(self):
        items = ["bb", "aaa", "c"]
        assert merge_sort(key=len).sort(items) == ["c", "bb", "aaa"]
