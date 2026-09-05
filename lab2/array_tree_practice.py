"""
Lab 2 Practice: Array Representation of Binary Trees
CSCI 3212 - Algorithms

Instructions:
Complete the TODO functions below. Run this script to test your solutions:
    python array_tree_practice.py
"""

from typing import List, Optional, Any


# =====================================================================
# Exercise 1: 0-Based Index Calculations
# =====================================================================

def left_child_0(i: int) -> int:
    """
    Given index i of a node in a 0-indexed complete binary tree,
    return the index of its left child.
    """
    # TODO: Implement the 0-based left child index formula.
    raise NotImplementedError("TODO: Implement left_child_0")


def right_child_0(i: int) -> int:
    """
    Given index i of a node in a 0-indexed complete binary tree,
    return the index of its right child.
    """
    # TODO: Implement the 0-based right child index formula.
    raise NotImplementedError("TODO: Implement right_child_0")


def parent_0(i: int) -> Optional[int]:
    """
    Given index i of a node in a 0-indexed complete binary tree,
    return the index of its parent, or None if i is the root (i == 0).
    """
    # TODO: Implement the 0-based parent index formula.
    raise NotImplementedError("TODO: Implement parent_0")


# =====================================================================
# Exercise 2: 1-Based Index Calculations
# =====================================================================

def left_child_1(i: int) -> int:
    """
    Given index i of a node in a 1-indexed binary tree (root at index 1),
    return the index of its left child.
    """
    # TODO: Implement the 1-based left child index formula.
    raise NotImplementedError("TODO: Implement left_child_1")


def right_child_1(i: int) -> int:
    """
    Given index i of a node in a 1-indexed binary tree (root at index 1),
    return the index of its right child.
    """
    # TODO: Implement the 1-based right child index formula.
    raise NotImplementedError("TODO: Implement right_child_1")


def parent_1(i: int) -> Optional[int]:
    """
    Given index i of a node in a 1-indexed binary tree (root at index 1),
    return the index of its parent, or None if i is the root (i <= 1).
    """
    # TODO: Implement the 1-based parent index formula.
    raise NotImplementedError("TODO: Implement parent_1")


# =====================================================================
# Exercise 3: Boundary & Leaf Checking (0-Based)
# =====================================================================

def has_left_0(i: int, n: int) -> bool:
    """
    Returns True if node at index i has a left child in a complete tree of size n.
    """
    # TODO: Return whether the left child index is strictly less than n.
    raise NotImplementedError("TODO: Implement has_left_0")


def has_right_0(i: int, n: int) -> bool:
    """
    Returns True if node at index i has a right child in a complete tree of size n.
    """
    # TODO: Return whether the right child index is strictly less than n.
    raise NotImplementedError("TODO: Implement has_right_0")


def is_leaf_0(i: int, n: int) -> bool:
    """
    Returns True if node at index i is a leaf in a complete binary tree of size n.
    Hint: In a complete binary tree, if a node has no left child, can it have a right child?
    """
    # TODO: Determine if node i is a leaf.
    raise NotImplementedError("TODO: Implement is_leaf_0")


# =====================================================================
# Exercise 4: Max-Heap Property Validator
# =====================================================================

def is_valid_max_heap(arr: List[int]) -> bool:
    """
    Given a 0-indexed array of integers representing a complete binary tree,
    return True if the array satisfies the Max-Heap property, False otherwise.
    
    Max-Heap Property:
    For every index i > 0, arr[parent(i)] >= arr[i].
    Equivalently, every parent must be greater than or equal to both of its children.
    """
    # TODO: Iterate through the tree and verify the Max-Heap property.
    raise NotImplementedError("TODO: Implement is_valid_max_heap")


# =====================================================================
# Exercise 5: In-Order Traversal from an Array Tree
# =====================================================================

def inorder_from_array(arr: List[Any], index: int = 0) -> List[Any]:
    """
    Given a 0-indexed array representing a complete binary tree,
    return a list containing the elements in IN-ORDER traversal (Left -> Root -> Right).
    """
    # TODO: Recursively collect the elements in in-order.
    # Base case: if index is out of bounds or arr[index] is None, return []
    raise NotImplementedError("TODO: Implement inorder_from_array")


# =====================================================================
# Exercise 6 (Optional Challenge): Sift-Down (max_heapify)
# =====================================================================

def max_heapify_down(arr: List[int], i: int, n: int) -> None:
    """
    Maintains the max-heap property for subtree rooted at index i,
    assuming subtrees at left_child(i) and right_child(i) are already valid heaps.
    
    This is the fundamental operation used to build heaps in O(N) time (Lecture 5)
    and perform Heapsort in O(N log N) time (Lecture 6)!
    """
    # OPTIONAL CHALLENGE: Implement sift-down iteratively or recursively
    raise NotImplementedError("Optional Challenge: Implement max_heapify_down")


# =====================================================================
# Verification / Test Suite
# =====================================================================

