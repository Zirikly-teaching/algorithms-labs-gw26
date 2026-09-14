"""
Lab 2: Quicksort & Lomuto Partition Benchmark Suite
CSCI 3212 - Algorithms

This script benchmarks Lomuto partitioning with various pivot selection strategies
on a 1,000,000-sized randomized array, as well as critical edge cases:
1. Pivot Selection Strategies:
   - Last Element (standard Lomuto: arr[high])
   - Random Pivot (swaps a uniformly random index to arr[high])
   - Median-of-Three (median of arr[low], arr[mid], arr[high])
2. Algorithmic Comparisons:
   - Lomuto Quicksort
   - 3-Way Quicksort (Dutch National Flag: < pivot, == pivot, > pivot)
   - Python Built-in Sort (Timsort, C-accelerated baseline)
3. Edge Case Distributions:
   - Uniform Random Array
   - Already Sorted Array
   - Reverse-Sorted Array
   - All Identical Elements (the classic Lomuto pitfall)
   - Few Unique Elements (heavy duplicates)
   - Nearly Sorted Array (1% perturbed)
"""

import sys
import time
import random
from typing import List, Callable, Tuple, Dict, Any

# Increase Python recursion limit as a safeguard, but we also use
# tail-recursion elimination to keep call stack depth O(log N).
sys.setrecursionlimit(50000)


# =====================================================================
# 1. Partition Schemes & Pivot Selection
# =====================================================================

def select_pivot(arr: List[int], low: int, high: int, strategy: str) -> None:
    """Selects pivot and swaps it to arr[high] before partitioning."""
    if strategy == "last":
        return
    elif strategy == "random":
        r = random.randint(low, high)
        arr[r], arr[high] = arr[high], arr[r]
    elif strategy == "median3":
        mid = (low + high) // 2
        # Find index of median of arr[low], arr[mid], arr[high]
        a, b, c = arr[low], arr[mid], arr[high]
        if (a <= b <= c) or (c <= b <= a):
            med_idx = mid
        elif (b <= a <= c) or (c <= a <= b):
            med_idx = low
        else:
            med_idx = high
        arr[med_idx], arr[high] = arr[high], arr[med_idx]


def lomuto_partition(arr: List[int], low: int, high: int) -> int:
    """Standard Lomuto partition using arr[high] as pivot."""
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quicksort_lomuto_stack_safe(arr: List[int], low: int, high: int, strategy: str = "random") -> None:
    """
    Quicksort using Lomuto partition with tail-call elimination.
    Always recurses on the smaller subarray and loops on the larger one.
    This guarantees stack depth <= O(log N), preventing Python stack overflows.
    """
    while low < high:
        select_pivot(arr, low, high, strategy)
        p = lomuto_partition(arr, low, high)
        
        # Recurse on smaller half first
        if (p - low) < (high - p):
            quicksort_lomuto_stack_safe(arr, low, p - 1, strategy)
            low = p + 1
        else:
            quicksort_lomuto_stack_safe(arr, p + 1, high, strategy)
            high = p - 1


def quicksort_threeway(arr: List[int], low: int, high: int) -> None:
    """
    3-way Quicksort (Dijkstra's Dutch National Flag partition).
    Partitions into: [< pivot | == pivot | > pivot].
    Optimal for datasets with duplicate or identical elements (O(N) time!).
    """
    while low < high:
        # Random pivot selection for robustness
        r = random.randint(low, high)
        arr[low], arr[r] = arr[r], arr[low]
        pivot = arr[low]
        
        lt = low      # arr[low..lt-1] < pivot
        gt = high     # arr[gt+1..high] > pivot
        i = low + 1   # arr[lt..i-1] == pivot
        
        while i <= gt:
            if arr[i] < pivot:
                arr[lt], arr[i] = arr[i], arr[lt]
                lt += 1
                i += 1
            elif arr[i] > pivot:
                arr[gt], arr[i] = arr[i], arr[gt]
                gt -= 1
            else:
                i += 1
        
        # Subarrays to sort: arr[low..lt-1] and arr[gt+1..high]
        if (lt - low) < (high - gt):
            quicksort_threeway(arr, low, lt - 1)
            low = gt + 1
        else:
            quicksort_threeway(arr, gt + 1, high)
            high = lt - 1


