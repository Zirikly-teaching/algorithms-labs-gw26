---
layout: default
title: Lab 3
nav_order: 4
---

# CSCI 3212 Lab 3: Heaps and Binary Search Trees

In this lab, you will explore both array-based binary trees and pointer-based
binary search trees. You will implement Max-Heap sift-down and the ascending
Heapsort algorithm structure, trace and implement pointer-based BST insertion
and deletion, and profile structural imbalance.

This lab uses two primary tree representations:
1. **Array-based binary heaps:** Complete binary trees mapped onto 0-based
   lists using index formulas $\text{left}(i) = 2i + 1$,
   $\text{right}(i) = 2i + 2$, and $\text{parent}(i) = \lfloor (i - 1)/2 \rfloor$.
   For Heapsort, this lab uses **Max-Heaps** to sort in standard **ascending
   order**.
2. **Pointer-based linked trees:** Nodes with explicit child and parent
   references (`left`, `right`, `parent`). For two-child BST deletions, the
   **in-order successor** (minimum of the right subtree) replaces the deleted
   node. Subtree height is defined such that an empty child has height `-1` and a
   leaf has height `0`.

## Files and deliverables

| File | Your work |
|---|---|
| `README.md` | Complete the trace tables and written responses in your lab notes or a copy of this file |
| `heap_practice.py` | Implement `max_heapify_down` and complete `heap_sort`; bottom-up heap construction is provided |
| `bst_practice.py` | Implement `bst_insert` and `bst_delete`; search, minimum, and transplant are provided |
| `lab_checks.py` | Provided checks; do not edit |

- [ ] Part 1: Max-Heap sift-down trace, Heapsort extraction trace, implementation, and short answers.
- [ ] Part 2: BST insertion and deletion traces, implementation, and short answers.
- [ ] Part 3: Compare search paths in degenerate and balanced BSTs.
- [ ] Run both practice files and resolve all failed checks.

Keep the function names and parameters unchanged. Do not use `sorted`,
`list.sort`, or `heapq` to implement the required functions. The provided checks
inspect array mutations, pointer identities, in-order traversals, parent
references directly.

## Counting and height conventions

- Array indices are 0-based.
- Height of `None` is `-1`.
- Height of a leaf node (both children `None`) is `0`.
- Height of an internal node is $1 + \max(\text{height}(\text{left}), \text{height}(\text{right}))$.
- Depth of the root is `0`. Depth increases by `1` along each downward edge.
- Search comparisons count comparisons between element keys.

---

## Part 1: Binary Heaps and the Heapsort Structure

A **binary heap** is a complete binary tree represented sequentially inside an
array. Because every level except possibly the last is completely filled from
left to right, no explicit child or parent pointers are stored:
- $\text{left}(i) = 2i + 1$
- $\text{right}(i) = 2i + 2$
- $\text{parent}(i) = \lfloor (i - 1)/2 \rfloor$

Binary heaps come in two fundamental forms:
- **Min-Heap:** Every node satisfies $A[\text{parent}(i)] \le A[i]$. The
  minimum element is always at index `0`.
- **Max-Heap:** Every node satisfies $A[\text{parent}(i)] \ge A[i]$. The
  maximum element is always at index `0`.

**In a Max-Heap, every parent element is greater than or equal to both of its children, guaranteeing the absolute maximum element always resides at index 0.**

