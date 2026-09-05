---
layout: default
title: Lab 2
nav_order: 3
permalink: /lab2/
---

# CSCI 3212 Lab 2: Sorting Traces, Lomuto Partition & Benchmarks, and Array-Backed Binary Trees

In this lab, you will explore three fundamental topics in algorithm design and data structures:
1. **Bubble Sort and Insertion Sort**: Trace step-by-step logic, loop invariants, comparisons vs. swaps/shifts, and early-stopping optimizations.
2. **Lomuto Partition Scheme & Quicksort Benchmarks**: Understand pointer mechanics and invariants of Lomuto partitioning, then run experiments comparing runtimes on **1,000,000 randomized arrays** and pathological edge cases across various pivot strategies.
3. **Representing Binary Trees via Arrays**: Master index arithmetic (0-based and 1-based), parent/child relationships, tree traversals, and binary heap representations without pointers.

## On this page
1. TOC
{:toc}

---

## Part 1: Bubble Sort and Insertion Sort Trace & Logic

### 1.1 Bubble Sort Logic and Invariants

Bubble Sort works by repeatedly sweeping through an array, comparing adjacent elements, and swapping them if they are out of order. 

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr
```

#### Key Mechanics:
1. **The "Bubbling" Effect**: In each pass $i$ (from $0$ to $n-1$), the largest unsorted element "bubbles up" to its correct final position at index $n - 1 - i$.
2. **Loop Invariant**: After pass $k$, the suffix `arr[n-k .. n-1]` consists of the $k$ largest elements in the array in their final, sorted positions.
3. **Early-Stopping Optimization**: The `swapped` boolean flag detects if an entire pass completed without a single swap. If no swaps occurred, the array is already sorted, allowing Bubble Sort to terminate in $O(n)$ time on pre-sorted input.

#### Trace Walkthrough
Consider the array: `[5, 2, 9, 1, 5, 6]` ($n = 6$).

| Pass | Scanning Range | Comparison ($arr[j]$ vs $arr[j+1]$) | Action | Array State | Sorted Suffix |
|---|---|---|---|---|---|
| **1** | $j=0 \dots 4$ | $5 > 2$ | SWAP | `[2, 5, 9, 1, 5, 6]` | |
| | | $5 \le 9$ | KEEP | `[2, 5, 9, 1, 5, 6]` | |
| | | $9 > 1$ | SWAP | `[2, 5, 1, 9, 5, 6]` | |
| | | $9 > 5$ | SWAP | `[2, 5, 1, 5, 9, 6]` | |
| | | $9 > 6$ | SWAP | `[2, 5, 1, 5, 6, 9]` | `[9]` |
| **2** | $j=0 \dots 3$ | $2 \le 5$ | KEEP | `[2, 5, 1, 5, 6, 9]` | |
| | | $5 > 1$ | SWAP | `[2, 1, 5, 5, 6, 9]` | |
| | | $5 \le 5$ | KEEP | `[2, 1, 5, 5, 6, 9]` | |
| | | $5 \le 6$ | KEEP | `[2, 1, 5, 5, 6, 9]` | `[6, 9]` |
| **3** | $j=0 \dots 2$ | $2 > 1$ | SWAP | `[1, 2, 5, 5, 6, 9]` | |
| | | $2 \le 5$ | KEEP | `[1, 2, 5, 5, 6, 9]` | |
| | | $5 \le 5$ | KEEP | `[1, 2, 5, 5, 6, 9]` | `[5, 6, 9]` |
| **4** | $j=0 \dots 1$ | $1 \le 2$ | KEEP | `[1, 2, 5, 5, 6, 9]` | |
| | | $2 \le 5$ | KEEP | `[1, 2, 5, 5, 6, 9]` | `[5, 5, 6, 9]` |
| *Exit* | Pass 4 had 0 swaps -> **Early Termination** | | | `[1, 2, 5, 5, 6, 9]` | **Sorted!** |

---

### 1.2 Insertion Sort Logic and Invariants

Insertion Sort maintains a sorted subarray on the left and repeatedly inserts the next element (the `key`) into its correct relative position by shifting larger elements one slot to the right.

```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]  # Shift right
            j -= 1
        arr[j + 1] = key         # Place key
    return arr
