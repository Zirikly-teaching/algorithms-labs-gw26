"""Part 3: implement merge. Recursive Merge Sort is provided."""


def merge(left, right):
  """Return a new sorted list from two sorted lists without changing them.

  Preserve duplicates. On equal values, take from left first.
  Use indices; do not remove items from the input lists.
  """
  # TODO 3.2: Compare current elements, then copy any remaining elements.
  raise NotImplementedError("Complete merge")


def merge_sort(arr):
  """Provided: return a sorted copy; leave the original list unchanged."""
  if len(arr) <= 1:
    return arr.copy()
  mid = len(arr) // 2
  left = merge_sort(arr[:mid])
  right = merge_sort(arr[mid:])
  return merge(left, right)


if __name__ == "__main__":
  from lab2.morning_session.lab2.lab_checks import check_mergesort
  raise SystemExit(check_mergesort(merge, merge_sort))
