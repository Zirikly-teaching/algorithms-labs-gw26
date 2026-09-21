---
layout: default
title: Lab 2
nav_order: 3
---

# CSCI 3212 Lab 2: Sorting Logic and Implementation

In this lab, you will trace Bubble Sort and Insertion Sort, implement Lomuto
partitioning, practice the merge step of Merge Sort, and use an array-based
min-heap to implement Heapsort.

Bubble Sort and Insertion Sort are **trace exercises only**. Their code is
provided below; you do not need to implement either algorithm. This lab uses
Lomuto partitioning only.

## Files and deliverables

| File | Your work |
|---|---|
| `README.md` | Complete the trace tables and written responses in your lab notes or a copy of this file |
| `quicksort_practice.py` | Implement `lomuto_partition`; Quicksort is provided |
| `mergesort_practice.py` | Implement `merge`; recursive Merge Sort is provided |
| `heapsort_practice.py` | Implement `min_heapify_down` and complete `heap_sort`; heap construction is provided |
| `lab_checks.py` | Provided checks; do not edit |

- [ ] Part 1: Bubble Sort and Insertion Sort traces and short answers.
- [ ] Part 2: Lomuto trace, partition implementation, and short answers.
- [ ] Part 3: Merge Sort trace, merge implementation, and short answer.
- [ ] Part 4: Heap representation, sift-down trace, and Heapsort implementation.
- [ ] Run all three practice files and resolve all failed checks.

Keep the function names and parameters unchanged. Do not use `sorted`,
`list.sort`, or `heapq` to implement the required functions. The provided checks
use `sorted` only to verify results.

## Part 1: Bubble Sort and Insertion Sort

Count only **comparisons between element values**. Do not count loop bounds or
index checks such as `j >= 0`. Count a failed element comparison when it is
actually evaluated. Count each adjacent exchange as one swap and each move of
an existing element one position right as one shift. Placing the saved key is
not a shift.

### 1.1 Bubble Sort: trace only

Each pass compares neighboring elements. If they are out of order, it swaps
them. After each completed pass, the largest remaining unsorted element is in
its final position. After `k` passes, the last `k` positions form a sorted suffix.
If a pass makes no swaps, the entire array is sorted and the algorithm stops.

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

Trace `[5, 2, 9, 1, 5, 6]`. Pass 1 is provided:

| Comparison | Action | Array afterward |
|---|---|---|
| `5 > 2` | Swap | `[2, 5, 9, 1, 5, 6]` |
| `5 > 9` | Keep | `[2, 5, 9, 1, 5, 6]` |
| `9 > 1` | Swap | `[2, 5, 1, 9, 5, 6]` |
| `9 > 5` | Swap | `[2, 5, 1, 5, 9, 6]` |
| `9 > 6` | Swap | `[2, 5, 1, 5, 6, 9]` |

**TODO 1.1:** Complete the remaining comparisons. Record the values compared,
not just their indices. The array state is the state after that comparison.

| Pass | `j` | Values compared | Swap or keep? | Array afterward |
|---|---|---|---|---|
| 2 | 0 | TODO | TODO | TODO |
| 2 | 1 | TODO | TODO | TODO |
| 2 | 2 | TODO | TODO | TODO |
| 2 | 3 | TODO | TODO | TODO |
| 3 | 0 | TODO | TODO | TODO |
| 3 | 1 | TODO | TODO | TODO |
| 3 | 2 | TODO | TODO | TODO |
| 4 | 0 | TODO | TODO | TODO |
| 4 | 1 | TODO | TODO | TODO |

Record the sorted suffix guaranteed after each pass, the total comparisons,
and the total swaps. Why does the algorithm stop after Pass 4 even though the
outer loop permits more passes?

### 1.2 Insertion Sort: trace only

At the start of iteration `i`, positions `0` through `i - 1` are sorted.
Save `arr[i]` as `key`, shift larger elements right, and place `key` into the
gap. Saving `key` matters because shifting can overwrite its original slot.

