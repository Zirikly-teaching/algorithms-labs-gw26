"""Provided checks for Lab 2. No third-party packages required."""

from collections import Counter


def require(condition, message):
  if not condition:
    raise AssertionError(message)


def run_checks(cases):
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
      print(
        "[FAIL] " + name + ": "
        + type(error).__name__ + ": " + str(error)
      )

  print(str(len(cases) - failed) + "/" + str(len(cases)) + " checks passed")
  return 1 if failed else 0


SORT_CASES = [
  [],
  [4],
  [2, 1],
  [1, 2, 3, 4],
  [4, 3, 2, 1],
  [5, 5, 5, 5, 5],
  [3, -1, 3, 0, -8, 2],
  [2, 8, 7, 1, 3, 5, 6, 4]
]

def check_quicksort(partition, sort):
  def partition_case(values, low, high):
    arr = values.copy()
    pivot = values[high]
    p = partition(arr, low, high)

    require(
      type(p) is int and low <= p <= high,
      "Return a pivot index in range"
    )
    require(
      arr[p] == pivot,
      "Returned index must contain the original pivot"
    )
    require(
      all(arr[k] <= pivot for k in range(low, p)),
      "Left region exceeds pivot"
    )
    require(
      all(arr[k] > pivot for k in range(p + 1, high + 1)),
      "Right region must be > pivot"
    )
    require(
      Counter(arr[low:high + 1]) == Counter(values[low:high + 1]),
      "Partition lost or changed values"
    )
    require(
      arr[:low] == values[:low]
      and arr[high + 1:] == values[high + 1:],
      "Changed values outside the range"
    )

  def sorting_case(values):
    arr = values.copy()
    result = sort(arr)

    require(
      arr == sorted(values),
      "Quicksort result is incorrect"
    )
    require(
      result is arr,
      "Quicksort must return the original list"
    )

  def runtime_case():
    import random
    from statistics import median
    from time import perf_counter

    size = 900
    repetitions = 5
    ascending = list(range(size))
    rng = random.Random(3212)

    def random_pivot_quick_sort(arr, low=0, high=None):
      """Provided demonstration: Quicksort with random pivot selection."""
      if high is None:
        high = len(arr) - 1

      if low < high:
        # Move a randomly chosen pivot to the position Lomuto expects.
        pivot_index = rng.randint(low, high)
        arr[pivot_index], arr[high] = arr[high], arr[pivot_index]

        # Reuse the student's Lomuto partition function.
        p = partition(arr, low, high)

        random_pivot_quick_sort(arr, low, p - 1)
        random_pivot_quick_sort(arr, p + 1, high)

      return arr

    def measure(sort_function):
      # Both strategies receive a fresh copy of the same ascending input.
      arr = ascending.copy()

      start = perf_counter()
      result = sort_function(arr)
      elapsed = perf_counter() - start

      require(
        arr == ascending,
        "Incorrect result during the pivot comparison"
      )
      require(
        result is arr,
        "Quicksort must return the original list"
      )

      return elapsed

    last_pivot_times = []
    random_pivot_times = []

    for trial in range(repetitions):
      # Alternate measurement order to reduce ordering effects.
      if trial % 2 == 0:
        last_pivot_times.append(measure(sort))
        random_pivot_times.append(measure(random_pivot_quick_sort))
      else:
        random_pivot_times.append(measure(random_pivot_quick_sort))
        last_pivot_times.append(measure(sort))

    last_pivot_time = median(last_pivot_times)
    random_pivot_time = median(random_pivot_times)

    print("Pivot comparison: " + str(size) + " ascending elements")
    print("Both strategies sort the same values in the same starting order.")
    print("Reported times are medians of " + str(repetitions) + " runs.")

    print(
      "Last-element pivot: "
      + format(last_pivot_time * 1000, ".3f") + " ms"
    )
    print(
      "Random pivot: "
      + format(random_pivot_time * 1000, ".3f") + " ms"
    )
    print(
      "Speedup from random pivot (last / random): "
      + format(last_pivot_time / random_pivot_time, ".2f") + "x"
    )

    print(
      "A ratio above 1 means random pivot was faster; "
      "below 1 means it was slower.\n"
    )
    print(
      "On ascending input, the last-element pivot repeatedly produces "
      "subproblems of sizes n - 1 and 0."
    )
    print(
      "Random pivots usually divide the work more evenly, giving "
      "expected O(n log n) time instead of this O(n^2) case.\n"
    )

  cases = []

  for values, low, high in [
    ([2, 8, 7, 1, 3, 5, 6, 4], 0, 7),
    ([5, 5, 5, 5, 5], 0, 4),
    ([9], 0, 0),
    ([99, 6, 2, 5, 1, 88], 1, 4),
    ([4, 3, 2, 1], 0, 3)
  ]:
    cases.append((
      "Partition " + str(values) + " range " + str((low, high)),
      lambda v=values, l=low, h=high: partition_case(v, l, h)
    ))

  for values in SORT_CASES:
    cases.append((
      "Quicksort " + str(values),
      lambda v=values: sorting_case(v)
    ))

  cases.append((
    "Runtime comparison: shuffled versus ascending input",
    runtime_case
  ))

  return run_checks(cases)