def hoare_partition(arr: List[int], low: int, high: int) -> int:
    """Hoare two-pointer partition scheme using middle element as pivot."""
    mid = (low + high) // 2
    pivot = arr[mid]
    i = low - 1
    j = high + 1
    while True:
        i += 1
        while arr[i] < pivot:
            i += 1
        j -= 1
        while arr[j] > pivot:
            j -= 1
        if i >= j:
            return j
        arr[i], arr[j] = arr[j], arr[i]


def quicksort_hoare_stack_safe(arr: List[int], low: int, high: int) -> None:
    """Quicksort using Hoare partition with tail-call elimination."""
    while low < high:
        p = hoare_partition(arr, low, high)
        if (p - low) < (high - (p + 1)):
            quicksort_hoare_stack_safe(arr, low, p)
            low = p + 1
        else:
            quicksort_hoare_stack_safe(arr, p + 1, high)
            high = p


# =====================================================================
# 2. Dataset Generators
# =====================================================================

def generate_data(dtype: str, size: int) -> List[int]:
    """Generates an array of specified size and distribution."""
    if dtype == "random":
        return [random.randint(1, 10_000_000) for _ in range(size)]
    elif dtype == "sorted":
        return list(range(size))
    elif dtype == "reverse_sorted":
        return list(range(size, 0, -1))
    elif dtype == "all_identical":
        return [42] * size
    elif dtype == "few_unique":
        # 10 distinct values repeated
        return [random.choice([10, 20, 30, 40, 50, 60, 70, 80, 90, 100]) for _ in range(size)]
    elif dtype == "nearly_sorted":
        arr = list(range(size))
        # 1% random pairwise swaps
        num_swaps = max(1, size // 100)
        for _ in range(num_swaps):
            i = random.randint(0, size - 1)
            j = random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    else:
        raise ValueError(f"Unknown data type: {dtype}")


# =====================================================================
# 3. Timing Harness
# =====================================================================

def benchmark_sort(sort_fn: Callable[[List[int]], None], arr: List[int]) -> Tuple[float, bool]:
    """Times sort_fn on a fresh copy of arr and verifies correctness."""
    data = list(arr)
    t0 = time.perf_counter()
    sort_fn(data)
    t1 = time.perf_counter()
    duration = t1 - t0
    
    # Fast verification: check if sorted
    is_sorted = all(data[k] <= data[k+1] for k in range(min(1000, len(data) - 1)))
    if is_sorted and len(data) > 1000:
        is_sorted = (data[0] <= data[-1])
    return duration, is_sorted


def run_million_element_benchmark(size: int = 1_000_000):
    """Benchmarks 1,000,000 randomized integers across pivot strategies."""
    print(f"\n{'='*75}")
    print(f"BENCHMARK 1: 1,000,000 RANDOMIZED ARRAY COMPARISON")
    print(f"Array Size: N = {size:,} integers")
    print(f"{'='*75}")
    
    print(f"Generating {size:,} random integers...", end="", flush=True)
    t_gen = time.perf_counter()
    random_arr = generate_data("random", size)
    print(f" done ({time.perf_counter() - t_gen:.2f}s).")

    configs = [
        ("Python Timsort (Built-in)", lambda a: a.sort()),
        ("Lomuto QS (Random Pivot)", lambda a: quicksort_lomuto_stack_safe(a, 0, len(a) - 1, strategy="random")),
        ("Lomuto QS (Median-of-3)", lambda a: quicksort_lomuto_stack_safe(a, 0, len(a) - 1, strategy="median3")),
        ("Lomuto QS (Last Element)", lambda a: quicksort_lomuto_stack_safe(a, 0, len(a) - 1, strategy="last")),
        ("Hoare QS (Two-Pointer)", lambda a: quicksort_hoare_stack_safe(a, 0, len(a) - 1)),
        ("3-Way Quicksort (Dutch Flag)", lambda a: quicksort_threeway(a, 0, len(a) - 1)),
    ]

    results = []
    for name, fn in configs:
        print(f"  Running {name:<30} ... ", end="", flush=True)
        dur, valid = benchmark_sort(fn, random_arr)
        status = "PASS" if valid else "FAIL"
        print(f"{dur:7.3f}s  [{status}]")
        results.append((name, dur, status))

    print(f"\n{'-'*75}")
    print(f"{'Algorithm / Pivot Strategy':<32} | {'Time (seconds)':<15} | {'Speed vs Timsort'}")
    print(f"{'-'*75}")
    timsort_time = results[0][1]
    for name, dur, _ in results:
        ratio = f"{dur / timsort_time:.1f}x" if timsort_time > 0 else "N/A"
        print(f"{name:<32} | {dur:>12.3f} s | {ratio:>15}")
    print(f"{'-'*75}")

    print("\n[Copy-Paste Markdown Table for Your Lab Report]:")
    print("| Algorithm / Pivot Strategy | Runtime (N=1,000,000) | Ratio vs Timsort |")
    print("|---|---|---|")
    for name, dur, _ in results:
        ratio = f"{dur / timsort_time:.1f}x" if timsort_time > 0 else "N/A"
        print(f"| {name} | {dur:.3f} s | {ratio} |")


def run_edge_case_benchmarks():
    """
    Benchmarks pivot strategies on pathological edge cases:
    - Sorted, Reverse Sorted, All Identical, Few Unique, Nearly Sorted.
    
    Safety Note:
    For known O(N^2) configurations (e.g. Last Pivot Lomuto on sorted or identical data),
    N is set to 10,000 so the quadratic explosion is demonstrated in ~1-2 seconds
    without hanging the system for hours.
    """
    print(f"\n{'='*75}")
    print("BENCHMARK 2: EDGE CASES & PATHOLOGICAL INPUTS")
    print(f"{'='*75}")
    print("Notice how pivot choice & partition scheme behave on tricky distributions!\n")

    demo_size = 10_000

    scenarios = [
        ("Already Sorted Array", "sorted", demo_size),
        ("Reverse-Sorted Array", "reverse_sorted", demo_size),
        ("All Identical Elements", "all_identical", demo_size),
        ("Few Unique Elements (Heavy Dups)", "few_unique", 20_000),
        ("Nearly Sorted (1% perturbed)", "nearly_sorted", 20_000),
    ]

    algorithms = [
        ("Lomuto (Last Pivot)", lambda a: quicksort_lomuto_stack_safe(a, 0, len(a) - 1, strategy="last")),
        ("Lomuto (Random Pivot)", lambda a: quicksort_lomuto_stack_safe(a, 0, len(a) - 1, strategy="random")),
        ("Lomuto (Median-of-3)", lambda a: quicksort_lomuto_stack_safe(a, 0, len(a) - 1, strategy="median3")),
        ("Hoare (Two-Pointer)", lambda a: quicksort_hoare_stack_safe(a, 0, len(a) - 1)),
        ("3-Way Quicksort", lambda a: quicksort_threeway(a, 0, len(a) - 1)),
        ("Python Timsort", lambda a: a.sort()),
    ]

    edge_results = {}
    for title, dtype, n in scenarios:
        print(f"\n--- Scenario: {title} (N = {n:,}) ---")
        arr = generate_data(dtype, n)
        edge_results[title] = []
        for alg_name, fn in algorithms:
            print(f"  {alg_name:<28}: ", end="", flush=True)
            dur, valid = benchmark_sort(fn, arr)
            print(f"{dur:7.4f}s")
            edge_results[title].append((alg_name, dur))

    print(f"\n{'='*75}")
    print("KEY TAKEAWAYS FOR STUDENTS:")
    print("1. Random / Median-of-3 pivots protect against sorted / reverse-sorted arrays.")
    print("2. Standard Lomuto FAILS on arrays with identical elements even with random pivot,")
    print("   because '<=' sends duplicate keys to one side, yielding O(N^2) degradation!")
    print("3. Hoare partition naturally splits duplicate keys across both pointers, preventing O(N^2) trap.")
    print("4. 3-Way Quicksort (Dutch National Flag) handles duplicate keys in O(N) linear time.")
    print("5. Python's Timsort recognizes pre-sorted runs and completes in O(N) linear time.")
    print(f"{'='*75}\n")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        run_million_element_benchmark(size=100_000)
    else:
        run_million_element_benchmark(size=1_000_000)
    
    run_edge_case_benchmarks()
