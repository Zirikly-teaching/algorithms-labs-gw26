---
layout: default
title: Lab 8
nav_order: 9
---

# CSCI 3212 Lab 8: Graph Traversals

Graph traversals let us explore connections between vertices. We can use them
to find a route through a network, check which vertices are reachable, or
visit every part of a graph.

This lab covers the graph representations and traversals from lecture:

1. **Part 1: Representing a Graph:** Read an adjacency list and compare it with an adjacency matrix.
2. **Part 2: Breadth-First Search (BFS):** Explore one level at a time and recover a shortest path.
3. **Part 3: Depth-First Search (DFS):** Follow each branch, then backtrack while recording discovery and finishing times.

## Files and deliverables

| File | Your work |
|---|---|
| `README.md` | Complete two short traces and the analysis questions |
| `graph_traversals.py` | Complete `bfs`, `reconstruct_path`, and `dfs` |
| `lab_checks.py` | Provided automated checks; do not edit |

- [ ] Part 2: Trace BFS, implement it, and reconstruct a path.
- [ ] Part 3: Trace and implement DFS, then compare traversal costs.

---

## Part 1: Representing a Graph

A graph has **vertices** and **edges** connecting them. An **adjacency list**
stores each vertex's neighbors. An **adjacency matrix** has one row and column
per vertex; entry `[u][v]` is `1` when there is an edge from `u` to `v`, and
`0` otherwise.

We will use the undirected graph from the BFS lecture, with one isolated
vertex, `5`, added:

```text
0 ----- 1
|       | \
|       |  3       5
|       | /
2 ----- 4
```

The provided `EXAMPLE_GRAPH` stores it as a Python list of lists:

```python
EXAMPLE_GRAPH = [
    [1, 2],     # neighbors of 0
    [0, 3, 4],  # neighbors of 1
    [0, 4],     # neighbors of 2
    [1, 4],     # neighbors of 3
    [1, 2, 3],  # neighbors of 4
    [],         # neighbors of 5
]
```

For example, `graph[1]` gives `[0, 3, 4]`. In a matrix, row `1` would be
`[1, 0, 0, 1, 1, 0]`. Each undirected edge appears in both endpoints' lists.
For a directed graph, `graph[u]` lists only the vertices that `u` points to.

### Conventions

- Vertices are integers `0` through `len(graph) - 1`. Every neighbor is a valid vertex.
- Visit neighbors **in the order listed**. The DFS outer loop visits vertices in increasing order.
- Keep the input graph unchanged. The provided graph and tests are ready to use.
- Use `None` for a missing parent and `float("inf")` for an unreachable BFS distance.

---

## Part 2: Breadth-First Search

### Background: Explore one level at a time

BFS uses a **FIFO queue**: the first vertex added is the first removed.
Starting at a source, it discovers that vertex's neighbors, then their
neighbors, and so on. In an unweighted graph, this finds paths with the
fewest edges.

When BFS first discovers `v` from `u`, it marks `v` visited, sets
`dist[v] = dist[u] + 1`, and records `parent[v] = u`. Marking a vertex when
it enters the queue prevents another vertex from adding it again.

Starting at `0`, we remove `0` and discover `1` and `2`. Both get distance
`1` and parent `0`; the queue becomes `[1, 2]`. Vertex `5` cannot be reached
from `0`, so its distance stays infinite.

### Pseudocode

```text
BFS(graph, source)
  visited = array of False
  dist = array of infinity
  parent = array of None
  visited[source] = True
  dist[source] = 0
  Q = queue containing source
  while Q is not empty
    u = dequeue front of Q
    for v in graph[u]
      if not visited[v]
        visited[v] = True
        dist[v] = dist[u] + 1
        parent[v] = u
        enqueue v at back of Q
  return (dist, parent)
```

All arrays have one entry per vertex. In Python, use the provided `deque`
import: `append(v)` adds to the back and `popleft()` removes from the front.

### 2.1 Trace: Queue and parents

**TODO 2.1:** Continue BFS from source `0`. Record the queue after each vertex
has had all its neighbors checked, with the front on the left. List only
newly assigned parents.

| Vertex removed | Queue afterward | New parent assignments |
|---|---|---|
| 0 | `[1, 2]` | `parent[1] = 0`, `parent[2] = 0` |
| 1 | `[2, 3, 4]` | `parent[3] = 1`, `parent[4] = 1` |
| 2 | `[3, 4]` | None |
| 3 | `[4]` | None |

Why does processing `2` leave `parent[4]` unchanged? Answer in one sentence.

