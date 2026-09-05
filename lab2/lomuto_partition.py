"""
Lab 2: Lomuto Partition Scheme and Quicksort
CSCI 3212 - Algorithms

This script explains, visualizes, and traces the Lomuto partition algorithm,
which is the most common partitioning scheme taught in introductory algorithms
(and the one featured in CLRS).

Lomuto Partition Logic:
----------------------
Given an array slice arr[low .. high]:
1. Choose a pivot element (traditionally arr[high]).
2. Maintain two pointers:
   - j: Current scanner, exploring elements from low to high - 1.
   - i: Boundary index for elements <= pivot (initialized to low - 1).
3. Loop Invariant:
   - arr[low .. i]     <= pivot
   - arr[i+1 .. j-1]   >  pivot
   - arr[j .. high-1]  not yet inspected
   - arr[high]         == pivot
4. When arr[j] <= pivot:
   - Advance i (i += 1)
   - Swap arr[i] with arr[j] (putting the smaller element into the <= pivot partition)
5. Finally, swap arr[i + 1] with arr[high] to place the pivot between the two partitions.
6. Return i + 1 as the pivot's finalized index.
"""

import random
from typing import List, Tuple


def select_pivot(arr: List[int], low: int, high: int, strategy: str = "last") -> int:
    """
    Selects a pivot index in arr[low..high] according to strategy,
    and swaps it to arr[high] so that standard Lomuto logic can proceed.
    """
    if strategy == "last":
        return high
    elif strategy == "first":
        arr[low], arr[high] = arr[high], arr[low]
        return high
    elif strategy == "random":
        rand_idx = random.randint(low, high)
        arr[rand_idx], arr[high] = arr[high], arr[rand_idx]
        return high
    elif strategy == "median3":
        mid = (low + high) // 2
        # Sort low, mid, high to find median
        triplet = [(arr[low], low), (arr[mid], mid), (arr[high], high)]
        triplet.sort(key=lambda x: x[0])
        med_idx = triplet[1][1]
        arr[med_idx], arr[high] = arr[high], arr[med_idx]
        return high
    else:
        raise ValueError(f"Unknown pivot strategy: {strategy}")


def lomuto_partition(arr: List[int], low: int, high: int, verbose: bool = False) -> int:
    """
    Executes Lomuto's partition scheme on arr[low .. high].
    Uses arr[high] as the pivot.
    
    Returns the final index of the pivot element.
    """
    pivot = arr[high]
    i = low - 1

    if verbose:
        print(f"\n--- Lomuto Partition on arr[{low}..{high}] with Pivot = {pivot} (at index {high}) ---")
        print(f"Initial: {arr}")
        print(f"Pointers: i = {i} (before start), pivot = {pivot} at index {high}")

    for j in range(low, high):
        curr_val = arr[j]
        if verbose:
            print(f"\nStep j = {j}: Examining arr[{j}] = {curr_val} vs Pivot = {pivot}")
        
        if curr_val <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            if verbose:
                print(f"  {curr_val} <= {pivot}: Increment i to {i}, SWAP arr[{i}] and arr[{j}]")
                print(f"  Array now: {arr}")
                print(f"    Region <= pivot: indices [{low}..{i}] -> {arr[low:i+1]}")
                print(f"    Region >  pivot: indices [{i+1}..{j}] -> {arr[i+1:j+1]}")
        else:
            if verbose:
                print(f"  {curr_val} > {pivot}: Do nothing with i (i remains {i})")
                print(f"  Array now: {arr}")
                print(f"    Region <= pivot: indices [{low}..{i}] -> {arr[low:i+1]}")
                print(f"    Region >  pivot: indices [{i+1}..{j}] -> {arr[i+1:j+1]}")

    # Final step: place pivot into its correct spot at i + 1
    pivot_pos = i + 1
    arr[pivot_pos], arr[high] = arr[high], arr[pivot_pos]

    if verbose:
        print(f"\nFinal Swap: Place pivot from index {high} to index {pivot_pos}")
        print(f"Partitioned Array: {arr}")
        print(f"  Left part  (<= {pivot}): {arr[low:pivot_pos]}")
        print(f"  Pivot spot ({pivot}):        index {pivot_pos}")
        print(f"  Right part (>  {pivot}): {arr[pivot_pos+1:high+1]}")
        print(f"{'='*60}")

    return pivot_pos


