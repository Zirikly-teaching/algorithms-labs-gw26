"""Part 2: implement Lomuto partition. The Quicksort wrapper is provided."""


def lomuto_partition(arr, low, high):
  """Partition inclusive range [low, high] in place; return pivot index.

  Preconditions: 0 <= low <= high < len(arr).
  Choose arr[high] as pivot. Values to its left must be <= pivot;
  values to its right must be > pivot. Preserve values outside the range.
  """
  # TODO 2.2: Translate the README's Lomuto pseudocode.
  pivot = arr[high]
  i = low - 1
  for j in range(low, high):
    if arr[j] <= pivot:
      i = i + 1
      placeholder = arr[i]
      arr[i] = arr[j]
      arr[j] = placeholder
  place = arr[i + 1]
  arr[i + 1] = arr[high]
  arr[high] = place 
  return i + 1


def quick_sort(arr, low=0, high=None):
  """Provided: sort in place and return arr. Intended for small lab inputs."""
  if high is None:
    high = len(arr) - 1
  if low < high:
    p = lomuto_partition(arr, low, high)
    quick_sort(arr, low, p - 1)
    quick_sort(arr, p + 1, high)
  return arr


if __name__ == "__main__":
  from lab_checks import check_quicksort
  raise SystemExit(check_quicksort(lomuto_partition, quick_sort))
