---
layout: default
title: Lab 4
nav_order: 5
---

# CSCI 3212 Lab 4: Binary Search Trees, AVL Rotations, and AVL Insertion

In this lab, you will work with pointer-based binary search trees. You will
trace and implement BST insertion and deletion, profile structural imbalance,
calculate AVL balance factors, implement single and double rotations, and
combine them into iterative and recursive AVL insertion.

This lab uses **pointer-based linked trees**: nodes with explicit child and
parent references (`left`, `right`, `parent`). For two-child BST deletions, the
**in-order successor** (minimum of the right subtree) replaces the deleted
node. Subtree height is defined such that an empty child has height `-1` and a
leaf has height `0`. Balance factors are computed as
$\text{BF}(v) = \text{height}(v.\text{left}) - \text{height}(v.\text{right})$.

## Files and deliverables

| File | Your work |
|---|---|
| `README.md` | Complete the trace tables and written responses in your lab notes or a copy of this file |
| `bst_practice.py` | Implement `bst_insert` and `bst_delete`; search, minimum, and transplant are provided |
| `rotation_practice.py` | Implement `balance_factor`, `rotate_left`, `rotate_right`, `rotate_left_right`, `rotate_right_left`, `avl_insert_iterative`, and `avl_insert_recursive`; `print_tree` is provided for debugging |
| `lab_checks.py` | Provided checks and profiling demonstration; do not edit |

- [ ] Part 1: BST insertion and deletion traces, implementation, and short answers.
- [ ] Part 2: Imbalance search path trace and violation diagnostics.
- [ ] Part 3: AVL rotation trace, implementations, and short answer.
- [ ] Part 4: Iterative and recursive AVL insertion implementations and comparison.
- [ ] Run both practice files and resolve all failed checks.

Keep the function names and parameters unchanged. Do not use `sorted` or
`list.sort` to implement the required functions. The provided checks inspect
pointer identities, in-order traversals, parent references, and node heights
directly.

## Counting and height conventions

- Height of `None` is `-1`.
- Height of a leaf node (both children `None`) is `0`.
- Height of an internal node is $1 + \max(\text{height}(\text{left}), \text{height}(\text{right}))$.
- Balance factor is $\text{height}(v.\text{left}) - \text{height}(v.\text{right})$.
- An AVL node is balanced if $\text{BF}(v) \in \{-1, 0, 1\}$. It is left-heavy if $\text{BF}(v) > 0$ and right-heavy if $\text{BF}(v) < 0$.
- Depth of the root is `0`. Depth increases by `1` along each downward edge.
- Search comparisons count comparisons between element keys.

---

## Part 1: Binary Search Tree Pointer Insertion and Deletion

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
| **Case 3 (2 children)** | Find `y = tree_minimum(z.right)`. If `y != z.right`, splice `y` out using `transplant(tree, y, y.right)` and rewire `y.right = z.right`. Finally `transplant(tree, z, y)` and rewire `y.left = z.left`. |

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

### 1.1 Trace: Insertion

Trace inserting the keys `[40, 20, 60, 10, 30, 50, 70]` into an initially empty
BST.

**TODO 1.1:** Complete the table below. For each inserted key, identify its
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

### 1.2 Trace: Deletion

Starting from the tree built in 1.1 with keys `[10, 20, 30, 40, 50, 60, 70]`,
perform the following three deletions sequentially:

1. Delete key `10`
2. Delete key `20`
3. Delete key `40`

**TODO 1.2:** Complete the table below. Identify the deletion case (0 children,
1 child, or 2 children), the successor key used (if applicable), which node was
spliced out, and the in-order traversal after the deletion. The first row is
worked.

| Target key | Deletion case | Successor key | Node spliced / replaced | In-order traversal afterward |
|---|---|---|---|---|
| 10 | 0 children (leaf) | None | 10 | `[20, 30, 40, 50, 60, 70]` |
| 20 | TODO | TODO | TODO | TODO |
| 40 | TODO | TODO | TODO | TODO |

### 1.3 Implementation

**TODO 1.3A:** Implement `bst_insert(tree, key)` in `bst_practice.py`.

**TODO 1.3B:** Implement `bst_delete(tree, key)` in `bst_practice.py`. Use the
provided `transplant` helper and `tree_minimum` function.

```bash
python3 bst_practice.py
```

