"""Provided checks for Lab 8. No third-party packages required."""

from copy import deepcopy


def check_graph_traversals(bfs, reconstruct_path, dfs):
    """Run named checks and return zero only when all checks pass."""
    inf = float("inf")
    example = [[1, 2], [0, 3, 4], [0, 4], [1, 4], [1, 2, 3], []]
    directed = [[1, 2], [3], [3], [], [0]]
    ordered = [[2, 1], [3], [3], []]
    cycle = [[1], [2], [0], []]
    cases = []

    def add_case(name, function, args, expected):
        def test():
            # give every check fresh inputs and catch accidental graph edits
            inputs = deepcopy(args)
            before = deepcopy(inputs)
            actual = function(*inputs)
            if actual != expected:
                raise AssertionError(f"expected {expected!r}, got {actual!r}")
            if inputs != before:
                raise AssertionError("input graph or parent list was modified")
        cases.append((name, test))

    bfs_cases = [
        ("lecture graph", example, 0,
         ([0, 1, 1, 2, 2, inf], [None, 0, 0, 1, 1, None])),
        ("isolated source", example, 5,
         ([inf, inf, inf, inf, inf, 0], [None] * 6)),
        ("directed edges", directed, 0,
         ([0, 1, 1, 2, inf], [None, 0, 0, 1, None])),
        ("nonzero source", directed, 4,
         ([1, 2, 2, 3, 0], [4, 0, 0, 1, None])),
        ("listed neighbor order", ordered, 0,
         ([0, 1, 1, 2], [None, 0, 0, 2])),
        ("cycle", cycle, 0,
         ([0, 1, 2, inf], [None, 0, 1, None])),
        ("self-loop", [[0]], 0, ([0], [None])),
        ("single vertex", [[]], 0, ([0], [None])),
    ]
    for name, graph, source, expected in bfs_cases:
        add_case("BFS: " + name, bfs, (graph, source), expected)

    path_cases = [
        ("lecture path", [None, 0, 0, 1, 1, None], 0, 4, [0, 1, 4]),
        ("unreachable target", [None, 0, 0, 1, 1, None], 0, 5, []),
        ("source equals target", [None, 0, 0, 1, 1, None], 0, 0, [0]),
        ("nonzero source", [4, 0, 0, 1, None], 4, 3, [4, 0, 1, 3]),
        ("parent zero", [None, 0], 0, 1, [0, 1]),
        ("isolated source", [None, None, None], 2, 2, [2]),
    ]
    for name, parent, source, target, expected in path_cases:
        add_case("Path: " + name, reconstruct_path, (parent, source, target), expected)

    dfs_cases = [
        ("lecture graph and isolated vertex", example,
         ([None, 0, 4, 1, 3, None], [1, 2, 5, 3, 4, 11], [10, 9, 6, 8, 7, 12])),
        ("directed graph", directed,
         ([None, 0, 0, 1, None], [1, 2, 6, 3, 9], [8, 5, 7, 4, 10])),
        ("listed neighbor order", ordered,
         ([None, 0, 0, 2], [1, 6, 2, 3], [8, 7, 5, 4])),
        ("cycle", cycle,
         ([None, 0, 1, None], [1, 2, 3, 7], [6, 5, 4, 8])),
        ("isolated vertices", [[], [], []],
         ([None, None, None], [1, 3, 5], [2, 4, 6])),
        ("self-loop", [[0]], ([None], [1], [2])),
        ("empty graph", [], ([], [], [])),
    ]
    for name, graph, expected in dfs_cases:
        add_case("DFS: " + name, dfs, (graph,), expected)

    def check_bfs_path_together():
        graph = deepcopy(example)
        dist, parent = bfs(graph, 0)
        path = reconstruct_path(parent, 0, 3)
        if path != [0, 1, 3] or len(path) - 1 != dist[3]:
            raise AssertionError("path to 3 must be [0, 1, 3] with distance 2")
        if graph != example:
            raise AssertionError("input graph was modified")
    cases.append(("BFS and path reconstruction together", check_bfs_path_together))

    failed = 0
    for name, test in cases:
        try:
            test()
            print("[PASS] " + name)
        except NotImplementedError as error:
            failed += 1
            print("[TODO] " + name + ": " + str(error))
        except Exception as error:
            failed += 1
            print("[FAIL] " + name + ": " + type(error).__name__ + ": " + str(error))
    print(f"{len(cases) - failed}/{len(cases)} checks passed")
    return 1 if failed else 0
