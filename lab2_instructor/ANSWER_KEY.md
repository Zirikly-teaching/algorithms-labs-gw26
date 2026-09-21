# Lab 2: Instructor Answer Key

Distribute only the student package. This folder contains complete coding
solutions and answers to the required written exercises. The student files
require only four functions or loop bodies: Lomuto partition, merge, sift-down,
and the Heapsort extraction loop. Bubble and Insertion Sort require no coding.

Run the reference implementations from this folder:

```bash
python3 quicksort_solution.py
python3 mergesort_solution.py
python3 heapsort_solution.py
```

The same `lab_checks.py` is included in both packages. Reference code uses
2-space indentation and no third-party dependencies. The provided recursive
Quicksort is intentionally for small instructional inputs; it is not a robust
large-input benchmark implementation.

## Part 1

### 1.1 Bubble Sort

| Pass | j | Comparison | Action | Array afterward |
|---|---|---|---|---|
| 2 | 0 | 2 > 5: false | Keep | `[2, 5, 1, 5, 6, 9]` |
| 2 | 1 | 5 > 1: true | Swap | `[2, 1, 5, 5, 6, 9]` |
| 2 | 2 | 5 > 5: false | Keep | `[2, 1, 5, 5, 6, 9]` |
| 2 | 3 | 5 > 6: false | Keep | `[2, 1, 5, 5, 6, 9]` |
| 3 | 0 | 2 > 1: true | Swap | `[1, 2, 5, 5, 6, 9]` |
| 3 | 1 | 2 > 5: false | Keep | `[1, 2, 5, 5, 6, 9]` |
| 3 | 2 | 5 > 5: false | Keep | `[1, 2, 5, 5, 6, 9]` |
| 4 | 0 | 1 > 2: false | Keep | `[1, 2, 5, 5, 6, 9]` |
| 4 | 1 | 2 > 5: false | Keep | `[1, 2, 5, 5, 6, 9]` |

Guaranteed suffixes after passes 1 through 4: `[9]`, `[6, 9]`, `[5, 6, 9]`,
`[5, 5, 6, 9]`. Total comparisons: **14**. Total swaps: **6**.
Pass 4 makes no swaps, so the flag triggers the break. The array became sorted
at the first comparison of Pass 3, but the flag cannot certify that until a
whole pass completes without swaps.

### 1.2 Insertion Sort

| i | Key | Comparisons | Shifted elements | Insertion index | Array afterward |
|---|---|---|---|---|---|
| 1 | 3 | 7 > 3: true | 7 | 0 | `[3, 7, 5, 8, 2]` |
| 2 | 5 | 7 > 5: true; 3 > 5: false | 7 | 1 | `[3, 5, 7, 8, 2]` |
| 3 | 8 | 7 > 8: false | None | 3 | `[3, 5, 7, 8, 2]` |
| 4 | 2 | 8 > 2; 7 > 2; 5 > 2; 3 > 2: all true | 8, 7, 5, 3 | 0 | `[2, 3, 5, 7, 8]` |

Total element comparisons: **8**. Total shifts: **6**.

### 1.3 Short answers

A. On sorted input, Bubble Sort makes one pass with n - 1 comparisons and no
swaps, then exits. Insertion Sort makes one failed element comparison per key
and no shifts, also n - 1 comparisons. Both take O(n). Without the early exit,
this Bubble Sort runs all passes and makes n(n - 1)/2 comparisons, giving
Theta(n²) best-case time.

B. Strict comparisons do not move equal items past each other. Using `>=`
still sorts values, but can reverse equal items. `[5A, 5B]` becomes `[5B, 5A]`
on its first pass, so stability is lost.

Optional inversions, using 0-based indices: `(0, 1)`, `(0, 2)`, `(0, 4)`,
`(1, 4)`, `(2, 4)`, `(3, 4)`. Their count is 6, equal to the number of shifts.

## Part 2

### 2.1 Lomuto trace

