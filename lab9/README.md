---
layout: default
title: Lab 9
nav_order: 10
---

# CSCI 3212 Lab 9: Topological Sorting and Minimum Spanning Trees

This week, we use graphs to solve two problems: put tasks in an order that
respects their dependencies, and connect all vertices at the lowest total
cost. We will build on the queues and DFS ideas from Lab 8.

1. **Part 1: Topological Sorting:** Implement Kahn's algorithm and detect when a cycle makes an ordering impossible.
2. **Part 2: Minimum Spanning Trees:** Implement union-find, then use it to decide which edges Kruskal's algorithm should keep.

## Files and deliverables

| File | Your work |
|---|---|
| `README.md` | Complete two short traces and two analysis questions |
| `graph_algorithms.py` | Complete the four implementation TODOs |
| `lab_checks.py` | Provided automated checks; do not edit |

- [ ] Part 1: Trace and implement topological sorting.
- [ ] Part 2: Implement union-find and Kruskal, then trace their decisions.

Vertices in the code are numbered `0` through `n - 1`. In the lecture
examples, `A, B, C, D, E` correspond to `0, 1, 2, 3, 4`.
Keep input graphs and edge lists unchanged. All endpoints are valid.

---

## Part 1: Topological Sorting

### Background: Which task is ready next?

In a dependency graph, `u -> v` means that `u` must come before `v`.
A **topological order** lists every vertex once while following all these
rules. Such an order exists exactly when the graph is a **DAG**: a directed
acyclic graph.

For the lecture example, the dependencies are:

```text
A -> B, A -> C, B -> D, C -> D, D -> E
```

Both `B` and `C` must finish before `D` can start. Either may come first,
so a graph can have more than one valid topological order.

Kahn's algorithm keeps an **in-degree** count for each vertex: how many
incoming edges remain. A count of zero means the vertex is ready. Put ready
vertices in a queue. Each time you remove `u`, add it to the output and
subtract one from the in-degree of every neighbor of `u`.

If the queue empties before all vertices reach the output, the graph has a
cycle. Some remaining vertices may also be tasks blocked by that cycle.

### Pseudocode

```text
TOPOLOGICAL-SORT(graph)
  n = number of vertices
  indegree = array of n zeros
  for u = 0 to n - 1
    for v in graph[u]
      indegree[v] = indegree[v] + 1
  Q = queue of all zero-indegree vertices, in increasing order
  order = []
  while Q is not empty
    u = dequeue front of Q
    append u to order
    for v in graph[u]
      indegree[v] = indegree[v] - 1
      if indegree[v] == 0
        enqueue v at back of Q
  if length(order) != n
    return None
  return order
```

### 1.1 Trace: Waiting for both prerequisites

Use the lecture graph above. Its initial in-degrees, in `A` through `E`
order, are `[0, 1, 1, 2, 1]`. Visit neighbors in the order shown.

**TODO 1.1:** Complete these steps. The queue's front is on the left.

| Vertex removed | Queue afterward | In-degree of `D` |
|---|---|---|
| A | `[B, C]` | 2 |
| B | TODO | TODO |
| C | TODO | TODO |

Now add the edge `E -> B`. Which vertices reach the output before the
algorithm stops? What does the function return?

### 1.2 Implementation

**TODO 1.2:** Complete `topological_sort(graph)` in `graph_algorithms.py`.
The graph is a directed adjacency list, as in Lab 8. Return a list containing
all vertices, or `None` if there is a cycle. An empty graph returns `[]`.

Use the provided `deque` import with `append` and `popleft`. Put initial
zero-indegree vertices into the queue in increasing order, then process
neighbors in their listed order. The provided `DAG_EXAMPLE` is the trace graph.

### Connection to DFS

When DFS examines `u -> v`, the colors and discovery times from Lab 8
tell us what kind of edge it is:

| State of `v` | Edge type |
|---|---|
| WHITE | Tree: discovers `v` |
| GRAY | Back: reaches an active ancestor, or itself |
| BLACK, `d[u] < d[v]` | Forward: reaches a finished descendant |
| BLACK, `d[u] > d[v]` | Cross: reaches a finished branch or tree |

A back edge proves there is a directed cycle. If there are no back edges,
appending each vertex when it finishes and reversing that list gives a
topological order. For every edge `u -> v` in a DAG, `v` finishes before `u`.

A topological order also helps with **shortest paths in a weighted DAG**:
process vertices in that order and update each neighbor's distance whenever
`dist[u] + weight(u, v)` improves it. All predecessors of a vertex are
processed before that vertex, so one pass over the edges is enough.

### 1.3 Analysis

**TODO 1.3:** Give the time and extra-space bounds for Kahn's algorithm in
terms of `V` vertices and `E` edges, excluding storage for the input graph.
Briefly explain how often each vertex enters the queue and each edge is checked.