```

#### Key Mechanics:
1. **Loop Invariant**: At the start of iteration $i$, the prefix `arr[0 .. i-1]` contains the original elements from those positions, but in sorted order.
2. **Inversion Sensitivity**: An inversion is a pair $(i, j)$ such that $i < j$ and $arr[i] > arr[j]$. The total number of shifts in Insertion Sort is **exactly equal** to the number of inversions in the array.
#### Insertion Sort Trace Walkthrough
Consider the same array: `[5, 2, 9, 1, 5, 6]` ($n = 6$).

| Step $i$ | Key ($arr[i]$) | Comparisons & Shifts | Insertion Action | Array State | Sorted Prefix |
|---|---|---|---|---|---|
| **Init** | - | - | Prefix of length 1 is sorted | `[5, 2, 9, 1, 5, 6]` | `[5]` |
| **$i=1$** | `2` | $5 > 2 \to$ shift $5$ right | Place `2` at index 0 | `[2, 5, 9, 1, 5, 6]` | `[2, 5]` |
| **$i=2$** | `9` | $5 \le 9 \to$ stop (0 shifts) | Place `9` at index 2 | `[2, 5, 9, 1, 5, 6]` | `[2, 5, 9]` |
| **$i=3$** | `1` | $9>1, 5>1, 2>1 \to$ shift $9, 5, 2$ | Place `1` at index 0 | `[1, 2, 5, 9, 5, 6]` | `[1, 2, 5, 9]` |
| **$i=4$** | `5` | $9 > 5 \to$ shift $9$; $5 \le 5 \to$ stop! | Place `5` at index 3 | `[1, 2, 5, 5, 9, 6]` | `[1, 2, 5, 5, 9]` |
| **$i=5$** | `6` | $9 > 6 \to$ shift $9$; $5 \le 6 \to$ stop! | Place `6` at index 4 | `[1, 2, 5, 5, 6, 9]` | **Sorted!** |

Total Comparisons: **9** &nbsp;|&nbsp; Total Shifts: **6** (equal to the number of inversions!).

---

### 1.3 Algorithm Stability (Preserving Relative Order)

A sorting algorithm is **stable** if elements with equal keys appear in the output in the same relative order as in the initial input.

* **Bubble Sort is Stable**: In `bubble_sort`, adjacent elements are swapped only when `arr[j] > arr[j + 1]`. If two adjacent elements are equal (`arr[j] == arr[j + 1]`), no swap occurs. Therefore, equal elements never jump past one another.
* **Insertion Sort is Stable**: In `insertion_sort`, the inner scan continues while `arr[j] > key`. The moment an element equal to the key is encountered (`arr[j] == key`), the loop terminates. The `key` is placed strictly to the *right* of its equal predecessor, preserving original order.
* **Breaking Stability**: If either comparison is written with a non-strict inequality (`>=`), equal elements will swap past each other, destroying stability!

#### Running the Visual Trace Tool
We have provided [`lab2/sorting_trace.py`](sorting_trace.py) to trace any array step-by-step:
```bash
python sorting_trace.py
```

{: .exercise }
> ### Exercise 1: Tracing & Analysis Questions
> 
> Answer the following in your lab notes or submission:
> 
> ```text
> TODO 1.1:
> Trace Insertion Sort manually on arr = [7, 3, 5, 8, 2].
> For each step i (from 1 to 4), show:
> - The key being inserted
> - The elements shifted
> - The array state after inserting the key
> 
> Step 1 (key = 3): 
> Step 2 (key = 5): 
> Step 3 (key = 8): 
> Step 4 (key = 2): 
> 
> TODO 1.2:
> How many comparisons and swaps does Bubble Sort perform on a reverse-sorted
> array of size N (e.g. [5, 4, 3, 2, 1])? Express your answer in terms of N.
> A:
> 
> TODO 1.3:
> Why does Bubble Sort require an explicit boolean flag (`swapped`) to achieve
> O(N) time on sorted data, whereas Insertion Sort naturally achieves O(N) without any flag?
> A:
> 
> TODO 1.4:
> List all inversions (pairs (i, j) where i < j and arr[i] > arr[j]) in [7, 3, 5, 8, 2].
> How many total inversions are there? Verify that this number exactly equals the total
> number of shifts performed in TODO 1.1.
> Inversions:
> Total count:
> Matches shift count (yes/no)?
> 
> TODO 1.5:
> If a student writes Bubble Sort with `if arr[j] >= arr[j + 1]:`, does the algorithm
> still sort correctly? Does it remain stable? Explain why or why not.
> A:
> ```

---

## Part 2: Lomuto Partition Scheme

Quicksort relies on a **partition function** that picks a pivot element $x$ and rearranges `arr[low .. high]` such that:
- All elements $\le x$ are placed to the left of $x$.
- All elements $> x$ are placed to the right of $x$.
- The pivot $x$ is placed at its final sorted index $p$.

The **Lomuto Partition Scheme** (introduced by Nico Lomuto and featured in the CLRS textbook) uses the last element `arr[high]` as the pivot.

```python
def lomuto_partition(arr, low, high):
    pivot = arr[high]
    i = low - 1  # Boundary of elements <= pivot
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

