"""Complete topological sorting, union-find, and Kruskal for Lab 9."""

from collections import deque

DAG_EXAMPLE = [[1, 2], [3], [3], [4], []]
MST_EDGES = [
    (0, 1, 1), (2, 3, 2), (1, 2, 3), (1, 3, 4),
    (0, 2, 5), (3, 4, 6), (2, 4, 7),
]


def topological_sort(graph):
    """Return a Kahn ordering of the directed graph, or None if cyclic.

    Queue initial sources in increasing order; keep the listed neighbor order.
    """
    n = len(graph)
    indegree = [0] * n
    queue = deque()
    order = []

    for u in range(0, n):
        for v in graph[u]:
            indegree[v] = indegree[v] + 1

    for u in range(0, n):
        if indegree[u] == 0:
            queue.append(u)
        

    # TODO 1.2: count incoming edges, process ready vertices, and check for a cycle
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph[u]:
            indegree[v] = indegree[v]-1
            if indegree[v] == 0:
                queue.append(v)
    if len(order) != n:
        return None

    return order


class DisjointSet:
    """Track components with path compression and union by rank."""

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        """Return x's root and compress the path to it."""
        # TODO 2.1A: update each parent on the search path to the root
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """Merge different components and return True, or return False if joined.

        On equal ranks, attach root_y under root_x and increment rank[root_x].
        """
        # TODO 2.1B: find the roots and merge by rank
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] = self.rank[root_x] + 1
        return True

def kruskal(n, edges):
    """Return (chosen, total) for a minimum spanning forest.

    Each undirected edge is (u, v, weight). Preserve ties in input order.
    """
    if n <= 1:
        return [], 0
    sets = DisjointSet(n)
    sorted_edges = sorted(edges, key=lambda edge: edge[2])
    chosen = []
    total = 0

    # TODO 2.1C: use union to accept edges and stop once a spanning tree is complete
    for (u, v, weight) in sorted_edges:
        if sets.union(u, v):
            chosen.append((u, v, weight))
            total = total + weight
            if len(chosen) == n-1:
                break


    return chosen, total


if __name__ == "__main__":
    from lab_checks import check_graph_algorithms

    raise SystemExit(check_graph_algorithms(topological_sort, DisjointSet, kruskal))
