"""Unit tests for Assignment 9 graphs and pathfinding.

The methods under test are shells that initially raise ``NotImplementedError``.
The behaviour tests are marked ``xfail`` so the suite stays green until the
assignment is implemented; once a method is filled in, its test will pass.
"""

import pytest

from data_structures.assignment9 import graph, bfs_pathfinder


# -- graph tests --


class TestGraph:
    def test_new_graph_has_no_nodes(self):
        g = graph()
        assert g.nodes() == set()

    @pytest.mark.xfail(reason="graph.add_node not yet implemented")
    def test_add_node(self):
        g = graph()
        g.add_node("A")
        assert g.nodes() == {"A"}

    @pytest.mark.xfail(reason="graph.add_edge not yet implemented")
    def test_add_edge_is_undirected(self):
        g = graph()
        g.add_edge("A", "B")
        assert g.neighbors("A") == {"B"}
        assert g.neighbors("B") == {"A"}


# -- bfs_pathfinder tests --


class TestBFSPathfinder:
    def _build(self):
        g = graph()
        edges = [("A", "B"), ("B", "C"), ("A", "D"), ("D", "E"), ("E", "C")]
        for a, b in edges:
            g.add_edge(a, b)
        return g

    def test_constructible(self):
        assert bfs_pathfinder() is not None

    @pytest.mark.xfail(reason="bfs_pathfinder.shortest_path not yet implemented")
    def test_path_to_self(self):
        g = self._build()
        assert bfs_pathfinder().shortest_path(g, "A", "A") == ["A"]

    @pytest.mark.xfail(reason="bfs_pathfinder.shortest_path not yet implemented")
    def test_finds_shortest_path(self):
        g = self._build()
        path = bfs_pathfinder().shortest_path(g, "A", "C")
        assert path == ["A", "B", "C"]

    @pytest.mark.xfail(reason="bfs_pathfinder.shortest_path not yet implemented")
    def test_no_path_returns_none(self):
        g = graph()
        g.add_node("A")
        g.add_node("Z")
        assert bfs_pathfinder().shortest_path(g, "A", "Z") is None