### 2.1 The Loop Invariant

At the beginning of each iteration of the `for j` loop, the array is partitioned into four regions:

```text
  low          i        i+1        j-1      j          high-1     high
+------------+--------+------------+------+------------+------+-------+
|  <= pivot  |  ...   |  > pivot   | ...  | unexamined | ...  | pivot |
+------------+--------+------------+------+------------+------+-------+
```

1. If $low \le k \le i$, then $arr[k] \le pivot$.
2. If $i+1 \le k \le j-1$, then $arr[k] > pivot$.
3. If $j \le k \le high - 1$, the relation of $arr[k]$ to $pivot$ is not yet determined.
4. If $k = high$, $arr[k] = pivot$.

### 2.2 Trace Example (CLRS Classic)
Trace of `arr = [2, 8, 7, 1, 3, 5, 6, 4]` on `low = 0, high = 7` (Pivot = $4$):

| $j$ | $arr[j]$ | $arr[j] \le 4$? | Action | $i$ | Array State (`arr[0..7]`) |
|---|---|---|---|---|---|
| Init | - | - | Initialize $i = -1$ | $-1$ | `[2, 8, 7, 1, 3, 5, 6, 4]` |
| 0 | 2 | Yes | $i \leftarrow 0$, swap $arr[0]$ with $arr[0]$ | 0 | `[2, 8, 7, 1, 3, 5, 6, 4]` |
| 1 | 8 | No | Do nothing | 0 | `[2, 8, 7, 1, 3, 5, 6, 4]` |
| 2 | 7 | No | Do nothing | 0 | `[2, 8, 7, 1, 3, 5, 6, 4]` |
| 3 | 1 | Yes | $i \leftarrow 1$, swap $arr[1]$ with $arr[3]$ | 1 | `[2, 1, 7, 8, 3, 5, 6, 4]` |
| 4 | 3 | Yes | $i \leftarrow 2$, swap $arr[2]$ with $arr[4]$ | 2 | `[2, 1, 3, 8, 7, 5, 6, 4]` |
| 5 | 5 | No | Do nothing | 2 | `[2, 1, 3, 8, 7, 5, 6, 4]` |
| 6 | 6 | No | Do nothing | 2 | `[2, 1, 3, 8, 7, 5, 6, 4]` |
| **End** | - | - | Swap $arr[i+1]$ with $arr[high]$ ($arr[3] \leftrightarrow arr[7]$) | 3 | `[2, 1, 3, 4, 7, 5, 6, 8]` |

Pivot $4$ is now fixed at index $3$. Subproblems are `arr[0..2]` ($[2, 1, 3]$) and `arr[4..7]` ($[7, 5, 6, 8]$).

You can see this logged visually with:
```bash
python lomuto_partition.py
```

### 2.3 The Fatal Flaw of Lomuto: Duplicate Elements
Look closely at line 6 of Lomuto:
```python
if arr[j] <= pivot:
```
{: .note }
> **The All-Identical Trap**: If all elements in the array are identical (e.g., `[5, 5, 5, 5, 5]`), `arr[j] <= pivot` is **always True**!
> $i$ increments on every single step, and the pivot is swapped into `arr[high]` at the end. The subproblem sizes become $N-1$ and $0$.
### 2.4 Lomuto vs. Hoare Partition Scheme

In addition to Lomuto's scheme, C.A.R. Hoare's original two-pointer partition algorithm is widely used in production libraries:
- **Two Inward Pointers**: Pointer $i$ starts at $low - 1$ moving right, while $j$ starts at $high + 1$ moving left. When $arr[i] \ge pivot$ and $arr[j] \le pivot$, they swap.
- **Fewer Swaps**: Hoare's scheme performs roughly **3 times fewer swaps** on average than Lomuto ($\sim n/6$ swaps vs $\sim n/2$ swaps).
- **Duplicate Key Resilience**: Because Hoare stops pointers on elements *equal* to the pivot and swaps them, duplicate elements are divided evenly between left and right partitions. This avoids Lomuto's $O(N^2)$ degradation on arrays with identical elements!