*Note: A node is a leaf node if there is no left child (2i + 1 ≥ n,  or,   i ≥ n // 2), where **n** is the active heap size*

### In-place Heapsort mechanics

Heapsort sorts an array entirely in place with $O(1)$ auxiliary space:
1. **Build a Max-Heap:** Transform an arbitrary array into a valid Max-Heap
   using bottom-up heap construction (`build_max_heap`).
2. **Repeated Extraction:** The maximum element is at `arr[0]`. Swap `arr[0]`
   with `arr[end]`, moving the maximum into its final position at the end of the
   array.
3. **Active Heap Shrink:** Decrement the active heap size (`end`). The sorted
   suffix begins at `end` and remains frozen.
4. **Sift-Down:** Call `max_heapify_down(arr, 0, end)` to restore the Max-Heap
   property over the reduced active range `0` to `end - 1`.

Repeating this process produces an array sorted in standard **ascending order**.

| Structure / Property | Min-Heap | Max-Heap |
|---|---|---|
| Invariant | Parent $\le$ Children | Parent $\ge$ Children |
| Root element (`arr[0]`) | Global Minimum | Global Maximum |
| Sift-down compares with | Smallest child | Largest child |
| Heapsort output order | Descending order | Ascending order |

### Pseudocode

```text
MAX-HEAPIFY-DOWN(arr, i, heap_size)
  while true
    left = 2 * i + 1
    right = 2 * i + 2
    largest = i
    if left < heap_size and arr[left] > arr[largest]
      largest = left
    if right < heap_size and arr[right] > arr[largest]
      largest = right
    if largest != i
      swap arr[i] with arr[largest]
      i = largest
    else
      break

BUILD-MAX-HEAP(arr)
  for i from floor(length(arr) / 2) - 1 down to 0
    MAX-HEAPIFY-DOWN(arr, i, length(arr))

HEAP-SORT(arr)
  BUILD-MAX-HEAP(arr)
  for end from length(arr) - 1 down to 1
    swap arr[0] with arr[end]
    MAX-HEAPIFY-DOWN(arr, 0, end)
  return arr
```

### 1.1 Trace: Sift-down in a Max-Heap

Trace `max_heapify_down(arr, 0, 7)` on the array `[4, 10, 8, 5, 1, 2, 7]`
where child subtrees are already valid max-heaps.

**TODO 1.1:** Complete the table below tracing each swap during sift-down.
Record the current index `i`, its child indices and values, the largest index,
and the array state after each step. The first row is worked.

| Step | Current `i` | Value at `i` | Children (left, right) | Largest index | Action taken | Array afterward |
|---|---|---|---|---|---|---|
| 1 | 0 | 4 | `left=1` (10), `right=2` (8) | 1 | Swap `arr[0]` with `arr[1]` | `[10, 4, 8, 5, 1, 2, 7]` |
| 2 | 1 | 4 | `left=3` (5), `right=4` (1) | 3 | Swap `arr[1]` with `arr[3]` | `[10, 5, 8, 4, 1, 2, 7]` |
| 3 | 3 | 4 | `left=7` (-), `right=8` (-) | break | break | break |

### 1.2 Trace: Heapsort extraction passes

Consider the initial 7-element Max-Heap `[15, 12, 8, 6, 2, 3, 7]`.

**TODO 1.2:** Complete the table below for each extraction pass of `heap_sort`.
Record the root swap, active heap size, active heap state after sift-down, and
the growing sorted suffix. Pass 1 is worked.

| Pass (`end`) | Swap root with `arr[end]` | Active heap size | Active heap after `max_heapify_down` | Sorted suffix | Full array afterward |
|---|---|---|---|---|---|
| 6 | Swap `15` with `7` | 6 | `[12, 7, 8, 6, 2, 3]` | `[15]` | `[12, 7, 8, 6, 2, 3, 15]` |
| 5 | Swap `12` with `15` | 6 | `[15, 8, 7, 6, 2, 3]` | `[12]` | `[15, 8, 7, 6, 2, 3, 12]` |
| 4 | Swap `15` with `7` | TODO | TODO | TODO | TODO |
| 3 | Swap `15` with `7` | TODO | TODO | TODO | TODO |
| 2 | Swap `15` with `7` | TODO | TODO | TODO | TODO |
| 1 | Swap `15` with `7` | TODO | TODO | TODO | TODO |

Record the final sorted array returned by `heap_sort`.

### 1.3 Implementation

**TODO 1.3A:** Implement `max_heapify_down(arr, i, heap_size)` in `heap_practice.py`.

**TODO 1.3B:** Implement the extraction loop of `heap_sort(arr)` in `heap_practice.py`.

```bash
python3 heap_practice.py
```

### 1.4 Short answers

**TODO 1.4A:** Why does using a Max-Heap produce an *ascending* sort when
repeatedly extracting the root to the end of the array, whereas using a Min-Heap
produces a descending sort?

**TODO 1.4B:** Bottom-up heap construction (`build_max_heap`) takes $O(n)$ time,
yet `heap_sort` overall requires $O(n \log n)$ time. Where does the additional
time come from during the sorting phase?

Building a heap takes $\Theta(n)$ time. Each of the $n - 1$ extractions performs
at most $O(\log n)$ sift-down work, yielding $\Theta(n \log n)$ total time and
$\Theta(1)$ auxiliary space.

---

## Part 2: Binary Search Tree Pointer Insertion and Deletion

A Binary Search Tree satisfies the **BST invariant**: for every node $v$ with
key $k$, all keys in the left subtree of $v$ are strictly less than $k$, and all
keys in the right subtree of $v$ are strictly greater than $k$ (assuming unique
keys).

Each node maintains pointers to its `left` child, `right` child, and `parent`.
The tree container object holds a reference to `root`.

When inserting a new key, we traverse down from `root` until finding an empty
slot, attach a new `Node(key, parent=...)`, and link the parent's `left` or
`right` pointer.

Deletion is divided into three structural cases depending on how many children
the target node $z$ possesses:
1. **0 children (leaf):** Disconnect $z$ from its parent.
2. **1 child:** Bypass $z$ by connecting $z$'s parent directly to $z$'s sole child.
3. **2 children:** Locate $z$'s in-order successor $y$ (the minimum key in $z$'s
   right subtree). Replace $z$ with $y$. If $y$ is not $z$'s immediate right child,
   $y$'s own right child is spliced into $y$'s former position before $y$ takes
   $z$'s place.