```python
def insertion_sort(arr):
  for i in range(1, len(arr)):
    key = arr[i]
    j = i - 1
    while j >= 0 and arr[j] > key:
      arr[j + 1] = arr[j]
      j -= 1
    arr[j + 1] = key
  return arr
```

**TODO 1.2:** Trace `[7, 3, 5, 8, 2]`. In the comparisons column, include any
failed element comparison that stops shifting. If `j` becomes `-1`, Python
stops at the index check, so no further element comparison occurs.

| `i` | Key | Element comparisons in order | Elements shifted | Insertion index | Array after insertion |
|---|---|---|---|---|---|
| 1 | 3 | `7 > 3` (true) | 7 | 0 | `[3, 7, 5, 8, 2]` |
| 2 | 5 | TODO | TODO | TODO | TODO |
| 3 | 8 | TODO | TODO | TODO | TODO |
| 4 | 2 | TODO | TODO | TODO | TODO |

Record the total comparisons and total shifts.

### 1.3 Short answers

A stable sort preserves the original relative order of equal-key items.
For example, if `5A` appears before `5B`, a stable sort keeps that order when
comparing only their numeric values.

**TODO 1.3A:** On an already sorted array, explain why the provided Bubble Sort
and Insertion Sort each take O(n) time. What happens to Bubble Sort's best-case
time if you remove its early-exit check?

**TODO 1.3B:** Why do the strict `>` comparisons preserve stability? If Bubble
Sort uses `>=` instead, does it still sort correctly? Is it still stable? Use
`[5A, 5B]` to explain.

## Part 2: Lomuto Partition and Quicksort

Quicksort partitions a range around a pivot, then recursively sorts the two
sides. **Partitioning alone does not sort either side.** Here, `low` and `high`
are inclusive indices, and the pivot is the last element, `arr[high]`.

During scanning, `i` is the last index of the region containing values less
than or equal to the pivot. `j` is the index currently being examined.
Initially, `i = low - 1` means that the first region is empty; do not read
`arr[i]` at that point.

At the beginning of a loop iteration:

| Indices (inclusive) | Meaning |
|---|---|
| `low` through `i` | Values <= pivot |
| `i + 1` through `j - 1` | Values > pivot |
| `j` through `high - 1` | Not yet examined |
| `high` | Pivot |

A region is empty when its starting index exceeds its ending index.

```text
LOMUTO-PARTITION(arr, low, high)
  pivot = arr[high]
  i = low - 1
  for j from low through high - 1
    if arr[j] <= pivot
      increment i
      swap arr[i] with arr[j]
  swap arr[i + 1] with arr[high]
  return i + 1
```

### 2.1 Trace partitioning

**TODO 2.1:** Use `[2, 8, 7, 1, 3, 5, 6, 4]`, `low = 0`, `high = 7`.
The pivot is 4. Each row records the state **after** processing `j`.
A swap with the same index is allowed and leaves the array unchanged.

| `j` | Value examined | <= 4? | Swap indices, or none | `i` afterward | Array afterward |
|---|---|---|---|---|---|
| Initial | N/A | N/A | None | -1 | `[2, 8, 7, 1, 3, 5, 6, 4]` |
| 0 | 2 | Yes | 0 and 0 | 0 | `[2, 8, 7, 1, 3, 5, 6, 4]` |
| 1 | TODO | TODO | TODO | TODO | TODO |
| 2 | TODO | TODO | TODO | TODO | TODO |
| 3 | TODO | TODO | TODO | TODO | TODO |
| 4 | TODO | TODO | TODO | TODO | TODO |
| 5 | TODO | TODO | TODO | TODO | TODO |
| 6 | TODO | TODO | TODO | TODO | TODO |
| Final pivot swap | N/A | N/A | TODO | N/A | TODO |