### 1.4 Short answers

**TODO 1.4A:** In a two-child deletion (Case 3), why is the in-order successor
guaranteed never to have a left child?

**TODO 1.4B:** When deleting the root node of the tree, what special pointer
updates must take place regarding `tree.root` and `node.parent`?

All three basic BST operations (search, insert, delete) run in $O(h)$ time,
where $h$ is the height of the tree. The iterative implementations require
$O(1)$ auxiliary space.

---

## Part 2: Structural Degeneration, Balance Factors, and Diagnostics

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

### 2.1 Trace: Search-path comparison

**TODO 2.1:** Search for target key `7` in both trees above. Record every node
visited, in order, and the total number of key comparisons.

| Tree | Search path to key `7` | Total comparisons |
|---|---|---|
| Degenerate BST | TODO | TODO |
| Balanced BST | TODO | TODO |

The test suite in `lab_checks.py` demonstrates the difference empirically by
searching for key `999` among 1,000 keys: 1,000 node comparisons on a
degenerate tree versus only 9 on a balanced tree (including the matching node).

### 2.2 Height balance factors and violation signatures

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

For example, inserting `[30, 20, 10]` into an empty BST produces a left chain.
Its heights and balance factors are:

| Node key | Subtree height | Left child height | Right child height | Balance factor $\text{BF}$ |
|---|---|---|---|---|
| 10 | 0 | -1 | -1 | 0 |
| 20 | 1 | 0 | -1 | +1 |
| 30 | 2 | 1 | -1 | +2 |

### 2.3 Trace: Diagnose the four cases

Each insertion order below builds a 3-node BST with no rebalancing.

**TODO 2.3:** For each tree, sketch its shape, compute heights and balance
factors, then identify the unbalanced node $z$ and its BF, the heavier child and
its BF, the violation signature (LL, RR, LR, or RL), and the exact rotation call
that repairs it. The first row is worked.

| Insertion order | Unbalanced node and BF | Heavier child and BF | Signature | Repair |
|---|---|---|---|---|
| `[30, 20, 10]` | `30`, +2 | `20`, +1 | LL | `rotate_right(tree, 30)` |
| `[10, 20, 30]` | TODO | TODO | TODO | TODO |
| `[30, 10, 20]` | TODO | TODO | TODO | TODO |
| `[10, 30, 20]` | TODO | TODO | TODO | TODO |

AVL trees strictly guarantee height $h < 1.44 \log_2(n + 2)$, ensuring
$O(\log n)$ worst-case search.

---

## Part 3: AVL Rotation Primitives

Rotations are local pointer-rewiring transformations that alter the height of
subtrees without altering the in-order traversal of keys.

Before implementing the rotation functions, work through the illustrated cases:

**Visual guide:** [AVL Rotation Images and Cases](AVL_ROTATION_GUIDE.md)

The guide covers the **LL**, **RR**, **LR**, and **RL** cases. The missing final
RL drawing uses the same left rotation shown in the RR case.

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

### 3.1 Trace: Right rotation

