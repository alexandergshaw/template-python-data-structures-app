"""Unit tests for Assignment 4 searching algorithms.

The methods under test are shells that initially raise ``NotImplementedError``.
The behaviour tests are marked ``xfail`` so the suite stays green until the
assignment is implemented; once a method is filled in, its test will pass.
"""

import pytest

from data_structures.assignment4 import linear_search, binary_search


# -- linear_search tests --


class TestLinearSearch:
    def test_constructible(self):
        assert linear_search() is not None

    @pytest.mark.xfail(reason="linear_search.search not yet implemented")
    def test_finds_value(self):
        assert linear_search().search([10, 20, 30, 40], 30) == 2

    @pytest.mark.xfail(reason="linear_search.search not yet implemented")
    def test_missing_value_returns_minus_one(self):
        assert linear_search().search([10, 20, 30], 99) == -1

    @pytest.mark.xfail(reason="linear_search.search not yet implemented")
    def test_uses_key_function(self):
        items = [{"slug": "a"}, {"slug": "b"}, {"slug": "c"}]
        assert linear_search(key=lambda d: d["slug"]).search(items, "b") == 1


# -- binary_search tests --


class TestBinarySearch:
    def test_constructible(self):
        assert binary_search() is not None

    @pytest.mark.xfail(reason="binary_search.search not yet implemented")
    def test_finds_value(self):
        assert binary_search().search([1, 3, 5, 7, 9], 7) == 3

    @pytest.mark.xfail(reason="binary_search.search not yet implemented")
    def test_missing_value_returns_minus_one(self):
        assert binary_search().search([1, 3, 5, 7, 9], 4) == -1

    @pytest.mark.xfail(reason="binary_search.search not yet implemented")
    def test_empty_list_returns_minus_one(self):
        assert binary_search().search([], 1) == -1