Record the returned pivot index and the left and right subarrays.

### 2.2 Implement partitioning

**TODO 2.2:** Complete `lomuto_partition` in `quicksort_practice.py`.
Modify the supplied list in place, touch only positions `low` through `high`,
and return the pivot's final index. Use the supplied pseudocode.

The provided `quick_sort` calls your function, then sorts `low` through `p - 1`
and `p + 1` through `high`. The pivot is excluded because it is already placed.

```bash
python3 quicksort_practice.py
```

### 2.3 Short answers

**TODO 2.3A:** Why is the pivot excluded from the scanning loop? Why do we need
the final swap?

**TODO 2.3B:** For `[5, 5, 5, 5, 5]`, find the final `i`, returned pivot index,
and sizes of the two recursive subproblems. Explain why repeating this split
leads to O(n²) Quicksort time. What split occurs on ascending, distinct values
when the last element is always chosen as pivot?

## Part 3: Merge Sort

Merge Sort splits a list into two smaller lists, recursively sorts them, and
merges the sorted results. A list with zero or one element is already sorted.
The split makes the problems smaller; the merge step puts values in order.

```text
MERGE-SORT(arr)
  if length(arr) <= 1
    return a copy of arr
  mid = length(arr) // 2
  left = MERGE-SORT(elements before mid)
  right = MERGE-SORT(elements from mid onward)
  return MERGE(left, right)

MERGE(left, right)
  create an empty result list
  i = 0, j = 0
  while i < length(left) and j < length(right)
    if left[i] <= right[j]
      append left[i] to result; increment i
    otherwise
      append right[j] to result; increment j
  append all remaining elements of left, starting at i
  append all remaining elements of right, starting at j
  return result
```

### 3.1 Trace splitting and merging

**TODO 3.1A:** Start with `[7, 2, 6, 3]`. Write the two halves, the single-element
lists, the two sorted pairs, and the final sorted list.

Worked merge example: merging `[2, 7]` and `[3, 6]` takes 2, then 3, then 6.
The right list is exhausted, so the remaining 7 is appended.

**TODO 3.1B:** Trace merging `[2, 5, 8]` and `[1, 5, 9]`. Choose from the left
list on equal values. `i` and `j` below are their values before the comparison.

| `i` | `j` | Values compared | Take from left or right? | Result so far |
|---|---|---|---|---|
| 0 | 0 | 2 and 1 | Right | `[1]` |
| TODO | TODO | TODO | TODO | TODO |
| TODO | TODO | TODO | TODO | TODO |
| TODO | TODO | TODO | TODO | TODO |
| TODO | TODO | TODO | TODO | TODO |

Which list has elements remaining, and what is appended after the loop?

### 3.2 Implement merging

**TODO 3.2:** Complete `merge` in `mergesort_practice.py`. Inputs are already
sorted. Return a new sorted list containing every input element, including
duplicates. Do not modify either input. Use indices to advance through the
lists, and take from the left when values are equal.

The recursive `merge_sort` function is provided. In Python, `arr[:mid]` creates
a list of elements before `mid`; `arr[mid:]` creates a list from `mid` to the
end. You do not need to rewrite this function.

```bash
python3 mergesort_practice.py
```

**TODO 3.2A:** Why must `merge` copy the remaining elements after one input is
exhausted? What goes wrong if the function returns immediately after its main
comparison loop?

For context, merging n total elements takes O(n) time. Merge Sort has O(log n)
splitting levels and O(n) merging work per level, giving O(n log n) time.
The provided list-based version uses O(n) peak auxiliary space.

## Part 4: Array-Based Heaps and Heapsort

A binary heap is a **complete binary tree**: every level except possibly the
last is full, and the last level fills from left to right. In a **min-heap**,
each parent is at most as large as its children. The root is therefore a
minimum, but the array itself need not be sorted.

Store the tree in level order in a list. This lab uses 0-based indices only.

