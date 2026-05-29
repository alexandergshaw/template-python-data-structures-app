"""Assignment 10 — Advanced Graph Algorithms.

This module contains starter shells for two classical graph algorithms:

* ``dijkstra``         — single-source shortest paths in a weighted graph.
* ``topological_sort`` — a linear ordering of a DAG's vertices.

Both algorithms operate on a weighted directed graph represented as a dict
of ``{node: {neighbor: weight}}`` adjacency mappings (weights are ignored by
``topological_sort``). Fill in the method bodies marked with
``raise NotImplementedError`` as part of the assignment. The accompanying unit
tests in ``tests/test_assignment10.py`` describe the expected behaviour.
"""

import heapq


class dijkstra:
    """Dijkstra's shortest-path algorithm.

    Could be used by ``PortfolioService`` if portfolios were connected by
    weighted "similarity" edges (lower weight = more similar) — Dijkstra
    would then surface the most-similar recommendation chain for a given
    portfolio.
    """

    def shortest_paths(self, adjacency, start):
        """Return a dict mapping each reachable node to its shortest
        distance from ``start``.

        Maintains a min-heap of ``(distance, node)`` pairs, popping the
        closest unsettled node and relaxing each of its outgoing edges.
        Unreachable nodes are omitted from the returned dict.
        """
        if start not in adjacency:
            raise KeyError(f"Start node {start!r} not in graph")
        distances = {start: 0}
        heap = [(0, start)]
        while heap:
            dist, node = heapq.heappop(heap)
            if dist > distances.get(node, float("inf")):
                continue
            for neighbor, weight in adjacency.get(node, {}).items():
                if weight < 0:
                    raise ValueError("dijkstra does not support negative weights")
                new_dist = dist + weight
                if new_dist < distances.get(neighbor, float("inf")):
                    distances[neighbor] = new_dist
                    heapq.heappush(heap, (new_dist, neighbor))
        return distances


class topological_sort:
    """Kahn's algorithm for topologically ordering a DAG.

    Could be used by ``PortfolioService`` to order portfolio items by
    declared "prerequisite" dependencies — e.g. when a featured item must
    appear after the items it builds on.
    """

    def order(self, adjacency):
        """Return a topological ordering of the nodes in ``adjacency``.

        Computes in-degrees, repeatedly removes a zero-in-degree node, and
        decrements its neighbours' in-degrees. Raises ``ValueError`` if the
        graph contains a cycle.
        """
        in_degree = {node: 0 for node in adjacency}
        for node, neighbors in adjacency.items():
            for neighbor in neighbors:
                in_degree.setdefault(neighbor, 0)
                in_degree[neighbor] += 1
        ready = [n for n, d in in_degree.items() if d == 0]
        ready.sort()  # deterministic order for ties
        result = []
        while ready:
            node = ready.pop(0)
            result.append(node)
            for neighbor in adjacency.get(node, ()):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    ready.append(neighbor)
            ready.sort()
        if len(result) != len(in_degree):
            raise ValueError("graph contains a cycle; topological sort impossible")
        return result
