---
layout: default
title: Lab 3
nav_order: 4
---

# CSCI 3212 Lab 3: Heaps, Binary Search Trees, and AVL Rotations

In this lab, you will explore both array-based binary trees and pointer-based
binary search trees. You will implement Max-Heap sift-down and the ascending
Heapsort algorithm structure, trace and implement pointer-based BST insertion
and deletion, profile structural imbalance, calculate AVL balance factors, and
implement atomic single and double rotations.

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
   leaf has height `0`. Balance factors are computed as
   $\text{BF}(v) = \text{height}(v.\text{left}) - \text{height}(v.\text{right})$.

## Files and deliverables

| File | Your work |
|---|---|
| `README.md` | Complete the trace tables and written responses in your lab notes or a copy of this file |
| `heap_practice.py` | Implement `max_heapify_down` and complete `heap_sort`; bottom-up heap construction is provided |
| `bst_practice.py` | Implement `bst_insert` and `bst_delete`; search, minimum, and transplant are provided |
| `rotation_practice.py` | Implement `balance_factor`, `rotate_left`, `rotate_right`, `rotate_left_right`, and `rotate_right_left` |
| `lab_checks.py` | Provided checks and profiling demonstration; do not edit |

- [ ] Part 1: Max-Heap sift-down trace, Heapsort extraction trace, implementation, and short answers.
- [ ] Part 2: BST insertion and deletion traces, implementation, and short answers.
- [ ] Part 3: Imbalance search path trace, balance factor calculations, violation diagnostics, and short answers.
- [ ] Part 4: AVL rotation trace, implementations, and short answers.
- [ ] Run all three practice files and resolve all failed checks.

Keep the function names and parameters unchanged. Do not use `sorted`,
`list.sort`, or `heapq` to implement the required functions. The provided checks
inspect array mutations, pointer identities, in-order traversals, parent
references, and node heights directly.

## Counting and height conventions

- Array indices are 0-based.
- Height of `None` is `-1`.
- Height of a leaf node (both children `None`) is `0`.
- Height of an internal node is $1 + \max(\text{height}(\text{left}), \text{height}(\text{right}))$.
- Balance factor is $\text{height}(v.\text{left}) - \text{height}(v.\text{right})$.
- An AVL node is balanced if $\text{BF}(v) \in \{-1, 0, 1\}$. It is left-heavy if $\text{BF}(v) > 0$ and right-heavy if $\text{BF}(v) < 0$.
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
| 2 | TODO | TODO | TODO | TODO | TODO | TODO |
| 3 | TODO | TODO | TODO | TODO | TODO | TODO |

### 1.2 Trace: Heapsort extraction passes

Consider the initial 7-element Max-Heap `[15, 12, 8, 6, 2, 3, 7]`.

**TODO 1.2:** Complete the table below for each extraction pass of `heap_sort`.
Record the root swap, active heap size, active heap state after sift-down, and
the growing sorted suffix. Pass 1 is worked.

| Pass (`end`) | Swap root with `arr[end]` | Active heap size | Active heap after `max_heapify_down` | Sorted suffix | Full array afterward |
|---|---|---|---|---|---|
| 6 | Swap `15` with `7` | 6 | `[12, 7, 8, 6, 2, 3]` | `[15]` | `[12, 7, 8, 6, 2, 3, 15]` |
| 5 | TODO | TODO | TODO | TODO | TODO |
| 4 | TODO | TODO | TODO | TODO | TODO |
| 3 | TODO | TODO | TODO | TODO | TODO |
| 2 | TODO | TODO | TODO | TODO | TODO |
| 1 | TODO | TODO | TODO | TODO | TODO |

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
| 60 | TODO | TODO | TODO |
| 10 | TODO | TODO | TODO |
| 30 | TODO | TODO | TODO |
| 50 | TODO | TODO | TODO |
| 70 | TODO | TODO | TODO |

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

## Part 3: Structural Degeneration, Balance Factors, and Diagnostics

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

### 3.1 Trace: Search Path Comparison

Consider searching for target key `7` in both trees.

**TODO 3.1:** Complete the table tracing the search path for target key `7` in
the degenerate tree versus the balanced tree.

| Step | Degenerate BST: Node visited | Degenerate: Key comparison | Degenerate: Node depth | Balanced BST: Node visited | Balanced: Key comparison | Balanced: Node depth |
|---|---|---|---|---|---|---|
| 1 | 1 | `7 > 1` (go right) | 0 | 4 | `7 > 4` (go right) | 0 |
| 2 | TODO | TODO | TODO | TODO | TODO | TODO |
| 3 | TODO | TODO | TODO | TODO | TODO | TODO |
| 4 | TODO | TODO | TODO | — | — | — |
| 5 | TODO | TODO | TODO | — | — | — |
| 6 | TODO | TODO | TODO | — | — | — |
| 7 | TODO | TODO | TODO | — | — | — |

Record total comparisons: Degenerate: **TODO**, Balanced: **TODO**.

### Height balance factors and violation signatures