Run the comparison demo directly:
```bash
python lomuto_partition.py
```

---

## Part 3: Quicksort Benchmarks (1,000,000 Elements & Edge Cases)

We provide [`lab2/benchmark_partition.py`](benchmark_partition.py) outright. It tests:
- **1,000,000 Randomized Elements**: Evaluates sorting speed across pivot strategies.
- **Pivot Selection Strategies**:
  1. `Last Element`: standard Lomuto ($arr[high]$).
  2. `Random Pivot`: randomly selects an element and swaps with $arr[high]$.
  3. `Median-of-Three`: takes median of $\{arr[low], arr[mid], arr[high]\}$.
- **Edge Cases**:
  - Already Sorted Array
  - Reverse-Sorted Array
  - All-Identical Elements
  - Few Unique Elements (heavy duplicates)
  - Nearly Sorted Array (1% perturbed)
- **Comparisons**:
  - Lomuto Quicksort
  - Hoare Quicksort (Two-Pointer)
  - 3-Way Quicksort (Dutch National Flag: $<, =, >$)
  - Python Built-in Sort (Timsort)

{: .note }
> ### The Math of Scale: Why $N = 10,000$ for Edge Cases instead of $1,000,000$?
> 
> Students often ask: *Why does the benchmark use $N = 1,000,000$ for random data, but scale down to $N = 10,000$ for edge cases?*
> - For randomized data, Quicksort runs in $O(N \log_2 N)$ time. At $N = 10^6$, $N \log_2 N \approx 2 \times 10^7$ operations, taking $\approx 0.1$ to $1$ second in Python.
> - For pathological inputs (e.g. sorted or identical data with standard Lomuto), Quicksort degrades to $O(N^2)$.
> - If we ran $N = 10^6$ on an $O(N^2)$ algorithm, it would require $(10^6)^2 = 10^{12}$ operations. At $2 \times 10^7$ ops/sec, that would take **over 13 hours** and freeze your computer!
> - By scaling edge cases to $N = 10,000$, $N^2 = 10^8$ operations, which finishes in $\approx 1.5$ seconds. You can observe the dramatic quadratic slowdown in real time without crashing!

### Running the Benchmark

In your terminal:
```bash
python benchmark_partition.py
```
*(For a quick test on smaller sizes, run `python benchmark_partition.py --quick`)*

{: .exercise }
> ### Exercise 2: Benchmark Observations & Analysis
> 
> Run `benchmark_partition.py` and record the results:
> 
> ```text
> TODO 2.1:
> Record your execution times for N = 1,000,000 random integers (or N = 100,000 with --quick):
> - Python Timsort:
> - Lomuto (Random Pivot):
> - Lomuto (Median-of-3):
> - Lomuto (Last Element):
> - Hoare (Two-Pointer):
> - 3-Way Quicksort:
> 
> TODO 2.2:
> In the edge case benchmarks:
> What happens to Lomuto with Last Pivot on an Already Sorted array? Why?
> How does Random Pivot or Median-of-3 fix this?
> A:
> 
> TODO 2.3:
> On the "All Identical Elements" scenario:
> Compare the runtime of Lomuto Quicksort vs. Hoare Quicksort vs. 3-Way Quicksort.
> Explain why Hoare and 3-Way Quicksort avoid Lomuto's quadratic explosion on identical data.
> A:
> 
> TODO 2.4:
> Why does standard recursive Quicksort risk crashing with `RecursionError` in Python
> when sorting large unbalanced arrays, and how does tail-recursion elimination
> or small-side recursion prevent this?
> A:
> ```

---

## Part 4: Representing Binary Trees via Arrays

While binary trees are often introduced using pointer-based nodes (`Node.left`, `Node.right`), **complete binary trees** can be stored compactly in a flat array (Python list) with **zero pointer overhead** and optimal cache locality.

```text
                  Level 0:          [50]                     (index 0)
                                 /        \
                  Level 1:     [30]      [20]                (indices 1, 2)
                              /    \     /   \
                  Level 2:  [15]  [10] [8]  [16]             (indices 3, 4, 5, 6)
```

Flat Array Representation: `[50, 30, 20, 15, 10, 8, 16]`

