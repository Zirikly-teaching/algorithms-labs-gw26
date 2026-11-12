---
layout: default
title: Lab 5
nav_order: 6
---

# CSCI 3212 Lab 5: AVL Tree Deletion and Rebalancing

In this lab, you will extend your AVL tree implementation from Lab 4 by implementing
deletion with post-deletion rebalancing. You will trace and implement AVL deletion,
analyze why deletions require more complex rebalancing than insertions, and
empirically compare insertion and deletion cost.

This lab reuses the pointer-based linked AVL trees and rotation infrastructure
from Lab 4. Deletion follows the same three BST deletion cases (0, 1, 2 children),
then rebalances every ancestor of the deleted node on the way up toward the root.
Unlike insertion, a single deletion can trigger **multiple independent rotations**
at different ancestors.

## Files and deliverables

| File | Your work |
|---|---|
| `README.md` | Complete the trace tables and written responses in your lab notes or a copy of this file |
| `avl_practice.py` | Implement `avl_delete` and complete the rebalancing loop; rotation functions from Lab 4 are provided |
| `lab_checks.py` | Provided checks and profiling demonstration; do not edit |

- [x] Part 1: AVL deletion strategy, rebalancing pass conceptual understanding
- [x] Part 2: Deletion traces (single rotation, double rotation, multiple rotations)
- [x] Part 3: Implement `avl_delete` with post-deletion rebalancing
- [x] Part 4: Analyze and compare insertion vs. deletion cost
- [x] Run the practice file and resolve all failed checks.

Keep the function names and parameters unchanged. The provided checks inspect
pointer identities, in-order traversals, parent references, node heights, and
balance factors directly.

---

## Part 1: AVL Deletion Strategy

### Why deletion is harder than insertion