---

## Part 2: Kruskal's Algorithm and Union-Find

### Background: Connect everything cheaply

A **spanning tree** connects every vertex of an undirected graph without
cycles. For `n` vertices, it has `n - 1` edges. A **minimum spanning tree
(MST)** has the smallest possible sum of edge weights.

Kruskal sorts the edges from lightest to heaviest. It keeps an edge when
its endpoints are in different components. If the endpoints are already
connected by the edges kept so far, adding the edge would create a cycle.

Why is the greedy choice safe? A **cut** divides the vertices into two groups.
Choose one current component as a group. No accepted edge leaves that
component, and the next edge Kruskal accepts from it is a lightest edge
crossing the cut. The cut property says that this edge can be added while
keeping the accepted edges part of some MST.

### Union-find: Track the components

A **disjoint-set structure**, or **union-find**, stores each component as a
tree of parent pointers. Initially, every vertex is its own parent.
`find(x)` returns the root of `x`'s component. `union(x, y)` joins two
components and returns whether a merge happened.

Two rules keep these trees short:

- **Path compression:** During `find`, point each vertex on the search path directly at the root.
- **Union by rank:** Attach the smaller-rank root under the larger-rank root. On a tie, attach the second root under the first and increase the first root's rank.

Rank starts at zero. It is an upper bound on height, so path compression
leaves ranks unchanged. These parent pointers describe the components;
the MST's chosen edges are stored separately.

### Pseudocode: Find and union

`parent` and `rank` belong to the provided `DisjointSet` object.

```text
FIND(x)
  if parent[x] != x
    parent[x] = FIND(parent[x])
  return parent[x]

UNION(x, y)
  root_x = FIND(x)
  root_y = FIND(y)
  if root_x == root_y
    return False
  if rank[root_x] < rank[root_y]
    parent[root_x] = root_y
  else if rank[root_x] > rank[root_y]
    parent[root_y] = root_x
  else
    parent[root_y] = root_x
    rank[root_x] = rank[root_x] + 1
  return True
```

### Pseudocode: Kruskal

```text
KRUSKAL(n, edges)
  sets = DisjointSet(n)
  chosen = []
  total = 0
  for (u, v, weight) in edges sorted by weight
    if sets.UNION(u, v)
      append (u, v, weight) to chosen
      total = total + weight
      if length(chosen) == n - 1
        break
  return (chosen, total)
```

Here, `UNION` performs the component check and only merges different sets.
For a disconnected graph, this returns a **minimum spanning forest**: a
minimum spanning tree for each connected component.

### 2.1 Implementation

In the provided `graph_algorithms.py`:

- **TODO 2.1A:** Complete `DisjointSet.find` with path compression.
- **TODO 2.1B:** Complete `DisjointSet.union` with union by rank and the tie rule above.
- **TODO 2.1C:** Complete `kruskal(n, edges)` using those methods.

Edges are tuples `(u, v, weight)`, with each undirected edge listed once.
Weights may be negative or equal. The starter supplies a sorted copy;
equal-weight edges keep their input order. Return `(chosen, total)` with
chosen edges in acceptance order. For zero or one vertex, return `([], 0)`.

### 2.2 Trace: Accept, reject, and compress

Use the lecture's sorted edge list:

```text
(A, B): 1    (C, D): 2    (B, C): 3    (B, D): 4
(A, C): 5    (D, E): 6    (C, E): 7
```

The first three edges are accepted. Their total weight is `6`, and the
union-find arrays, in `A` through `E` order, are:

```text
parent = [A, A, A, C, E]
rank   = [2, 0, 1, 0, 0]
```

**TODO 2.2:** Continue from this state. Record roots after the two `find`
calls, then decide whether the edge is accepted.

| Edge | Roots | Accept? | Total weight |
|---|---|---|---|
| `(B, D): 4` | TODO | TODO | TODO |
| `(A, C): 5` | TODO | TODO | TODO |
| `(D, E): 6` | TODO | TODO | TODO |

After checking `(B, D)`, what is `parent[D]`? Explain why a rejected edge
can still change the parent array. Does Kruskal examine `(C, E): 7`?

### 2.3 Analysis

**TODO 2.3:** For a connected graph, give Kruskal's total time bound,
including initialization and sorting. You may use the lecture's amortized
bound of `O(α(V))` per union-find operation, where `α` grows extremely slowly.
Which step dominates? What changes if the edges are already sorted?

---

## Final check

Run the provided file from within `lab9/`:

```bash
python3 graph_algorithms.py
```

Unfinished functions report `[TODO]`, incorrect results report `[FAIL]`, and
successful checks report `[PASS]`. When all checks pass, the command returns
exit code `0`.
