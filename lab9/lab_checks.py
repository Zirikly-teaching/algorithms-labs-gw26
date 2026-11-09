"""Provided checks for Lab 9. No third-party packages required."""

from copy import deepcopy


def check_graph_algorithms(topological_sort, DisjointSet, kruskal):
    """Run named checks and return zero only when every check passes."""
    cases = []

    def require(condition, message):
        if not condition:
            raise AssertionError(message)

    def add_case(name, function, args, expected):
        def test():
            inputs = deepcopy(args)
            before = deepcopy(inputs)
            actual = function(*inputs)
            require(actual == expected, f"expected {expected!r}, got {actual!r}")
            require(inputs == before, "input graph or edge list was modified")
        cases.append((name, test))

    topo_cases = [
        ("lecture DAG", [[1, 2], [3], [3], [4], []], [0, 1, 2, 3, 4]),
        ("multiple initial sources", [[2], [2], [], []], [0, 1, 3, 2]),
        ("listed neighbor order", [[2, 1], [], []], [0, 2, 1]),
        ("all isolated", [[], [], []], [0, 1, 2]),
        ("empty graph", [], []),
        ("cycle with blocked descendant", [[1], [2], [1, 3], []], None),
        ("disconnected cycle", [[], [2], [1]], None),
        ("self-loop", [[0]], None),
    ]
    for name, graph, expected in topo_cases:
        add_case("Topological sort: " + name, topological_sort, (graph,), expected)

    def test_find_root():
        sets = DisjointSet(4)
        require(sets.find(2) == 2, "a singleton is its own root")
        require(sets.parent == [0, 1, 2, 3], "singleton parents changed")

    def test_compression():
        sets = DisjointSet(5)
        # a valid rank tree with a two-edge path from 3 to 0
        sets.parent = [0, 0, 0, 2, 4]
        sets.rank = [2, 0, 1, 0, 0]
        require(sets.find(3) == 0, "find(3) must return 0")
        require(sets.parent == [0, 0, 0, 0, 4], "the path from 3 was not compressed")
        require(sets.rank == [2, 0, 1, 0, 0], "find must leave ranks unchanged")

    def test_rank_ties():
        sets = DisjointSet(4)
        for x, y in [(0, 1), (2, 3), (1, 2)]:
            require(sets.union(x, y) is True, "union must report a new merge")
        require(sets.parent == [0, 0, 0, 2], "equal-rank roots must follow the tie rule")
        require(sets.rank == [2, 0, 1, 0], "incorrect rank updates")

    def test_unequal_ranks():
        sets = DisjointSet(5)
        sets.union(0, 1)
        sets.union(2, 3)
        require(sets.union(4, 0) is True, "singleton should join the larger-rank tree")
        require(sets.parent[4] == 0 and sets.rank[0] == 1, "smaller first root attached incorrectly")
        sets.union(0, 2)
        require(sets.parent[2] == 0 and sets.rank[0] == 2, "equal-rank merge failed")
        require(sets.find(3) == 0, "all four original vertices should be connected")

    def test_repeated_union():
        sets = DisjointSet(3)
        sets.union(0, 1)
        before = sets.rank[:]
        require(sets.union(1, 0) is False, "already-connected vertices must return False")
        require(sets.union(2, 2) is False, "union with itself must return False")
        require(sets.rank == before, "a repeated union must not increase rank")

    cases.extend([
        ("Find: singleton", test_find_root),
        ("Find: path compression", test_compression),
        ("Union: lecture tie rule", test_rank_ties),
        ("Union: ranks and non-root arguments", test_unequal_ranks),
        ("Union: already connected", test_repeated_union),
    ])

    lecture = [(0, 1, 1), (2, 3, 2), (1, 2, 3), (1, 3, 4),
               (0, 2, 5), (3, 4, 6), (2, 4, 7)]
    mst_cases = [
        ("lecture edges, unsorted", 5, list(reversed(lecture)),
         ([(0, 1, 1), (2, 3, 2), (1, 2, 3), (3, 4, 6)], 12)),
        ("stable weight ties", 4, [(2, 3, 1), (0, 2, 1), (0, 3, 1), (1, 3, 1)],
         ([(2, 3, 1), (0, 2, 1), (1, 3, 1)], 3)),
        ("negative weights", 3, [(0, 2, 5), (1, 2, -1), (0, 1, -3)],
         ([(0, 1, -3), (1, 2, -1)], -4)),
        ("disconnected forest", 5, [(0, 1, 4), (2, 3, 2)],
         ([(2, 3, 2), (0, 1, 4)], 6)),
        ("no edges", 3, [], ([], 0)),
        ("self-loop rejected", 2, [(0, 0, -10), (0, 1, 2)], ([(0, 1, 2)], 2)),
        ("single vertex", 1, [], ([], 0)),
        ("empty graph", 0, [], ([], 0)),
    ]
    for name, n, edges, expected in mst_cases:
        add_case("Kruskal: " + name, kruskal, (n, edges), expected)

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