class TaggedValue:
  """Equal numeric keys carry distinct labels so stability can be checked."""

  def __init__(self, key, label):
    self.key = key
    self.label = label

  def __le__(self, other):
    return self.key <= other.key

  def __lt__(self, other):
    return self.key < other.key


def check_mergesort(merge, sort):
  def merge_case(left, right):
    lcopy = left.copy()
    rcopy = right.copy()
    result = merge(left, right)

    require(
      result == sorted(lcopy + rcopy),
      "Merged values incorrect"
    )
    require(
      left == lcopy and right == rcopy,
      "Do not modify either input"
    )
    require(
      result is not left and result is not right,
      "Return a new list"
    )

  def sorting_case(values):
    arr = values.copy()
    result = sort(arr)

    require(
      result == sorted(values),
      "Merge Sort result is incorrect"
    )
    require(
      arr == values,
      "Merge Sort must preserve the input"
    )
    require(
      result is not arr,
      "Merge Sort must return a new list"
    )

  def stability_case():
    left = [
      TaggedValue(2, "A"),
      TaggedValue(2, "B")
    ]
    right = [
      TaggedValue(2, "C")
    ]
    result = merge(left, right)

    require(
      [item.label for item in result] == ["A", "B", "C"],
      "Take from left first on ties"
    )

  cases = []

  for left, right in [
    ([], []),
    ([], [1, 2]),
    ([1, 2], []),
    ([2, 5, 8], [1, 5, 9]),
    ([1, 2], [8, 9]),
    ([8, 9], [1, 2]),
    ([-4, 0, 3], [-2, 3])
  ]:
    cases.append((
      "Merge " + str(left) + " and " + str(right),
      lambda l=left, r=right: merge_case(l, r)
    ))

  cases.append((
    "Stable merge on equal keys",
    stability_case
  ))

  for values in SORT_CASES:
    cases.append((
      "Merge Sort " + str(values),
      lambda v=values: sorting_case(v)
    ))

  return run_checks(cases)


def check_heapsort(sift, build, sort):
  def is_heap(arr, size):
    return all(
      arr[(child - 1) // 2] <= arr[child]
      for child in range(1, size)
    )

  def sift_case(values, i, size):
    arr = values.copy()
    result = sift(arr, i, size)

    require(
      result is None,
      "Sift-down must return None"
    )
    require(
      is_heap(arr, size),
      "Active prefix is not a min-heap"
    )
    require(
      Counter(arr[:size]) == Counter(values[:size]),
      "Active heap values changed"
    )
    require(
      arr[size:] == values[size:],
      "Sorted suffix must remain unchanged"
    )

  def build_case(values):
    arr = values.copy()
    build(arr)

    require(
      is_heap(arr, len(arr)),
      "Build did not produce a min-heap"
    )
    require(
      Counter(arr) == Counter(values),
      "Build lost or changed values"
    )

  def sorting_case(values):
    arr = values.copy()
    result = sort(arr)

    require(
      arr == sorted(values, reverse=True),
      "Heapsort result must be in descending order"
    )
    require(
      result is arr,
      "Heapsort must return the original list"
    )

  cases = []

  for values, i, size in [
    ([], 0, 0),
    ([4], 0, 1),
    ([2, 1], 0, 2),
    ([25, 10, 8, 30, 15, 20, 16], 0, 7),
    ([9, 3, 1, 4], 0, 4),
    ([16, 10, 8, 30, 15, 20, 4], 0, 6),
    ([4, 25, 8, 30, 15, 20, 16], 1, 7)
  ]:
    cases.append((
      "Sift-down " + str(values) + " size " + str(size),
      lambda v=values, j=i, n=size: sift_case(v, j, n)
    ))

  for values in SORT_CASES:
    cases.append((
      "Build heap " + str(values),
      lambda v=values: build_case(v)
    ))
    cases.append((
      "Heapsort " + str(values),
      lambda v=values: sorting_case(v)
    ))

  return run_checks(cases)