**In a two-child BST deletion, replacing the target node with its in-order successor preserves the sorted search property across the entire tree, and the successor itself always has at most one child.**

### Node structure and deletion cases

| Attribute / Case | Pointer / Structural Action |
|---|---|
| `node.left` | Points to left child or `None` |
| `node.right` | Points to right child or `None` |
| `node.parent` | Points to parent node or `None` (for `root`) |
| **Case 1 (0 children)** | `transplant(tree, z, None)` |
| **Case 2 (1 child)** | `transplant(tree, z, z.left)` if `z.right is None`, else `transplant(tree, z, z.right)` |
| **Case 3 (2 children)** | Find $y = \text{tree\_minimum}(z.\text{right})$. If $y \ne z.\text{right}$, splice $y$ out using `transplant(tree, y, y.right)` and rewire $y.\text{right} = z.\text{right}$. Finally `transplant(tree, z, y)` and rewire $y.\text{left} = z.\text{left}$. |

### Pseudocode

```text
BST-INSERT(T, key)
  z = Node(key)
  parent = None
  current = T.root
  while current != None
    parent = current
    if key < current.key
      current = current.left
    else if key > current.key
      current = current.right
    else
      return current  // duplicate key
  z.parent = parent
  if parent == None
    T.root = z
  else if key < parent.key
    parent.left = z
  else
    parent.right = z
  return z

TRANSPLANT(T, u, v)
  if u.parent == None
    T.root = v
  else if u == u.parent.left
    u.parent.left = v
  else
    u.parent.right = v
  if v != None
    v.parent = u.parent

BST-DELETE(T, key)
  z = BST-SEARCH(T.root, key)
  if z == None
    return None
  if z.left == None
    TRANSPLANT(T, z, z.right)
  else if z.right == None
    TRANSPLANT(T, z, z.left)
  else
    y = TREE-MINIMUM(z.right)
    if y.parent != z
      TRANSPLANT(T, y, y.right)
      y.right = z.right
      y.right.parent = y
    TRANSPLANT(T, z, y)
    y.left = z.left
    y.left.parent = y
  return z
```

### 2.1 Trace: Insertion

Trace inserting the keys `[40, 20, 60, 10, 30, 50, 70]` into an initially empty
BST.

