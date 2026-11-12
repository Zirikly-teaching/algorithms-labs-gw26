"""Complete BFS, path reconstruction, and recursive DFS for Lab 8."""

from collections import deque

WHITE, GRAY, BLACK = 0, 1, 2

EXAMPLE_GRAPH = [
    [1, 2],
    [0, 3, 4],
    [0, 4],
    [1, 4],
    [1, 2, 3],
    [],
]


def bfs(graph, source):
    """Return (dist, parent) lists for BFS from a valid source vertex.

    Use the listed neighbor order. Unreachable distances stay infinite.
    """
    n = len(graph)
    visited = [False] * n
    dist = [float("inf")] * n
    parent = [None] * n
    visited[source] = True
    dist[source] = 0
    queue = deque([source])

    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if not visited[v]:
                visited[v] = True
                dist[v] = dist[u] + 1
                parent[v] = u
                queue.append(v)

    return dist, parent


def reconstruct_path(parent, source, target):
    """Return a source-to-target path, or [] when the target is unreachable.

    parent comes from BFS rooted at source; source and target are valid indices.
    """
    path = []
    current = target

    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()
    if path and path[0] == source:
        return path

    return []

def dfs(graph):
    """Return (parent, discovered, finished) for a full recursive DFS forest.

    Visit roots in increasing order and neighbors in their listed order.
    The shared clock starts at zero and increases on discovery and finishing.
    """
    n = len(graph)
    color = [WHITE] * n
    parent = [None] * n
    discovered = [0] * n
    finished = [0] * n
    time = 0

    def visit(u):
        nonlocal time
        time += 1
        discovered[u] = time
        color[u] = GRAY
        for v in graph[u]:
            if color[v] == WHITE:
                parent[v] = u
                visit(v)
        color[u] = BLACK
        time += 1
        finished[u] = time

    for u in range(n):
        if color[u] == WHITE:
            visit(u)

    return parent, discovered, finished


if __name__ == "__main__":
    from lab_checks import check_graph_traversals

    raise SystemExit(check_graph_traversals(bfs, reconstruct_path, dfs))
