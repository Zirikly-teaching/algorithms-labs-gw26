"""Part 3: implement merge. Recursive Merge Sort is provided."""


def merge(left, right):
  """Return a new sorted list from two sorted lists without changing them.

  Preserve duplicates. On equal values, take from left first.
  Use indices; do not remove items from the input lists.
  """
  # TODO 3.2: Compare current elements, then copy any remaining elements.
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
  from lab_checks import check_mergesort
  raise SystemExit(check_mergesort(merge, merge_sort))