Though 2 is also a neighbor of 4, 4 was first reached through the queue when 1 was dequeued, therefore it was the original parent and remains even though 2 is also potential parent of 4, but only if it were processed first before 1.

### 2.2 Implementation

**TODO 2.2:** Complete `bfs(graph, source)` in `graph_traversals.py`.
Return `(dist, parent)` as two lists. The initialization is provided.
Assume `source` is a valid vertex.

### 2.3 Recover a shortest path

The parent list lets us work backward from a target to the source. Follow
those pointers, collect the vertices, then reverse the list. For example,
parents `parent[2] = 0` and `parent[0] = None` give the path `[0, 2]`.

```text
RECONSTRUCT-PATH(parent, source, target)
  path = []
  current = target
  while current is not None
    append current to path
    current = parent[current]
  reverse path
  if path[0] == source
    return path
  return []
```

**TODO 2.3:** Complete `reconstruct_path(parent, source, target)` using the
parent list returned by BFS from `source`. Return `[]` if the target is
unreachable and `[source]` if the source and target are the same. Both
indices are valid. Python's `path.reverse()` is allowed.

---

## Part 3: Depth-First Search

### Background: Follow a branch, then backtrack

DFS visits an unvisited neighbor and continues from there. When that vertex
has no unvisited neighbors left, the recursive call returns and the previous
vertex resumes checking its neighbors. Python's call stack keeps track of
where to return.

The lecture uses three colors:

| Color | Meaning |
|---|---|
| WHITE | Not yet discovered |
| GRAY | Discovered; its recursive call is still active |
| BLACK | Finished checking its neighbors |

DFS also records two times for each vertex: `discovered[u]` when it turns
GRAY and `finished[u]` when it turns BLACK. One shared counter increases at
each of these events. `parent[u]` records which vertex first discovered `u`.

On our graph, DFS starts at `0`, then follows `1`, then `3`. While these calls
are active, all three vertices are GRAY. When a call finishes, its vertex
turns BLACK. After finishing the component containing `0`, the outer loop
starts another traversal at `5`. Together, these traversals form a **DFS
forest**; each root has parent `None`.

### Pseudocode

```text
DFS(graph)
  color = array of WHITE
  parent = array of None
  discovered = array of zeros
  finished = array of zeros
  time = 0

  VISIT(u)
    time = time + 1
    discovered[u] = time
    color[u] = GRAY
    for v in graph[u]
      if color[v] == WHITE
        parent[v] = u
        VISIT(v)
    color[u] = BLACK
    time = time + 1
    finished[u] = time

  for u = 0 to number of vertices - 1
    if color[u] == WHITE
      VISIT(u)
  return (parent, discovered, finished)
```

### 3.1 Trace: Discovery and finishing times

**TODO 3.1:** Trace DFS on `EXAMPLE_GRAPH`, starting the clock at `0`.
Complete the selected vertices below. Keep the same clock when moving to
vertex `5`.

| Vertex | Parent | Discovery time | Finishing time |
|---|---|---|---|
| 0 | `None` | 1 | 10 |
| 3 | `[1]` | 3 | 8 |
| 4 | `[3]` | 4 | 7 |
| 5 | `None` | 11 | 12 |

### 3.2 Implementation

**TODO 3.2:** Complete `dfs(graph)` in `graph_traversals.py`. Fill in the
nested `visit(u)` function and the outer loop. The supplied `nonlocal time`
lets `visit` update the counter shared by all recursive calls.

Return `(parent, discovered, finished)` as three lists. Visit every vertex,
including disconnected components. For an empty graph, return three empty
lists. Use the provided color constants.

### 3.3 Representation and traversal costs

**TODO 3.3:** Let $V$ be the number of vertices and $E$ the number of edges.
Complete the table with tight bounds. Assume an undirected, connected graph
so BFS from one source reaches every vertex. For the matrix version, finding
a vertex's neighbors requires scanning its entire row.

| Cost | Adjacency list | Adjacency matrix |
|---|---|---|
| Store the graph | `O(V + E)` | `O(V^2)` |
| Run BFS | `O(V + E)` | `O(V^2)` |
| Run DFS | `O(V + E)` | `O(V^2)` |

In a few sentences, explain how many neighbor entries each traversal checks
with each representation. Why does a sparse graph benefit from adjacency lists?

---

## Final check

Run the provided file from within `lab8/`:

```bash
python3 graph_traversals.py
```

Unfinished functions report `[TODO]`, incorrect results report `[FAIL]`, and
successful checks report `[PASS]`. The checks cover cycles, directed edges,
disconnected vertices, shortest paths, and DFS timestamps. When all checks
pass, the command returns exit code `0`.