In Lab 4, AVL insertion was structured as: **insert → walk ancestors up → fix at most one violation**.
A single insertion creates a single "problem zone" (the inserted key's ancestors),
and one rotation fixes the entire subtree.

AVL deletion is fundamentally different:

1. **Multiple violation zones:** Deleting a node can cause imbalances at multiple
   ancestors simultaneously.
2. **Cascading rebalancing:** After fixing an imbalance at ancestor $z$ with a rotation,
   the rotated subtree may have a different height than before. This can cause a new
   imbalance higher up.
3. **Propagate further:** Unlike insertion (which stops after one rotation), deletion
   must check every ancestor all the way to the root. After each rotation, the
   rebalancing loop continues.

**Key insight:** An insertion at height $h$ changes the subtree's height by at most 1
locally, stopping rebalancing immediately. A deletion can propagate height changes
all the way to the root.

### Post-deletion rebalancing strategy

```text
AVL-DELETE(T, key)
  z = BST-DELETE(T, key)          // Perform BST deletion; z is the deleted node (or None)
  current = parent_of_deleted     // Start rebalancing from the parent of the deleted node
  while current != None
    UPDATE-HEIGHT(current)        // Recompute height after structural change
    bf = BALANCE-FACTOR(current)
    if |bf| >= 2                  // Imbalance detected
      // Determine which case (LL, RR, LR, RL) and rotate
      // Unlike insertion, the key is NOT available—use bf signs instead
      if bf > 1                   // Left-heavy
        if BALANCE-FACTOR(current.left) >= 0
          ROTATE-RIGHT(T, current)          // LL
          current = current.parent          // Move up after rotation
        else
          ROTATE-LEFT-RIGHT(T, current)     // LR
          current = current.parent          // Move up after rotation
      else if bf < -1             // Right-heavy
        if BALANCE-FACTOR(current.right) <= 0
          ROTATE-LEFT(T, current)           // RR
          current = current.parent          // Move up after rotation
        else
          ROTATE-RIGHT-LEFT(T, current)     // RL
          current = current.parent          // Move up after rotation
    current = current.parent      // Continue to next ancestor
  return z
```

**Critical difference from insertion:** After a rotation in insertion, the rebalancing
stops immediately. In deletion, we must continue up the tree. The rotated subtree may
have a different height, creating imbalances higher up.

### 1.1 Short answer: BST deletion reminder

**Answer 1.1:**
- If the target node has 0 children, it is removed and its parent is relinked to None.
- If it has 1 child, that child is spliced into the deleted node's position, and the parent of the deleted node points to the child.
- If it has 2 children, replace it with its in-order successor. The successor is used because it is the next key in sorted order, and it has at most one child, which makes the deletion case reduce cleanly to the 0 or 1 child case while preserving the BST invariant.

### 1.2 Short answer: Height change after deletion

**Answer 1.2:**
- When a leaf is deleted, the leaf's parent may lose one level of height, but only if that leaf was the last node on one side of the subtree. In the worst case, the parent's height decreases by 1.
- Yes, the grandparent's height can change because the subtree rooted at the parent may now be shorter than before.
- Yes, the imbalance can propagate upward to the root. Unlike insertion, deletion can reduce subtree heights at multiple ancestors, so rebalancing must continue until the root is checked.

---

## Part 2: AVL Deletion Traces

### Example: AVL trees for deletion traces

For the traces below, we use AVL trees built carefully so that deletions trigger imbalances.

### 2.1 Trace: Single rotation after deletion

Start with this AVL tree:
```
      30
     /  \
   20    40
   /
  10
```
(All nodes balanced: 30 has BF=1, 20 has BF=1, others BF=0.)

**Answer 2.1:** Delete key `40` from this tree. Trace the rebalancing:

1. Deleting the leaf `40` leaves the tree:
   ```
       30
      /
    20
    /
   10
   ```
2. Rebalance from the parent of the deleted node (30).
3. At 30, the left subtree height is 2 and the right subtree height is -1, so BF(30) = 2.
4. This is an LL imbalance because 30 is left-heavy and 20 is also left-heavy.
5. A single right rotation at 30 fixes it. The tree becomes balanced immediately, so no further rebalancing is needed.
6. Final tree and in-order traversal:
   ```
       20
      / \
     10  30
   ```
   In-order: [10, 20, 30]

| Step | Action | Tree state | Unbalanced node | BF | Signature | Rotation | Notes |
|---|---|---|---|---|---|---|---|
| 1 | Delete 40 | 40 is removed (leaf) | - | - | - | - | Tree now has 30 root, 20 left, nothing right |
| 2 | Rebalance from 30 | 30 is left-heavy | 30 | 2 | LL | Right rotation at 30 | Fixes the violation |
| 3 | After rotation | 20 is root, 30 is right child | - | - | - | - | Final state, balanced |

### 2.2 Trace: Double rotation after deletion

Start with this AVL tree:
```
      30
     /  \
   10    40
    \
    20
```
(All nodes balanced: 30 has BF=0, 10 has BF=-1, others BF=0.)

**Answer 2.2:** Delete key `40` from this tree. Trace the rebalancing:

1. Deleting the leaf `40` leaves:
   ```
       30
      / \
    10  -
      \
       20
   ```
2. Rebalance from 30.
3. At 30, BF(30) = 2 because the left subtree height is 1 and the right subtree is -1.
4. The violation is an LR case: 30 is left-heavy, and its left child 10 is right-heavy (BF(10) = -1).
5. A double rotation is needed: rotate left at 10, then right at 30.
6. Final tree and in-order traversal:
   ```
       20
      / \
    10  30
   ```
   In-order: [10, 20, 30]

| Step | Action | Current node | BF before | Signature | Rotation applied | BF after |
|---|---|---|---|---|---|---|
| 1 | Delete 40 | 30 | 2 | LR | left at 10, then right at 30 | 0 at 20/30 |
| 2 | Verify final | - | - | - | - | Balanced tree, inorder [10, 20, 30] |

### 2.3 Trace: Two-child deletion with rebalancing

Start with this AVL tree:
```
        50
       /  \
      30   70
     / \     \
   20  40    80
   /
  10
```
(All balanced initially.)

**Answer 2.3:** Delete key `30`. This is a 2-child deletion (has both 20 and 40 as children).

1. The in-order successor of `30` is `40`.
2. Replace 30 with 40; since 40 has no children, the subtree becomes:
```
       50
      /  \
    40    70
   /      \
 20       80
 /
10
```
3. Rebalance from 40 because that is the node where the structural change happened.
4. At 40, BF(40) = 2 because the left subtree has height 1 and the right side is empty, so this is an LL imbalance. The correct fix is a right rotation at 40.
5. After the rotation, the subtree becomes balanced and the root remains valid. No further rotations are required.

| Step | Current node | BF | Imbalanced? | Violation | Rotation applied |
|---|---|---|---|---|---|
| 1 | 40 | 2 | Yes | LL | Right rotation at 40 |
| 2 | 50 | 1 | No | - | None |

---

## Part 3: Implementation

Open `avl_practice.py` and implement the deletion function:

### 3.1 Implement AVL deletion

**TODO 3.1:** Complete `avl_delete(tree, key)` in `avl_practice.py`.

The skeleton is provided. Complete the rebalancing loop to:
1. Identify the parent of the deleted node to start rebalancing from.
2. Walk up from that node to the root, checking and fixing each ancestor.
3. Return the deleted node (or `None` if key not found).

Your implementation must:
- Correctly identify the rebalancing start point for all three BST deletion cases.
- Update heights and balance factors as you walk up.
- Recognize and apply the correct rotation for each violation signature (LL, RR, LR, RL).
- **Continue rebalancing at every ancestor** (unlike insertion, which stops after one rotation).

Provided helpers (already implemented):
- `transplant(tree, u, v)` - updates tree pointers
- `tree_minimum(node)` - finds minimum in subtree
- `tree_search(node, key)` - searches for key
- `balance_factor(node)` - returns BF
- `rotate_left(tree, node)`, `rotate_right(tree, node)` - single rotations
- `rotate_left_right(tree, node)`, `rotate_right_left(tree, node)` - double rotations
- `update_height(node)` - recalculates node's height

```bash
python3 avl_practice.py
```

---

## Part 4: Insertion vs. Deletion Comparison

Once deletion is working, the test suite runs a profiling experiment:
insert and delete 1000 random keys into an AVL tree,
measuring the number of rotations triggered by each operation.

### 4.1 Short answer: Why is deletion costlier?

**Answer 4.1:**

1. A single deletion can trigger multiple rotations at different ancestors because deleting a node can shrink the height of several subtrees along the path from the deleted node back to the root. Each ancestor may independently become imbalanced, so must keep walking upward and rebalancing until the tree is valid again. A single insertion only changes one local subtree and typically creates at most one imbalance on the insertion path.
2. The crucial property is that a valid AVL rotation restores the subtree height to its pre-violation height, so once the offending subtree is fixed, the height change is absorbed locally and no higher ancestor is affected.
3. No, a deletion never needs to rebalance higher than the root. The root has no parent, so once the check reaches the root and the tree is valid, there is nowhere else to propagate. The loop stops when current becomes None after the root has been processed.

### 4.2 Short answer: Real-world implications

**Answer 4.2:** Consider a scenario where an application frequently inserts and deletes values in an AVL tree (for example, a priority queue or cache).

1. Based on rotation cost, deletions should be slower than insertions. A deletion can trigger multiple repairs on the path back to the root, whereas insertion typically stops after a single rotation.
2. If deletions become the bottleneck, a binary heap is often a better choice for a priority queue because it supports insertion and removal of the maximum or minimum in O(log n) time without AVL-style rebalancing rotations.

---

## Final check

Run the practice file from within the `lab5/` directory:

```bash
python3 avl_practice.py
```

- Any unfinished function reports `[TODO]`.
- Any logic error or failed assertion reports `[FAIL]`.
- Any fully working function reports `[PASS]`.

The practice file exits with a nonzero exit code if any check is unfinished or
failing. When all checks pass, the command returns exit code `0`.

The profiling output compares insertion vs. deletion rotation counts on random keys
and provides empirical evidence of why deletion is costlier.