def run_tests():
    print("Running tests for Lab 2 Array Tree Practice...\n")
    passed = 0
    total = 5

    # Test 1: 0-Based Formulas
    try:
        assert left_child_0(0) == 1, f"left_child_0(0) expected 1, got {left_child_0(0)}"
        assert right_child_0(0) == 2, f"right_child_0(0) expected 2, got {right_child_0(0)}"
        assert parent_0(0) is None, f"parent_0(0) expected None, got {parent_0(0)}"
        assert left_child_0(2) == 5, f"left_child_0(2) expected 5, got {left_child_0(2)}"
        assert right_child_0(2) == 6, f"right_child_0(2) expected 6, got {right_child_0(2)}"
        assert parent_0(5) == 2, f"parent_0(5) expected 2, got {parent_0(5)}"
        assert parent_0(6) == 2, f"parent_0(6) expected 2, got {parent_0(6)}"
        print("  [PASS] Exercise 1: 0-Based Index Formulas")
        passed += 1
    except NotImplementedError:
        print("  [TODO] Exercise 1: Not implemented yet")
    except AssertionError as e:
        print(f"  [FAIL] Exercise 1: {e}")

    # Test 2: 1-Based Formulas
    try:
        assert left_child_1(1) == 2, f"left_child_1(1) expected 2, got {left_child_1(1)}"
        assert right_child_1(1) == 3, f"right_child_1(1) expected 3, got {right_child_1(1)}"
        assert parent_1(1) is None, f"parent_1(1) expected None, got {parent_1(1)}"
        assert left_child_1(3) == 6, f"left_child_1(3) expected 6, got {left_child_1(3)}"
        assert right_child_1(3) == 7, f"right_child_1(3) expected 7, got {right_child_1(3)}"
        assert parent_1(6) == 3, f"parent_1(6) expected 3, got {parent_1(6)}"
        assert parent_1(7) == 3, f"parent_1(7) expected 3, got {parent_1(7)}"
        print("  [PASS] Exercise 2: 1-Based Index Formulas")
        passed += 1
    except NotImplementedError:
        print("  [TODO] Exercise 2: Not implemented yet")
    except AssertionError as e:
        print(f"  [FAIL] Exercise 2: {e}")

    # Test 3: Boundary & Leaf Helpers
    try:
        # Array of 7 nodes: indices 0..6
        n = 7
        assert has_left_0(0, n) is True
        assert has_right_0(0, n) is True
        assert is_leaf_0(0, n) is False
        assert has_left_0(2, n) is True   # left child is 5 < 7
        assert has_right_0(2, n) is True  # right child is 6 < 7
        assert is_leaf_0(2, n) is False
        assert has_left_0(3, n) is False  # left child is 7 >= 7
        assert is_leaf_0(3, n) is True
        assert is_leaf_0(6, n) is True
        print("  [PASS] Exercise 3: Boundary & Leaf Helpers")
        passed += 1
    except NotImplementedError:
        print("  [TODO] Exercise 3: Not implemented yet")
    except AssertionError as e:
        print(f"  [FAIL] Exercise 3: {e}")

    # Test 4: Max-Heap Validator
    try:
        assert is_valid_max_heap([]) is True, "Empty tree is vacuously a valid heap"
        assert is_valid_max_heap([42]) is True, "Single node is a valid heap"
        valid_heap = [90, 80, 70, 50, 60, 65, 40]
        invalid_left = [90, 50, 70, 80, 60, 65, 40]   # 80 is left child of 50 -> invalid!
        invalid_right = [90, 80, 70, 50, 60, 65, 95]  # 95 is right child of 70 -> invalid!
        assert is_valid_max_heap(valid_heap) is True, "valid_heap should return True"
        assert is_valid_max_heap(invalid_left) is False, "invalid_left should return False"
        assert is_valid_max_heap(invalid_right) is False, "invalid_right should return False"
        print("  [PASS] Exercise 4: Max-Heap Validator")
        passed += 1
    except NotImplementedError:
        print("  [TODO] Exercise 4: Not implemented yet")
    except AssertionError as e:
        print(f"  [FAIL] Exercise 4: {e}")

    # Test 5: In-Order Traversal
    try:
        # Binary Search Tree stored in level-order:
        #        4
        #      /   \
        #     2     6
        #    / \   / \
        #   1   3 5   7
        bst_arr = [4, 2, 6, 1, 3, 5, 7]
        expected_inorder = [1, 2, 3, 4, 5, 6, 7]
        actual = inorder_from_array(bst_arr, 0)
        assert actual == expected_inorder, f"Expected {expected_inorder}, got {actual}"
        print("  [PASS] Exercise 5: In-Order Traversal")
        passed += 1
    except NotImplementedError:
        print("  [TODO] Exercise 5: Not implemented yet")
    except AssertionError as e:
        print(f"  [FAIL] Exercise 5: {e}")

    # Test 6 (Optional Challenge): Sift-Down
    try:
        test_heap = [10, 80, 70, 50, 60, 65, 40]  # root 10 violates heap property
        max_heapify_down(test_heap, 0, len(test_heap))
        assert is_valid_max_heap(test_heap) is True, f"Result {test_heap} is not a valid max heap!"
        print("  [PASS] Exercise 6 (Optional Challenge): max_heapify_down")
    except NotImplementedError:
        print("  [OPTIONAL] Exercise 6: Optional challenge not attempted")
    except AssertionError as e:
        print(f"  [FAIL] Exercise 6: {e}")

    print(f"\nResult: {passed}/{total} required exercises completed successfully.")


if __name__ == "__main__":
    run_tests()