| j | Examined | <= 4? | Swap | i afterward | Array afterward |
|---|---|---|---|---|---|
| 0 | 2 | Yes | 0, 0 | 0 | `[2, 8, 7, 1, 3, 5, 6, 4]` |
| 1 | 8 | No | None | 0 | `[2, 8, 7, 1, 3, 5, 6, 4]` |
| 2 | 7 | No | None | 0 | `[2, 8, 7, 1, 3, 5, 6, 4]` |
| 3 | 1 | Yes | 1, 3 | 1 | `[2, 1, 7, 8, 3, 5, 6, 4]` |
| 4 | 3 | Yes | 2, 4 | 2 | `[2, 1, 3, 8, 7, 5, 6, 4]` |
| 5 | 5 | No | None | 2 | `[2, 1, 3, 8, 7, 5, 6, 4]` |
| 6 | 6 | No | None | 2 | `[2, 1, 3, 8, 7, 5, 6, 4]` |
| Final | N/A | N/A | 3, 7 | N/A | `[2, 1, 3, 4, 7, 5, 6, 8]` |

Returned index: **3**. Pivot: **4**. Left: `[2, 1, 3]`. Right: `[7, 5, 6, 8]`.
Neither side needs to be sorted after partitioning.

### 2.2 Code

See `quicksort_solution.py`.

### 2.3 Short answers

A. The pivot is kept at `high` while the other values are classified. Including
it would incorrectly treat it as another scanned value in this algorithm and
invalidate the final placement logic. The final swap places it between the
<= region and the > region at index `i + 1`.

B. On five equal elements, the loop ends with `i = 3`, the pivot is placed at
index 4, and the recursive sizes are 4 and 0. Repeated sizes n - 1 and 0 mean
linear partition work on ranges n, n - 1, ..., 2. Their sum is Theta(n²).
Ascending distinct values with the last pivot give the same n - 1 and 0 split,
because that pivot is the largest value.

## Part 3

### 3.1 Traces

A. Split `[7, 2, 6, 3]` into `[7, 2]` and `[6, 3]`; then `[7]`, `[2]`, `[6]`,
and `[3]`. Merge into `[2, 7]` and `[3, 6]`, then `[2, 3, 6, 7]`.

| i | j | Compared | Take | Result |
|---|---|---|---|---|
| 0 | 0 | 2, 1 | Right | `[1]` |
| 0 | 1 | 2, 5 | Left | `[1, 2]` |
| 1 | 1 | 5, 5 | Left | `[1, 2, 5]` |
| 2 | 1 | 8, 5 | Right | `[1, 2, 5, 5]` |
| 2 | 2 | 8, 9 | Left | `[1, 2, 5, 5, 8]` |

The left list is exhausted. Append the remaining right value 9 to obtain
`[1, 2, 5, 5, 8, 9]`.

### 3.2 Code and explanation

See `mergesort_solution.py`. The main loop stops when either list is exhausted,
so the other list may still have unprocessed values. Returning immediately
would lose them. They are already sorted and can be appended in order.

## Part 4

### 4.1 Representation

Index 1 has children at 3 and 4, with values 15 and 10. Index 6 has parent index
2, with value 20. Leaves are at indices 3, 4, 5, 6. This is a max-heap:
50 >= 30 and 20; 30 >= 15 and 10; 20 >= 8 and 16.

### 4.2 Sift-down

Start `[4, 30, 20, 15, 10, 8, 16]`.
Swap indices 0 and 1: `[30, 4, 20, 15, 10, 8, 16]`.
Swap indices 1 and 3: `[30, 15, 20, 4, 10, 8, 16]`.
Stop at index 3 because it has no children in the active heap.

Choose the larger child so that the promoted value is >= both children at the
old parent position. Promoting the smaller child could leave a larger sibling
above which the heap property still fails. Continue downward because the
value moved down may still be too small for its new children.

See `heapsort_solution.py` for both coding tasks.

### 4.3 One extraction

Swap indices 0 and 6: `[16, 30, 20, 15, 10, 8, 50]`.
Set the active heap size to 6. Sift-down swaps indices 0 and 1:
`[30, 16, 20, 15, 10, 8, 50]`. At index 1, 16 >= 15 and 10, so stop.

Final array: `[30, 16, 20, 15, 10, 8, 50]`.
Active heap size: **6**. Sorted suffix: **[50]**.
The suffix contains values in their final sorted positions; including it in
sift-down could move them back into the heap.
