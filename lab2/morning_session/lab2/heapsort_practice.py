"""Part 4: implement sift-down and complete the Heapsort loop."""


def min_heapify_down(arr, i, heap_size):
  """Repair the heap at i in place and return None.

  Preconditions: 0 <= heap_size <= len(arr). For a nonempty heap,
  0 <= i < heap_size and i's child subtrees are already min-heaps.
  An empty heap with i = 0 is allowed and requires no action.
  Indices heap_size onward are outside the heap and must not change.
  """
  # TODO 4.2B: Follow the sift-down pseudocode. Check bounds before indexing.
  raise NotImplementedError("Complete min_heapify_down")


def build_min_heap(arr):
  """Provided: build a min-heap from the bottom up, in place."""
  for i in range(len(arr) // 2 - 1, -1, -1):
    min_heapify_down(arr, i, len(arr))


def heap_sort(arr):
  """Sort arr in descending order in place and return the same list."""
  build_min_heap(arr)
  for end in range(len(arr) - 1, 0, -1):
    # TODO 4.3A: Move the minimum to end and repair the smaller active heap.
    raise NotImplementedError("Complete the heap_sort loop")
  return arr


if __name__ == "__main__":
  from lab2.morning_session.lab2.lab_checks import check_heapsort
  raise SystemExit(check_heapsort(min_heapify_down, build_min_heap, heap_sort))