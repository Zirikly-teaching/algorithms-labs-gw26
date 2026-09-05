"""
Lab 2: Bubble Sort and Insertion Sort Trace and Logic
CSCI 3212 - Algorithms

This script demonstrates and traces the step-by-step logic of:
1. Bubble Sort (standard vs. optimized with early-stopping flag)
2. Insertion Sort (tracing sorted prefix and element shifting)
"""

from typing import List, Tuple


def bubble_sort_trace(arr: List[int], early_stopping: bool = True, verbose: bool = True) -> Tuple[List[int], int, int]:
    """
    Sorts a copy of arr using Bubble Sort, printing trace information if verbose=True.
    
    Returns:
        (sorted_list, total_comparisons, total_swaps)
    """
    a = list(arr)
    n = len(a)
    comparisons = 0
    swaps = 0
    
    if verbose:
        print(f"\n{'='*60}")
        print(f"BUBBLE SORT TRACE (early_stopping={early_stopping})")
        print(f"Initial Array: {a}")
        print(f"{'='*60}")

    for pass_num in range(1, n):
        swapped = False
        if verbose:
            print(f"\n--- Pass {pass_num} (scanning indices 0 to {n - pass_num}) ---")
        
        for j in range(0, n - pass_num):
            comparisons += 1
            comp_str = f"Compare a[{j}]={a[j]} and a[{j+1}]={a[j+1]}"
            
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
                if verbose:
                    print(f"  [SWAP] {comp_str:<32} -> {a}")
            else:
                if verbose:
                    print(f"  [KEEP] {comp_str:<32} -> {a}")
        
        if verbose:
            print(f"State after Pass {pass_num}: {a} (sorted suffix: {a[n - pass_num:]})")
        
        if early_stopping and not swapped:
            if verbose:
                print(f"--> Early exit at Pass {pass_num}: No swaps occurred; array is sorted!")
            break

    if verbose:
        print(f"\nFinal Sorted Array: {a}")
        print(f"Total Comparisons: {comparisons}")
        print(f"Total Swaps:       {swaps}")
        print(f"{'='*60}\n")

    return a, comparisons, swaps


def insertion_sort_trace(arr: List[int], verbose: bool = True) -> Tuple[List[int], int, int]:
    """
    Sorts a copy of arr using Insertion Sort, printing trace information if verbose=True.
    
    Returns:
        (sorted_list, total_comparisons, total_shifts)
    """
    a = list(arr)
    n = len(a)
    comparisons = 0
    shifts = 0

    if verbose:
        print(f"\n{'='*60}")
        print("INSERTION SORT TRACE")
        print(f"Initial Array: {a}")
        print(f"{'='*60}")

    for i in range(1, n):
        key = a[i]
        j = i - 1
        if verbose:
            print(f"\n--- Step {i}: Inserting key={key} (from index {i}) into sorted prefix {a[:i]} ---")
        
        # Shift elements of a[0..i-1] that are greater than key
        while j >= 0:
            comparisons += 1
            if a[j] > key:
                if verbose:
                    print(f"  a[{j}]={a[j]} > key={key}: shift a[{j}] to index {j+1}")
                a[j + 1] = a[j]
                shifts += 1
                j -= 1
            else:
                if verbose:
                    print(f"  a[{j}]={a[j]} <= key={key}: found insertion position at index {j+1}")
                break
        
        a[j + 1] = key
        if verbose:
            print(f"Placed key={key} at index {j+1} -> Current Array: {a} (sorted prefix: {a[:i+1]})")

    if verbose:
        print(f"\nFinal Sorted Array: {a}")
        print(f"Total Comparisons: {comparisons}")
        print(f"Total Shifts:      {shifts}")
        print(f"{'='*60}\n")

    return a, comparisons, shifts


def run_demonstration():
    examples = {
        "1. Random Array": [5, 2, 9, 1, 5, 6],
        "2. Best Case (Already Sorted)": [1, 2, 3, 4, 5],
        "3. Worst Case (Reverse Sorted)": [5, 4, 3, 2, 1],
    }

    print("===========================================================")
    print("CSCI 3212 Lab 2: Sorting Algorithm Traces")
    print("===========================================================")
    for name, sample in examples.items():
        print(f"\n{'#'*60}")
        print(f"DATASET: {name} -> {sample}")
        print(f"{'#'*60}")
        
        # Bubble Sort with and without early stopping
        b_res, b_comp, b_swap = bubble_sort_trace(sample, early_stopping=True, verbose=True)
        # Insertion Sort
        i_res, i_comp, i_shift = insertion_sort_trace(sample, verbose=True)

        print(f"Summary for {name}:")
        print(f"  Bubble Sort:    {b_comp} comparisons, {b_swap} swaps")
        print(f"  Insertion Sort: {i_comp} comparisons, {i_shift} shifts")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demonstration()
    else:
        print("Running demo traces. (Run with custom lists by editing this file or calling functions in Python REPL).")
        run_demonstration()