| Relationship | Index |
|---|---|
| Root | `0` |
| Left child of `i` | `2 * i + 1` |
| Right child of `i` | `2 * i + 2` |
| Parent of `i`, for `i > 0` | `(i - 1) // 2` |

A child exists in the active heap only if its index is less than `heap_size`.
The root has no parent; do not apply the parent formula to it.

### 4.1 Read an array as a heap

For `[4, 10, 8, 30, 15, 20, 16]`, the levels are:

| Level | Indices | Values |
|---|---|---|
| 0 | 0 | 4 |
| 1 | 1, 2 | 10, 8 |
| 2 | 3, 4, 5, 6 | 30, 15, 20, 16 |

**TODO 4.1:** Find the child indices and values of index 1, the parent index and
value of index 6, and all leaf indices. Is this a min-heap? Explain using the
parent-child comparisons, not whether the list looks sorted.

### 4.2 Restore the heap with sift-down

Sift-down repairs a node that may be larger than one of its children.
**Its child subtrees must already be min-heaps.** Compare the current node
with its existing children. If a child is smaller, swap with the smaller child
and continue from that child's index. Stop when no swap is needed.

```text
MIN-HEAPIFY-DOWN(arr, i, heap_size)
  repeat
    smallest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < heap_size and arr[left] < arr[smallest]
      smallest = left
    if right < heap_size and arr[right] < arr[smallest]
      smallest = right
    if smallest == i
      stop
    swap arr[i] with arr[smallest]
    i = smallest
```

**TODO 4.2A:** Trace sift-down on `[25, 10, 8, 30, 15, 20, 16]`, starting at
`i = 0`, with `heap_size = 7`. Record each swap and resulting array. Explain
why the smaller child must be chosen, and why the process stops.

**TODO 4.2B:** Implement `min_heapify_down` in `heapsort_practice.py`. Modify the
list in place and return `None`. The suffix starting at `heap_size` is outside
the heap and must remain unchanged.

### 4.3 Build the heap and sort

Leaves are already one-node heaps. The last internal node has index
`len(arr) // 2 - 1`. The provided `build_min_heap` works backward from that node
to the root, using your sift-down function. That order ensures each node's
child subtrees are already heaps when it is processed.

Heapsort first builds a min-heap, then repeatedly moves the minimum into its
final position at the end of the active heap. **This version produces
descending order:** the smallest value goes into the last position, the next
smallest goes immediately before it, and so on.

```text
HEAP-SORT(arr)
  BUILD-MIN-HEAP(arr)
  for end from length(arr) - 1 down through 1
    swap arr[0] with arr[end]
    MIN-HEAPIFY-DOWN(arr, 0, end)
  return arr
```

After the swap, `end` is the new heap size: active indices are `0` through
`end - 1`. The sorted suffix begins at `end`. **The list length does not
shrink.** Do not remove elements from the list.

**TODO 4.3A:** Complete the loop body in `heap_sort`. It should sort the original
list in descending order and return that same list object.

```bash
python3 heapsort_practice.py
```

**TODO 4.3B:** Starting with the min-heap `[4, 10, 8, 30, 15, 20, 16]`, perform
one Heapsort extraction: swap the root with the last active element, reduce
the active heap size, and sift down. Record the full array, active heap size,
and sorted suffix afterward. Why must sift-down exclude that suffix?

Heap construction takes O(n) time. Each extraction uses at most O(log n)
sift-down work, so Heapsort takes O(n log n) time overall. The iterative
implementation here uses O(1) auxiliary space.

## Final check

Run all three practice files. Unfinished functions report `[TODO]`; incorrect
results report `[FAIL]`; completed checks report `[PASS]`. Each command exits
with a nonzero status while any check is unfinished or failing. These checks
are examples, so also review your code against the function contracts.

```bash
python3 quicksort_practice.py
python3 mergesort_practice.py
python3 heapsort_practice.py
```
