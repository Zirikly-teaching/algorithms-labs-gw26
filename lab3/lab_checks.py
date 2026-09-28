"""Provided checks for Lab 3. No third-party packages required."""

from collections import Counter
import random
import sys


def require(condition, message):
  if not condition:
    raise AssertionError(message)


def run_checks(cases):
  """Run (name, zero-arg callable) pairs; return a process exit status.

  NotImplementedError -> [TODO]; any other exception -> [FAIL].
  """
  failed = 0

  for name, test in cases:
    try:
      test()
      print("[PASS] " + name)
    except NotImplementedError as error:
      failed += 1
      print("[TODO] " + name + ": " + str(error))
    except Exception as error:
      failed += 1
      print(
        "[FAIL] " + name + ": "
        + type(error).__name__ + ": " + str(error)
      )

  print(str(len(cases) - failed) + "/" + str(len(cases)) + " checks passed")
  return 1 if failed else 0


# Shared classes and tree helpers for test harness
class Node:
  def __init__(self, key, parent=None):
    self.key = key
    self.parent = parent
    self.left = None
    self.right = None
    self.height = 0

  def __repr__(self):
    return "Node(" + str(self.key) + ")"


class BinarySearchTree:
  def __init__(self):
    self.root = None


def get_height(node):
  if node is None:
    return -1
  return node.height


def update_height(node):
  if node is not None:
    node.height = 1 + max(get_height(node.left), get_height(node.right))


def inorder_walk(node):
  """Return a list of keys visited in an in-order traversal."""
  if node is None:
    return []
  return inorder_walk(node.left) + [node.key] + inorder_walk(node.right)


def verify_bst_invariants(tree):
  """Verify BST ordering and parent-pointer consistency."""
  if tree.root is None:
    return

  require(tree.root.parent is None, "Root node must have parent == None")

  def check_node(node, low, high):
    if node is None:
      return

    require(
      low < node.key < high,
      "BST search invariant violated at key " + str(node.key)
    )

    if node.left is not None:
      require(
        node.left.parent is node,
        "Left child " + str(node.left.key) + " has broken parent pointer to " + str(node.key)
      )
      check_node(node.left, low, node.key)

    if node.right is not None:
      require(
        node.right.parent is node,
        "Right child " + str(node.right.key) + " has broken parent pointer to " + str(node.key)
      )
      check_node(node.right, node.key, high)

  check_node(tree.root, float("-inf"), float("inf"))


# Test suites
def check_heap(max_heapify_down, build_max_heap, heap_sort):
  def heapify_case(values, i, heap_size):
    arr = values.copy()
    result = max_heapify_down(arr, i, heap_size)

    require(result is None, "max_heapify_down must return None")
    require(Counter(arr) == Counter(values), "max_heapify_down lost or changed values")
    require(arr[heap_size:] == values[heap_size:], "Changed elements outside active heap")

    for j in range(heap_size):
      left = 2 * j + 1
      right = 2 * j + 2
      if left < heap_size:
        require(
          arr[j] >= arr[left],
          "Max-heap invariant violated at index " + str(j)
          + " (parent " + str(arr[j]) + " < left child " + str(arr[left]) + ")"
        )
      if right < heap_size:
        require(
          arr[j] >= arr[right],
          "Max-heap invariant violated at index " + str(j)
          + " (parent " + str(arr[j]) + " < right child " + str(arr[right]) + ")"
        )

  def sort_case(values):
    arr = values.copy()
    result = heap_sort(arr)

    require(result is arr, "heap_sort must return the original list object")
    require(arr == sorted(values), "Array not sorted in ascending order")
    require(Counter(arr) == Counter(values), "heap_sort lost or changed values")

  cases = [
    ("Empty heap sift-down", lambda: heapify_case([], 0, 0)),
    ("Single-element sift-down", lambda: heapify_case([10], 0, 1)),
    ("Sift-down left child larger", lambda: heapify_case([4, 10, 2], 0, 3)),
    ("Sift-down right child larger", lambda: heapify_case([4, 2, 10], 0, 3)),
    ("Multi-level sift-down on trace input [4, 10, 8, 5, 1, 2, 7]",
     lambda: heapify_case([4, 10, 8, 5, 1, 2, 7], 0, 7)),
    ("Sift-down preserving suffix outside heap_size",
     lambda: heapify_case([3, 12, 9, 2, 1, 99, 100], 0, 5)),
    ("Ascending Heapsort on empty list", lambda: sort_case([])),
    ("Ascending Heapsort on single element", lambda: sort_case([42])),
    ("Ascending Heapsort on two elements", lambda: sort_case([9, 3])),
    ("Ascending Heapsort on sorted input", lambda: sort_case([1, 2, 3, 4, 5])),
    ("Ascending Heapsort on reverse sorted input", lambda: sort_case([5, 4, 3, 2, 1])),
    ("Ascending Heapsort on duplicates", lambda: sort_case([7, 7, 7, 7])),
    ("Ascending Heapsort on negative values", lambda: sort_case([3, -1, 3, 0, -8, 2])),
    ("Ascending Heapsort on trace input [15, 12, 8, 6, 2, 3, 7]",
     lambda: sort_case([15, 12, 8, 6, 2, 3, 7])),
  ]

  return run_checks(cases)


