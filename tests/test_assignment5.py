"""Unit tests for Assignment 5 recursion and backtracking.

The methods under test are shells that initially raise ``NotImplementedError``.
The behaviour tests are marked ``xfail`` so the suite stays green until the
assignment is implemented; once a method is filled in, its test will pass.
"""

import pytest

from data_structures.assignment5 import factorial, permutations


# -- factorial tests --


class TestFactorial:
    def test_constructible(self):
        assert factorial() is not None

    @pytest.mark.xfail(reason="factorial.compute not yet implemented")
    def test_factorial_zero(self):
        assert factorial().compute(0) == 1

    @pytest.mark.xfail(reason="factorial.compute not yet implemented")
    def test_factorial_five(self):
        assert factorial().compute(5) == 120

    @pytest.mark.xfail(reason="factorial.compute not yet implemented")
    def test_factorial_negative_raises(self):
        with pytest.raises(ValueError):
            factorial().compute(-1)


# -- permutations tests --


class TestPermutations:
    def test_constructible(self):
        assert permutations() is not None

    @pytest.mark.xfail(reason="permutations.generate not yet implemented")
    def test_empty_input(self):
        assert permutations().generate([]) == [[]]

    @pytest.mark.xfail(reason="permutations.generate not yet implemented")
    def test_three_distinct_items(self):
        result = permutations().generate([1, 2, 3])
        assert len(result) == 6
        assert sorted(result) == sorted(
            [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
        )
