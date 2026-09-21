"""Part 1: implement Max-Heap sift-down and complete the ascending Heapsort loop."""


def max_heapify_down(arr, i, heap_size):
  """Repair the max-heap property at index i in place and return None.

  Preconditions: 0 <= heap_size <= len(arr). For a nonempty heap,
  0 <= i < heap_size and i's child subtrees are already max-heaps.
  Indices heap_size onward are outside the active heap and must not change.
  """
  # TODO 1.3A: Follow the max-heap sift-down pseudocode. Check bounds before indexing.
  while True:
    left = 2 * i + 1
    right = 2 * i + 2
    largest = i
    if left < heap_size and arr[left] > arr[largest]:
      largest = left
    if right < heap_size and arr[right] > arr[largest]:
      largest = right
    if largest != i:
      arr[i], arr[largest] = arr[largest], arr[i]
      i = largest
    else:
      break
  return None


def build_max_heap(arr):
  """Provided: build a max-heap from the bottom up, in place."""
  for i in range(len(arr) // 2 - 1, -1, -1):
    max_heapify_down(arr, i, len(arr))


def heap_sort(arr):
  """Sort arr in ascending order in place and return the same list object."""
  build_max_heap(arr)
  for end in range(len(arr) - 1, 0, -1):
    # TODO 1.3B: Swap root with end, then repair the reduced active heap of size end.
    arr[0], arr[end] = arr[end], arr[0]
    max_heapify_down(arr, 0, end)
  return arr


if __name__ == "__main__":
  from lab_checks import check_heap
  raise SystemExit(check_heap(max_heapify_down, build_max_heap, heap_sort))