An **AVL tree** maintains the **balance invariant**:
$$\text{BF}(v) = \text{height}(v.\text{left}) - \text{height}(v.\text{right}) \in \{-1, 0, 1\} \quad \text{for all nodes } v$$

When a node insertion causes $|\text{BF}(z)| \ge 2$ at some ancestor $z$, an
imbalance has occurred. The lowest ancestor where this violation occurs is
categorized into one of four **violation signatures**:

| Signature | Name | Condition at ancestor $z$ | Condition at heavier child | Required rebalancing action |
|---|---|---|---|---|
| **LL** | Left-Left | $\text{BF}(z) = +2$ | $\text{BF}(z.\text{left}) \ge 0$ | Single `rotate_right(tree, z)` |
| **RR** | Right-Right | $\text{BF}(z) = -2$ | $\text{BF}(z.\text{right}) \le 0$ | Single `rotate_left(tree, z)` |
| **LR** | Left-Right | $\text{BF}(z) = +2$ | $\text{BF}(z.\text{left}) < 0$ | Double: `rotate_left(tree, z.left)` then `rotate_right(tree, z)` |
| **RL** | Right-Left | $\text{BF}(z) = -2$ | $\text{BF}(z.\text{right}) > 0$ | Double: `rotate_right(tree, z.right)` then `rotate_left(tree, z)` |

**An AVL violation occurs at the lowest ancestor where the height difference between left and right subtrees reaches 2 or -2, and the required rotation is uniquely determined by the sign of the ancestor's balance factor and its heavier child's balance factor.**

### 3.2 Trace: Heights and Balance Factors

Consider four 3-node trees constructed by inserting keys in different orders:
- **Tree 1 (Keys [30, 20, 10]):** 30 has left child 20; 20 has left child 10.
- **Tree 2 (Keys [10, 20, 30]):** 10 has right child 20; 20 has right child 30.
- **Tree 3 (Keys [30, 10, 20]):** 30 has left child 10; 10 has right child 20.
- **Tree 4 (Keys [10, 30, 20]):** 10 has right child 30; 30 has left child 20.

**TODO 3.2:** Complete the table below computing height and balance factor for
each node. Remember that an empty child has height `-1`. Tree 1 is worked.

| Tree | Node key | Subtree height | Left child height | Right child height | Balance factor $\text{BF}$ |
|---|---|---|---|---|---|
| 1 (LL) | 10 | 0 | -1 | -1 | 0 |
| 1 (LL) | 20 | 1 | 0 | -1 | +1 |
| 1 (LL) | 30 | 2 | 1 | -1 | +2 |
| 2 (RR) | 30 | TODO | TODO | TODO | TODO |
| 2 (RR) | 20 | TODO | TODO | TODO | TODO |
| 2 (RR) | 10 | TODO | TODO | TODO | TODO |
| 3 (LR) | 20 | TODO | TODO | TODO | TODO |
| 3 (LR) | 10 | TODO | TODO | TODO | TODO |
| 3 (LR) | 30 | TODO | TODO | TODO | TODO |
| 4 (RL) | 20 | TODO | TODO | TODO | TODO |
| 4 (RL) | 30 | TODO | TODO | TODO | TODO |
| 4 (RL) | 10 | TODO | TODO | TODO | TODO |

### 3.3 Trace: Violation Diagnostics

**TODO 3.3:** For each of the four trees above, identify the unbalanced ancestor
$z$, diagnose its violation signature (LL, RR, LR, or RL), and specify the
exact rotation function call(s) required to restore balance. Tree 1 is worked.

| Tree | Unbalanced node $z$ | $\text{BF}(z)$ | Child node inspected | Child $\text{BF}$ | Signature | Restorative rotation call(s) |
|---|---|---|---|---|---|---|
| 1 | 30 | +2 | 20 | +1 | LL | `rotate_right(tree, 30)` |
| 2 | TODO | TODO | TODO | TODO | TODO | TODO |
| 3 | TODO | TODO | TODO | TODO | TODO | TODO |
| 4 | TODO | TODO | TODO | TODO | TODO | TODO |

### 3.4 Short answers

**TODO 3.4A:** What common real-world data patterns (such as timestamped logs or
pre-sorted datasets) inadvertently construct worst-case degenerate BSTs?

**TODO 3.4B:** Why does a single right rotation around node `30` fail to balance
Tree 3 (the Left-Right tree with keys 30, 10, 20)? What structure results if a
single rotation is attempted?

The test suite in `lab_checks.py` demonstrates the difference empirically by
searching 1,000 keys: 999 comparisons on a degenerate tree versus only 8 on a
balanced tree. AVL trees strictly guarantee height $h < 1.44 \log_2(n + 2)$,
ensuring $O(\log n)$ worst-case search.

---

## Part 4: AVL Rotation Primitives

Rotations are local pointer-rewiring transformations that alter the height of
subtrees without altering the in-order traversal of keys.

Before implementing the rotation functions, work through the illustrated cases:

**Visual guide:** [AVL Rotation Images and Cases](AVL_ROTATION_GUIDE.md)

