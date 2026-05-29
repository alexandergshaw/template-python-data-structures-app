"""Unit tests for Assignment 10 advanced graph algorithms.

The methods under test are shells that initially raise ``NotImplementedError``.
The behaviour tests are marked ``xfail`` so the suite stays green until the
assignment is implemented; once a method is filled in, its test will pass.
"""

import pytest

from data_structures.assignment10 import dijkstra, topological_sort


# -- dijkstra tests --


class TestDijkstra:
    def _graph(self):
        return {
            "A": {"B": 1, "C": 4},
            "B": {"C": 2, "D": 5},
            "C": {"D": 1},
            "D": {},
        }

    def test_constructible(self):
        assert dijkstra() is not None

    @pytest.mark.xfail(reason="dijkstra.shortest_paths not yet implemented")
    def test_distances_from_start(self):
        result = dijkstra().shortest_paths(self._graph(), "A")
        assert result == {"A": 0, "B": 1, "C": 3, "D": 4}

    @pytest.mark.xfail(reason="dijkstra.shortest_paths not yet implemented")
    def test_unreachable_nodes_omitted(self):
        g = {"A": {"B": 1}, "B": {}, "C": {}}
        result = dijkstra().shortest_paths(g, "A")
        assert result == {"A": 0, "B": 1}


# -- topological_sort tests --


class TestTopologicalSort:
    def test_constructible(self):
        assert topological_sort() is not None

    @pytest.mark.xfail(reason="topological_sort.order not yet implemented")
    def test_simple_dag(self):
        # A -> B -> D, A -> C -> D
        g = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
        result = topological_sort().order(g)
        assert result.index("A") < result.index("B")
        assert result.index("A") < result.index("C")
        assert result.index("B") < result.index("D")
        assert result.index("C") < result.index("D")

    @pytest.mark.xfail(reason="topological_sort.order not yet implemented")
    def test_cycle_raises(self):
        g = {"A": ["B"], "B": ["C"], "C": ["A"]}
        with pytest.raises(ValueError):
            topological_sort().order(g)
