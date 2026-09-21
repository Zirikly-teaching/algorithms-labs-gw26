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


def check_rotations(balance_factor, rotate_left, rotate_right, rotate_left_right, rotate_right_left):
  def test_balance_factor_values():
    node = Node(20)
    require(balance_factor(node) == 0, "Leaf balance factor must be 0")
    require(balance_factor(None) == 0, "None node balance factor must be 0")

    node.left = Node(10, parent=node)
    node.left.height = 0
    node.height = 1
    require(balance_factor(node) == 1, "Left-heavy node balance factor must be 1")

    node.right = Node(30, parent=node)
    node.right.height = 0
    require(balance_factor(node) == 0, "Balanced 2-child node balance factor must be 0")

    node.right.height = 1
    require(balance_factor(node) == -1, "Right-heavy node balance factor must be -1")

  def test_rotate_right_root():
    # LL tree: 30 -> 20 -> 10
    tree = BinarySearchTree()
    n30 = Node(30)
    n20 = Node(20, parent=n30)
    n10 = Node(10, parent=n20)
    n30.left = n20
    n20.left = n10
    n30.height = 2
    n20.height = 1
    n10.height = 0
    tree.root = n30

    rotate_right(tree, n30)

    require(tree.root is n20, "Root must become 20 after right rotation")
    require(n20.parent is None, "New root parent must be None")
    require(n20.left is n10 and n10.parent is n20, "Left child 10 preserved")
    require(n20.right is n30 and n30.parent is n20, "30 becomes right child of 20")
    require(n30.left is None, "30 left child must be None")
    require(n30.height == 0, "Node 30 height updated to 0")
    require(n20.height == 1, "Node 20 height updated to 1")
    require(inorder_walk(tree.root) == [10, 20, 30], "In-order traversal preserved")

  def test_rotate_left_root():
    # RR tree: 10 -> 20 -> 30
    tree = BinarySearchTree()
    n10 = Node(10)
    n20 = Node(20, parent=n10)
    n30 = Node(30, parent=n20)
    n10.right = n20
    n20.right = n30
    n10.height = 2
    n20.height = 1
    n30.height = 0
    tree.root = n10

    rotate_left(tree, n10)

    require(tree.root is n20, "Root must become 20 after left rotation")
    require(n20.parent is None, "New root parent must be None")
    require(n20.left is n10 and n10.parent is n20, "10 becomes left child of 20")
    require(n20.right is n30 and n30.parent is n20, "Right child 30 preserved")
    require(n10.right is None, "10 right child must be None")
    require(n10.height == 0, "Node 10 height updated to 0")
    require(n20.height == 1, "Node 20 height updated to 1")
    require(inorder_walk(tree.root) == [10, 20, 30], "In-order traversal preserved")

  def test_rotate_interior_subtree():
    # Rotate an interior node with a parent
    # Tree: 50 -> left is 30 -> 30.left is 20, 20.left is 10
    tree = BinarySearchTree()
    n50 = Node(50)
    n30 = Node(30, parent=n50)
    n20 = Node(20, parent=n30)
    n10 = Node(10, parent=n20)
    n50.left = n30
    n30.left = n20
    n20.left = n10
    n50.height = 3
    n30.height = 2
    n20.height = 1
    n10.height = 0
    tree.root = n50

    rotate_right(tree, n30)

    require(tree.root is n50, "Tree root must remain 50")
    require(n50.left is n20, "50 left child must update to 20")
    require(n20.parent is n50, "20 parent must update to 50")
    require(n20.right is n30, "20 right child must be 30")
    require(n30.parent is n20, "30 parent must be 20")
    require(inorder_walk(tree.root) == [10, 20, 30, 50], "In-order traversal preserved")

  def test_double_rotation_left_right():
    # LR tree: 30 -> 10 -> 20
    tree = BinarySearchTree()
    n30 = Node(30)
    n10 = Node(10, parent=n30)
    n20 = Node(20, parent=n10)
    n30.left = n10
    n10.right = n20
    n30.height = 2
    n10.height = 1
    n20.height = 0
    tree.root = n30

    rotate_left_right(tree, n30)

    require(tree.root is n20, "Root must become 20 after rotate_left_right")
    require(n20.left is n10 and n10.parent is n20, "10 is left child of 20")
    require(n20.right is n30 and n30.parent is n20, "30 is right child of 20")
    require(inorder_walk(tree.root) == [10, 20, 30], "In-order traversal preserved")

  def test_double_rotation_right_left():
    # RL tree: 10 -> 30 -> 20
    tree = BinarySearchTree()
    n10 = Node(10)
    n30 = Node(30, parent=n10)
    n20 = Node(20, parent=n30)
    n10.right = n30
    n30.left = n20
    n10.height = 2
    n30.height = 1
    n20.height = 0
    tree.root = n10

    rotate_right_left(tree, n10)

    require(tree.root is n20, "Root must become 20 after rotate_right_left")
    require(n20.left is n10 and n10.parent is n20, "10 is left child of 20")
    require(n20.right is n30 and n30.parent is n20, "30 is right child of 20")
    require(inorder_walk(tree.root) == [10, 20, 30], "In-order traversal preserved")

  def demo_degeneration_profiling():
    # Demonstration comparing search depth on degenerate vs balanced BST
    n = 1000
    sorted_keys = list(range(n))
    random_keys = sorted_keys.copy()
    rng = random.Random(3212)
    rng.shuffle(random_keys)

    # We build trees manually for the demo
    deg_tree = BinarySearchTree()
    curr = None
    for k in sorted_keys:
      new_node = Node(k)
      if deg_tree.root is None:
        deg_tree.root = new_node
      else:
        curr.right = new_node
        new_node.parent = curr
      curr = new_node

    # Helper to measure depth
    def search_depth(root, target):
      depth = 0
      curr = root
      while curr is not None and curr.key != target:
        depth += 1
        if target < curr.key:
          curr = curr.left
        else:
          curr = curr.right
      return depth

    target = n - 1
    deg_depth = search_depth(deg_tree.root, target)

    # Build balanced tree by recursive median insertion
    bal_tree = BinarySearchTree()

    def insert_bst(tree, key):
      node = Node(key)
      if tree.root is None:
        tree.root = node
        return
      c = tree.root
      p = None
      while c:
        p = c
        c = c.left if key < c.key else c.right
      node.parent = p
      if key < p.key:
        p.left = node
      else:
        p.right = node

    def build_balanced(arr):
      if not arr:
        return
      mid = len(arr) // 2
      insert_bst(bal_tree, arr[mid])
      build_balanced(arr[:mid])
      build_balanced(arr[mid + 1:])

    build_balanced(sorted_keys)
    bal_depth = search_depth(bal_tree.root, target)

    print(
      "\n  [Demo] Search depth for key " + str(target) + " across " + str(n) + " keys:"
      + "\n         Degenerate (sorted input): " + str(deg_depth) + " comparisons (O(n))"
      + "\n         Balanced (median input):   " + str(bal_depth) + " comparisons (O(log n))"
    )

  cases = [
    ("Balance factor calculation", test_balance_factor_values),
    ("Rotate right on root (LL signature)", test_rotate_right_root),
    ("Rotate left on root (RR signature)", test_rotate_left_root),
    ("Rotate right on interior subtree", test_rotate_interior_subtree),
    ("Double rotation rotate_left_right (LR signature)", test_double_rotation_left_right),
    ("Double rotation rotate_right_left (RL signature)", test_double_rotation_right_left),
    ("Imbalance profiling demonstration", demo_degeneration_profiling),
  ]

  return run_checks(cases)