The guide presents the cases in increasing order of complexity: **LL**, **RR**,
**LR**, and **RL**. It shows the tree after each available rotation and explains
how the missing final RL drawing mirrors the simpler RR rotation.

**Rotations alter the pointer structure and heights of nodes to restore balance while strictly preserving the in-order traversal order of all keys.**

### Single Right Rotation (`rotate_right(tree, y)`)
In a right rotation around node $y$, $y$'s left child $x$ becomes the new root
of the subtree:
1. $x$'s right subtree becomes $y$'s left subtree.
2. $y$ becomes $x$'s right child.
3. Parent pointers are updated for $x$, $y$, and the transferred subtree.
4. The heights of $y$ and $x$ are recalculated (in that order: $y$ first, then $x$).

### Single Left Rotation (`rotate_left(tree, x)`)
The symmetric mirror of right rotation: $x$'s right child $y$ becomes the new
root of the subtree:
1. $y$'s left subtree becomes $x$'s right subtree.
2. $x$ becomes $y$'s left child.
3. Parent pointers are updated for $y$, $x$, and the transferred subtree.
4. The heights of $x$ and $y$ are recalculated (in that order: $x$ first, then $y$).

### Double Rotations
- **`rotate_left_right(tree, z)`**: Performs `rotate_left(tree, z.left)` followed
  by `rotate_right(tree, z)`.
- **`rotate_right_left(tree, z)`**: Performs `rotate_right(tree, z.right)` followed
  by `rotate_left(tree, z)`.

### Pseudocode

```text
ROTATE-LEFT(T, x)
  y = x.right
  x.right = y.left
  if y.left != None
    y.left.parent = x
  y.parent = x.parent
  if x.parent == None
    T.root = y
  else if x == x.parent.left
    x.parent.left = y
  else
    x.parent.right = y
  y.left = x
  x.parent = y
  UPDATE-HEIGHT(x)
  UPDATE-HEIGHT(y)

ROTATE-RIGHT(T, y)
  x = y.left
  y.left = x.right
  if x.right != None
    x.right.parent = y
  x.parent = y.parent
  if y.parent == None
    T.root = x
  else if y == y.parent.left
    y.parent.left = x
  else
    y.parent.right = x
  x.right = y
  y.parent = x
  UPDATE-HEIGHT(y)
  UPDATE-HEIGHT(x)

ROTATE-LEFT-RIGHT(T, z)
  ROTATE-LEFT(T, z.left)
  ROTATE-RIGHT(T, z)

ROTATE-RIGHT-LEFT(T, z)
  ROTATE-RIGHT(T, z.right)
  ROTATE-LEFT(T, z)
```

### 4.1 Trace: Right Rotation

Trace `rotate_right(tree, 30)` on Tree 1 (keys `[30, 20, 10]`, where 30 is the root,
20 is its left child, and 10 is 20's left child).

**TODO 4.1:** Complete the table below comparing the pointers and heights of the
three nodes before and after `rotate_right(tree, 30)`. The first two rows are
worked.

| Node key | Parent before | Left child before | Right child before | Height before | Parent after | Left child after | Right child after | Height after |
|---|---|---|---|---|---|---|---|---|
| 30 | None | 20 | None | 2 | 20 | None | None | 0 |
| 20 | 30 | 10 | None | 1 | None (Root) | 10 | 30 | 1 |
| 10 | TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO |

Confirm that the in-order traversal of the keys remains `[10, 20, 30]` both
before and after the rotation.

### 4.2 Implementation

Open `rotation_practice.py` and implement the five functions:
- **TODO 4.2A:** `balance_factor(node)`
- **TODO 4.2B:** `rotate_left(tree, x)`
- **TODO 4.2C:** `rotate_right(tree, y)`
- **TODO 4.2D:** `rotate_left_right(tree, z)`
- **TODO 4.2E:** `rotate_right_left(tree, z)`

```bash
python3 rotation_practice.py
```

### 4.3 Short answers

**TODO 4.3A:** When rotating node $x$ to the left around child $y$, why must the
height of $x$ be recalculated before the height of $y$?

**TODO 4.3B:** Why do single and double rotations execute in strictly $O(1)$
time, regardless of whether the tree contains 3 nodes or 3,000,000 nodes?

A single rotation modifies a fixed set of 6 pointers and updates 2 height
fields, taking $\Theta(1)$ time and $\Theta(1)$ auxiliary space. A double rotation
consists of two single rotations, also running in $\Theta(1)$ time and
$\Theta(1)$ auxiliary space.

---

## Final check

Run all three practice files from within the `lab_3/` directory:

```bash
python3 heap_practice.py
python3 bst_practice.py
python3 rotation_practice.py
```

- Any unfinished function reports `[TODO]`.
- Any logic error or failed assertion reports `[FAIL]`.
- Any fully working function reports `[PASS]`.

Each practice file exits with a nonzero exit code if any check is unfinished or
failing. When all checks pass, all three commands return exit code `0`.
