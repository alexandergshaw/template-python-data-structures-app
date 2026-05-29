"""Assignment 9 — Graphs and Pathfinding.

This module contains starter shells for a basic graph plus a breadth-first
search pathfinder:

* ``graph``         — an adjacency-list representation of an undirected graph.
* ``bfs_pathfinder`` — finds the shortest unweighted path between two nodes.

Fill in the method bodies marked with ``raise NotImplementedError`` as part of
the assignment. The accompanying unit tests in ``tests/test_assignment9.py``
describe the expected behaviour of each method.
"""


class graph:
    """An undirected graph stored as an adjacency list.

    Could be used by ``PortfolioService`` to model "related portfolios" —
    each ``PortfolioItem`` is a node and an edge connects two items that
    share a tag, so the service can recommend neighbours of the currently
    viewed item.
    """

    def __init__(self):
        self._adj = {}

    def add_node(self, node):
        """Add ``node`` to the graph if it isn't already present."""
        if node not in self._adj:
            self._adj[node] = set()

    def add_edge(self, a, b):
        """Add an undirected edge between ``a`` and ``b``.

        Ensures both endpoints exist as nodes, then records each as a
        neighbour of the other.
        """
        self.add_node(a)
        self.add_node(b)
        self._adj[a].add(b)
        self._adj[b].add(a)

    def neighbors(self, node):
        """Return the set of nodes directly connected to ``node``."""
        if node not in self._adj:
            raise KeyError(f"Node {node!r} not in graph")
        return set(self._adj[node])

    def nodes(self):
        """Return the set of all nodes in the graph."""
        return set(self._adj.keys())


class bfs_pathfinder:
    """Breadth-first search shortest-path finder.

    Could be used by ``PortfolioService`` to compute the shortest chain of
    "related portfolios" links between two ``PortfolioItem`` slugs, which
    powers a "how is X connected to Y?" navigation feature.
    """

    def shortest_path(self, g, start, goal):
        """Return the shortest path from ``start`` to ``goal`` as a list of
        nodes, or ``None`` if no path exists.

        Performs a standard breadth-first traversal, tracking each node's
        predecessor so the path can be reconstructed once ``goal`` is
        reached.
        """
        if start not in g.nodes() or goal not in g.nodes():
            return None
        if start == goal:
            return [start]
        visited = {start}
        parents = {start: None}
        frontier = [start]
        while frontier:
            next_frontier = []
            for node in frontier:
                for neighbor in g.neighbors(node):
                    if neighbor in visited:
                        continue
                    visited.add(neighbor)
                    parents[neighbor] = node
                    if neighbor == goal:
                        return self._reconstruct(parents, goal)
                    next_frontier.append(neighbor)
            frontier = next_frontier
        return None

    def _reconstruct(self, parents, goal):
        path = []
        node = goal
        while node is not None:
            path.append(node)
            node = parents[node]
        path.reverse()
        return path