### 4.1 Index Arithmetic

| Navigation | 0-Based Indexing (Root at index 0) | 1-Based Indexing (Root at index 1) |
|---|---|---|
| **Root Index** | `0` | `1` (`arr[0]` unused) |
| **Left Child of $i$** | `2 * i + 1` | `2 * i` |
| **Right Child of $i$** | `2 * i + 2` | `2 * i + 1` |
| **Parent of $i$** | `(i - 1) // 2` (for $i > 0$) | `i // 2` (for $i > 1$) |

### 4.2 Traversals on Array-Backed Trees
Even without pointers, classic tree traversals can be executed using array index calculations:
- **Pre-Order** ($Root \to Left \to Right$):
  `preorder(i) = [arr[i]] + preorder(2*i + 1) + preorder(2*i + 2)`
- **In-Order** ($Left \to Root \to Right$):
  `inorder(i) = inorder(2*i + 1) + [arr[i]] + inorder(2*i + 2)`
- **Post-Order** ($Left \to Right \to Root$):
  `postorder(i) = postorder(2*i + 1) + postorder(2*i + 2) + [arr[i]]`
- **Level-Order**:
  Simply read the array sequentially from left to right: `arr[0], arr[1], arr[2], ...`!

### 4.3 Why Arrays for Heaps? Why Not for All Binary Trees?
- **Binary Heaps**: A binary heap is always a **complete binary tree** (all levels filled, last level filled from left to right). Because there are no missing nodes, every array slot from $0$ to $n-1$ is utilized. No pointers needed, $O(1)$ child lookups, and minimal memory footprint!
- **Sparse / Skewed Trees**: If a binary tree is skewed (like a degenerate linked list), a tree of height $h$ requires up to $2^{h+1} - 1$ array slots, almost all of which will be `None`.

```text
Skewed Tree Example (Height h = 3, only 4 nodes):

  [10] (index 0)
     \
     [20] (index 2)
        \
        [30] (index 6)
           \
           [40] (index 14)

Flat Array:
[10, None, 20, None, None, None, 30, None, None, None, None, None, None, None, 40]
Array size needed: 2^(h+1) - 1 = 15 slots for just 4 nodes (73% wasted empty space!).
```
For sparse trees, linked pointer representations (`Node.left`, `Node.right`) are far more memory-efficient.

Explore the reference implementation and visualizer in [`lab2/array_tree.py`](array_tree.py):
```bash
python array_tree.py
```

{: .exercise }
> ### Exercise 3: Array Tree Practice Code
> 
> Open [`lab2/array_tree_practice.py`](array_tree_practice.py) and complete the TODOs:
> 1. **Exercise 1 (0-Based)**: Implement `left_child_0`, `right_child_0`, `parent_0`.
> 2. **Exercise 2 (1-Based)**: Implement `left_child_1`, `right_child_1`, `parent_1`.
> 3. **Exercise 3 (Boundary Checks)**: Implement `has_left_0`, `has_right_0`, and `is_leaf_0`.
> 4. **Exercise 4 (Heap Validator)**: Implement `is_valid_max_heap(arr)`.
> 5. **Exercise 5 (Traversals)**: Implement `inorder_from_array(arr, index)`.
> 6. **Exercise 6 (Optional Challenge)**: Implement `max_heapify_down(arr, i, n)` (sift-down operation).
> 
> Verify your code by running:
> ```bash
> python array_tree_practice.py
> ```
> All required tests should output `[PASS]`.

---

## Lab Files Summary

All files for this lab are located in the `lab2/` directory:
- [`sorting_trace.py`](sorting_trace.py): Step-by-step visual trace utility for Bubble and Insertion Sort with comparison/swap metrics.
- [`lomuto_partition.py`](lomuto_partition.py): Traceable Lomuto and Hoare partitioning with pointer step logs, pivot strategies, and duplicate handling demo.
- [`benchmark_partition.py`](benchmark_partition.py): Full benchmark suite for 1,000,000 randomized integers, pivot strategies, edge cases, and copy-paste Markdown table generation.
- [`array_tree.py`](array_tree.py): `ArrayBinaryTree` class, 0-based/1-based indexing, traversals, and ASCII visualizer.
- [`array_tree_practice.py`](array_tree_practice.py): Student practice exercises (index math, bounds safety, heap validation, in-order traversal, and sift-down challenge) with automated test suite.