def check_bst(bst_insert, bst_delete):
  def test_insert_empty():
    tree = BinarySearchTree()
    node = bst_insert(tree, 50)
    require(tree.root is not None, "tree.root must not be None after insert")
    require(tree.root.key == 50, "Inserted key must be 50")
    require(tree.root.parent is None, "Root parent must be None")
    require(node is tree.root, "bst_insert must return the newly inserted node")

  def test_insert_sequence(keys):
    tree = BinarySearchTree()
    for k in keys:
      bst_insert(tree, k)
    verify_bst_invariants(tree)
    require(
      inorder_walk(tree.root) == sorted(keys),
      "In-order traversal must equal sorted keys"
    )

  def test_delete_leaf():
    # Delete leaf node (0 children)
    tree = BinarySearchTree()
    for k in [40, 20, 60, 10, 30]:
      bst_insert(tree, k)
    deleted = bst_delete(tree, 10)
    verify_bst_invariants(tree)
    require(deleted is not None and deleted.key == 10, "Return deleted node")
    require(inorder_walk(tree.root) == [20, 30, 40, 60], "Key 10 must be removed")
    parent_node = tree.root.left  # node 20
    require(parent_node.left is None, "Parent left child must be None after leaf deletion")

  def test_delete_single_child():
    # Delete node with 1 child
    tree = BinarySearchTree()
    for k in [40, 20, 60, 30, 50, 70]:
      bst_insert(tree, k)
    # Node 20 has only right child 30
    deleted = bst_delete(tree, 20)
    verify_bst_invariants(tree)
    require(deleted is not None and deleted.key == 20, "Return deleted node")
    require(inorder_walk(tree.root) == [30, 40, 50, 60, 70], "Key 20 must be removed")
    require(tree.root.left.key == 30, "Child 30 must splice into 20's position")
    require(tree.root.left.parent is tree.root, "Child parent pointer must update to root")

  def test_delete_two_children_immediate_successor():
    # Successor is immediate right child
    tree = BinarySearchTree()
    for k in [40, 20, 60, 50, 70]:
      bst_insert(tree, k)
    deleted = bst_delete(tree, 60)
    verify_bst_invariants(tree)
    require(deleted is not None and deleted.key == 60, "Return deleted node")
    require(inorder_walk(tree.root) == [20, 40, 50, 70], "Key 60 must be removed")

  def test_delete_two_children_deep_successor():
    # Successor is deeper in right subtree
    tree = BinarySearchTree()
    for k in [40, 20, 60, 10, 30, 50, 70]:
      bst_insert(tree, k)
    # Delete root 40; successor is 50 (left child of 60)
    deleted = bst_delete(tree, 40)
    verify_bst_invariants(tree)
    require(deleted is not None and deleted.key == 40, "Return deleted node")
    require(tree.root.key == 50, "Successor 50 must become the new root")
    require(tree.root.parent is None, "New root parent must be None")
    require(inorder_walk(tree.root) == [10, 20, 30, 50, 60, 70], "Tree must maintain sorted in-order")

  def test_delete_all_sequential():
    tree = BinarySearchTree()
    keys = [40, 20, 60, 10, 30, 50, 70]
    for k in keys:
      bst_insert(tree, k)
    delete_order = [10, 20, 40, 30, 60, 50, 70]
    for k in delete_order:
      bst_delete(tree, k)
      verify_bst_invariants(tree)
    require(tree.root is None, "Tree must be empty after deleting all keys")

  cases = [
    ("Insert into empty tree", test_insert_empty),
    ("Insert sorted sequence [10, 20, 30, 40]", lambda: test_insert_sequence([10, 20, 30, 40])),
    ("Insert reverse sequence [40, 30, 20, 10]", lambda: test_insert_sequence([40, 30, 20, 10])),
    ("Insert README trace sequence [40, 20, 60, 10, 30, 50, 70]",
     lambda: test_insert_sequence([40, 20, 60, 10, 30, 50, 70])),
    ("Delete leaf (0-child node)", test_delete_leaf),
    ("Delete node with 1 child", test_delete_single_child),
    ("Delete node with 2 children (immediate successor)", test_delete_two_children_immediate_successor),
    ("Delete root node with 2 children (deep successor)", test_delete_two_children_deep_successor),
    ("Delete all nodes until empty", test_delete_all_sequential),
  ]

  return run_checks(cases)