**TODO 2.1:** Complete the table below. For each inserted key, identify its
parent node, whether it becomes the left or right child, and record the in-order
traversal of the tree after insertion. The first two rows are worked.

| Key | Parent node | Child direction | In-order traversal afterward |
|---|---|---|---|
| 40 | None (Root) | Root | `[40]` |
| 20 | 40 | Left | `[20, 40]` |
| 60 | 40 | Right | `[20, 40, 60]` |
| 10 | 20 | Left | `[10, 20, 40, 60]`  |
| 30 | 20 | Right | `[10, 20, 30, 40, 60]` |
| 50 | 60 | Left | `[10, 20, 30, 40, 50, 60]` |
| 70 | 60 | Right | `[10, 20, 30, 40, 50, 60, 70]` |

### 2.2 Trace: Deletion

Starting from the tree built in 2.1 with keys `[10, 20, 30, 40, 50, 60, 70]`,
perform the following three deletions sequentially:
1. Delete key `10`
2. Delete key `20`
3. Delete key `40`

**TODO 2.2:** Complete the table below. Identify the deletion case (0 children,
1 child, or 2 children), the successor key used (if applicable), which node was
spliced out, and the in-order traversal after the deletion. The first row is
worked.

| Target key | Deletion case | Successor key | Node spliced / replaced | In-order traversal afterward |
|---|---|---|---|---|
| 10 | 0 children (leaf) | None | 10 | `[20, 30, 40, 50, 60, 70]` |
| 20 | TODO | TODO | TODO | TODO |
| 40 | TODO | TODO | TODO | TODO |

### 2.3 Implementation

**TODO 2.3A:** Implement `bst_insert(tree, key)` in `bst_practice.py`.

**TODO 2.3B:** Implement `bst_delete(tree, key)` in `bst_practice.py`. Use the
provided `transplant` helper and `tree_minimum` function.

```bash
python3 bst_practice.py
```

### 2.4 Short answers

**TODO 2.4A:** In a two-child deletion (Case 3), why is the in-order successor
guaranteed never to have a left child?

**TODO 2.4B:** When deleting the root node of the tree, what special pointer
updates must take place regarding `tree.root` and `node.parent`?

All three basic BST operations (search, insert, delete) run in $O(h)$ time,
where $h$ is the height of the tree. The iterative implementations require
$O(1)$ auxiliary space.

---

## Part 3: Structural Degeneration

Because an unaugmented BST does not rebalance itself, its shape is determined
by the order in which keys are inserted.

**The shape and height of an unaugmented BST are entirely determined by the insertion order of its keys.**

Inserting keys in sorted order `[1, 2, 3, 4, 5, 6, 7]` creates a degenerate
chain of height $n - 1 = 6$ with $O(n)$ search depth. Inserting in balanced
order (medians first: `[4, 2, 6, 1, 3, 5, 7]`) yields a tree of height
$\lfloor \log_2 n \rfloor = 2$ with $O(\log n)$ search depth.

| Structure | Insertion order | Tree height | Search complexity |
|---|---|---|---|
| **Degenerate BST** | Ascending: `[1, 2, 3, 4, 5, 6, 7]` | $n - 1 = 6$ | $O(n)$ |
| **Balanced BST** | Medians first: `[4, 2, 6, 1, 3, 5, 7]` | $\lfloor \log_2 n \rfloor = 2$ | $O(\log n)$ |

### 3.1 Search-path comparison

Search for key `7` in each tree above. Record the nodes visited in order (ie: `1->2->3`) and
the total number of key comparisons.

| Tree | Search path to key `7` | Total comparisons |
|---|---|---|
| Degenerate BST |  |  |
| Balanced BST |  |  |

---

## Final check

Run both practice files from within the `lab3/` directory:

```bash
python3 heap_practice.py
python3 bst_practice.py
```

- Any unfinished function reports `[TODO]`.
- Any logic error or failed assertion reports `[FAIL]`.
- Any fully working function reports `[PASS]`.

Each practice file exits with a nonzero exit code if any check is unfinished or
failing. When all checks pass, both commands return exit code `0`.