def hoare_partition(arr: List[int], low: int, high: int, verbose: bool = False) -> int:
    """
    Executes Hoare's original two-pointer partition scheme on arr[low .. high].
    Uses arr[low] as the pivot (or middle element).
    
    Pointers i and j start outside the boundaries and move inward:
    - i moves right until arr[i] >= pivot
    - j moves left until arr[j] <= pivot
    - If i < j, swap arr[i] and arr[j]
    - When i >= j, return j (subproblems are arr[low..j] and arr[j+1..high]).
    
    Key Advantages over Lomuto:
    1. Does roughly 3x fewer swaps on average (~n/6 swaps vs ~n/2 swaps).
    2. Naturally splits identical elements into roughly equal halves, avoiding
       Lomuto's O(n^2) identical-element trap!
    """
    pivot = arr[low]
    i = low - 1
    j = high + 1
    swaps = 0

    if verbose:
        print(f"\n--- Hoare Partition on arr[{low}..{high}] with Pivot = {pivot} ---")
        print(f"Initial: {arr}")

    while True:
        i += 1
        while arr[i] < pivot:
            i += 1

        j -= 1
        while arr[j] > pivot:
            j -= 1

        if i >= j:
            if verbose:
                print(f"Pointers crossed: i={i}, j={j}. Partition index j={j}. Total swaps={swaps}")
                print(f"  Left part  (arr[{low}..{j}]):  {arr[low:j+1]}")
                print(f"  Right part (arr[{j+1}..{high}]): {arr[j+1:high+1]}")
                print(f"{'='*60}")
            return j

        arr[i], arr[j] = arr[j], arr[i]
        swaps += 1
        if verbose:
            print(f"  [SWAP #{swaps}] arr[{i}]={arr[i]} and arr[{j}]={arr[j]} -> {arr}")


def quicksort_hoare(arr: List[int], low: int = 0, high: int = None) -> None:
    """Standard recursive Quicksort using Hoare's partition."""
    if high is None:
        high = len(arr) - 1
    if low < high:
        p = hoare_partition(arr, low, high)
        quicksort_hoare(arr, low, p)
        quicksort_hoare(arr, p + 1, high)


def quicksort_lomuto(arr: List[int], low: int = 0, high: int = None, strategy: str = "last") -> None:
    """
    Standard recursive Quicksort using Lomuto's partition.
    Sorts arr in-place.
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        select_pivot(arr, low, high, strategy=strategy)
        p = lomuto_partition(arr, low, high, verbose=False)
        quicksort_lomuto(arr, low, p - 1, strategy=strategy)
        quicksort_lomuto(arr, p + 1, high, strategy=strategy)


def demonstrate_lomuto_trace():
    print("=" * 65)
    print("DEMO 1: Standard Lomuto Partition Trace on CLRS Example")
    print("=" * 65)
    example1 = [2, 8, 7, 1, 3, 5, 6, 4]
    print(f"Array: {example1}")
    p = lomuto_partition(example1, 0, len(example1) - 1, verbose=True)
    print(f"Resulting pivot index: {p}, pivot value: {example1[p]}\n")

    print("=" * 65)
    print("DEMO 2: Lomuto Edge Case — All Identical Elements")
    print("=" * 65)
    example2 = [5, 5, 5, 5, 5]
    print(f"Array: {example2}")
    print("Notice what happens because the comparison is '<=':")
    p2 = lomuto_partition(example2, 0, len(example2) - 1, verbose=True)
    print(f"Resulting pivot index: {p2}")
    print("CRITICAL FINDING: When all elements are identical, Lomuto puts EVERY")
    print("element into the '<= pivot' partition! The pivot ends up at the very end (high),")
    print("producing partition sizes of (N-1) and 0. This causes O(N^2) worst-case time!\n")

    print("=" * 65)
    print("DEMO 3: Hoare Partition on All Identical Elements (Fixing Lomuto's Flaw)")
    print("=" * 65)
    example3 = [5, 5, 5, 5, 5]
    print(f"Array: {example3}")
    p3 = hoare_partition(example3, 0, len(example3) - 1, verbose=True)
    print(f"Resulting split index: {p3}")
    print("NOTICE: Hoare partition split the identical array into sizes 3 and 2!")
    print("This guarantees O(N log N) time on identical elements without special casing.")


if __name__ == "__main__":
    demonstrate_lomuto_trace()