Trace `rotate_right(tree, 30)` on the LL tree built from `[30, 20, 10]` (30 is
the root, 20 is its left child, and 10 is 20's left child).

**TODO 3.1:** Complete the table below with each node's pointers and height
*after* the rotation. The first row is worked.

| Node | Parent after | Left after | Right after | Height after |
|---|---|---|---|---|
| 20 | `None` (root) | 10 | 30 | 1 |
| 10 | TODO | TODO | TODO | TODO |
| 30 | TODO | TODO | TODO | TODO |

Confirm that the in-order traversal of the keys remains `[10, 20, 30]` both
before and after the rotation.

### 3.2 Implementation

Open `rotation_practice.py` and implement the five functions:

- **TODO 3.2A:** `balance_factor(node)`
- **TODO 3.2B:** `rotate_left(tree, x)`
- **TODO 3.2C:** `rotate_right(tree, y)`
- **TODO 3.2D:** `rotate_left_right(tree, z)`
- **TODO 3.2E:** `rotate_right_left(tree, z)`

Use `tree.print_tree()` to print the tree with heights, balance factors, and
parent pointers while debugging.

```bash
python3 rotation_practice.py
```

The AVL insertion checks will report `[TODO]` until you finish Part 4.

### 3.3 Short answer: Height update order

**TODO 3.3:** When rotating node $x$ to the left around its right child $y$, why
must the height of $x$ be recalculated before the height of $y$?

A single rotation modifies a fixed set of pointers and updates 2 height fields,
taking $\Theta(1)$ time and $\Theta(1)$ auxiliary space. A double rotation
consists of two single rotations, also running in $\Theta(1)$ time.

---

## Part 4: Iterative and Recursive AVL Insertion

AVL insertion is ordinary BST insertion followed by a **rebalancing pass** over
the ancestors of the new node. On the way back up toward the root, each
ancestor's height is recomputed and its balance factor is checked. At the first
ancestor $z$ with $|\text{BF}(z)| = 2$, apply the rotation from the table in
2.2. After an insertion, one single or double rotation restores the subtree to
its original height, so no ancestor above it needs another rotation.

Because the new key was just inserted below $z$, comparing the key to $z$'s
child is enough to pick the signature:

- $\text{BF}(z) > 1$ and `key < z.left.key` $\rightarrow$ LL; otherwise LR.
- $\text{BF}(z) < -1$ and `key > z.right.key` $\rightarrow$ RR; otherwise RL.

There are two natural ways to visit the ancestors:

1. **Iterative:** Insert with a loop exactly like `BST-INSERT`, then follow
   `parent` pointers from the new node's parent up to the root.
2. **Recursive:** Recurse down to the empty slot. As each call returns, it
   rebalances its own node and returns the (possibly new) root of its subtree
   to the caller.

### Pseudocode

```text
REBALANCE(T, node, key)
  UPDATE-HEIGHT(node)
  bf = BALANCE-FACTOR(node)
  if bf > 1
    if key < node.left.key
      ROTATE-RIGHT(T, node)        // LL
    else
      ROTATE-LEFT-RIGHT(T, node)   // LR
    return true
  if bf < -1
    if key > node.right.key
      ROTATE-LEFT(T, node)         // RR
    else
      ROTATE-RIGHT-LEFT(T, node)   // RL
    return true
  return false

AVL-INSERT-ITERATIVE(T, key)
  inserted = BST-INSERT(T, key)    // return early on a duplicate key
  current = inserted.parent
  while current != None
    if REBALANCE(T, current, key)
      break
    current = current.parent
  return inserted

AVL-INSERT-RECURSIVE(T, key)
  INSERT-SUBTREE(node, parent)
    if node == None
      inserted = Node(key, parent)
      return inserted
    if key < node.key
      node.left = INSERT-SUBTREE(node.left, node)
    else if key > node.key
      node.right = INSERT-SUBTREE(node.right, node)
    else
      inserted = node
      return node                  // duplicate key
    if REBALANCE(T, node, key)
      return node.parent           // the node that rotated into this position
    return node
  T.root = INSERT-SUBTREE(T.root, None)
  T.root.parent = None
  return inserted
```

### 4.1 Implementation

Implement both versions in `rotation_practice.py`. Both must return the inserted
`Node` (or the existing node for a duplicate key) and keep all heights and
parent pointers correct.

- **TODO 4.1A:** `avl_insert_iterative(tree, key)`
- **TODO 4.1B:** `avl_insert_recursive(tree, key)`

```bash
python3 rotation_practice.py
```

### 4.2 Compare the two insertion methods

Insert the keys `[30, 10, 20]` into an empty AVL tree, once with each method.

**TODO 4.2:** Answer the following:

1. **Iterative insertion:** After inserting `20`, in what order does the
   algorithm visit the ancestors, and how does it move between them?
2. **Recursive insertion:** After inserting `20`, in what order do the
   recursive calls finish rebalancing their nodes?
3. Which node is the first unbalanced node in each version?
4. How much extra memory does each version use, in terms of the tree height
   $h$? Explain why they differ.

Both versions run in $O(\log n)$ time because an AVL tree has height
$O(\log n)$ and each rebalancing step does $O(1)$ work.

---

## Final check

Run both practice files from within the `lab4/` directory:

```bash
python3 bst_practice.py
python3 rotation_practice.py
```

- Any unfinished function reports `[TODO]`.
- Any logic error or failed assertion reports `[FAIL]`.
- Any fully working function reports `[PASS]`.

Each practice file exits with a nonzero exit code if any check is unfinished or
failing. When all checks pass, both commands return exit code `0`.
