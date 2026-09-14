"""INSTRUCTOR SOLUTION. Part 4: min-heap operations and Heapsort."""


def min_heapify_down(arr, i, heap_size):
  """Repair the min-heap at i in place; leave the suffix unchanged."""
  while True:
    smallest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < heap_size and arr[left] < arr[smallest]:
      smallest = left
    if right < heap_size and arr[right] < arr[smallest]:
      smallest = right

    if smallest == i:
      return

    arr[i], arr[smallest] = arr[smallest], arr[i]
    i = smallest


def build_min_heap(arr):
  """Build a min-heap from the bottom up, in place."""
  for i in range(len(arr) // 2 - 1, -1, -1):
    min_heapify_down(arr, i, len(arr))


def heap_sort(arr):
  """Sort arr in descending order in place and return the same list."""
  build_min_heap(arr)
  for end in range(len(arr) - 1, 0, -1):
    arr[0], arr[end] = arr[end], arr[0]
    min_heapify_down(arr, 0, end)
  return arr


if __name__ == "__main__":
  from lab_checks import check_heapsort
  raise SystemExit(check_heapsort(min_heapify_down, build_min_heap, heap_sort))