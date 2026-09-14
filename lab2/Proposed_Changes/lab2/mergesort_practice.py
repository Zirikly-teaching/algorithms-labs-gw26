"""Part 3: implement merge. Recursive Merge Sort is provided."""


def merge(left, right):
  """Return a new sorted list from two sorted lists without changing them.

  Preserve duplicates. On equal values, take from left first.
  Use indices; do not remove items from the input lists.
  """
  # TODO 3.2: Compare current elements, then copy any remaining elements.
  sort_list = []
  left_index = 0
  right_index = 0
  while left_index < len(left) and right_index < len(right):
    if left[left_index] <= right[right_index]:
      sort_list.append(left[left_index])
      left_index += 1
    else:
      sort_list.append(right[right_index])
      right_index += 1
  # add the left array if it's left over
  while left_index < len(left):
    sort_list.append(left[left_index])
    left_index += 1
  # add the right array if it's left over
  while right_index < len(right):
    sort_list.append(right[right_index])
    right_index += 1

  return sort_list


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
