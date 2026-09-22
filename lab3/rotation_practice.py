"""Parts 4-5: implement AVL rotations plus iterative and recursive insertion.

Node structure, tree container, and height maintenance helpers are provided.
"""


class Node:
  """Binary Search Tree node with parent pointer and height attribute."""

  def __init__(self, key, parent=None):
    self.key = key
    self.parent = parent
    self.left = None
    self.right = None
    self.height = 0

  def __repr__(self):
    return "Node(" + str(self.key) + ")"


class BinarySearchTree:
  """Container holding the root pointer of a Binary Search Tree."""

  def __init__(self):
    self.root = None

  def print_tree(self):
    """Print the full tree with child labels, heights, balance factors, and parents.

    This provided debugging helper reports the values currently stored in the
    nodes. It also marks repeated node references so an accidental pointer cycle
    does not cause infinite recursion.
    """
    if self.root is None:
      print("(empty tree)")
      return

    seen = set()

    def node_summary(node):
      left_height = -1 if node.left is None else node.left.height
      right_height = -1 if node.right is None else node.right.height
      bf = left_height - right_height
      parent_key = "None" if node.parent is None else str(node.parent.key)
      return (
        str(node.key)
        + " [height=" + str(node.height)
        + ", bf=" + str(bf)
        + ", parent=" + parent_key + "]"
      )

    def print_children(node, prefix):
      if node.left is None and node.right is None:
        return

      children = [("L", node.left), ("R", node.right)]
      for index, (direction, child) in enumerate(children):
        is_last = index == len(children) - 1
        connector = "└── " if is_last else "├── "
        child_prefix = prefix + ("    " if is_last else "│   ")

        if child is None:
          print(prefix + connector + direction + ": None")
        elif id(child) in seen:
          print(
            prefix + connector + direction + ": "
            + node_summary(child) + " [cycle or repeated reference]"
          )
        else:
          seen.add(id(child))
          print(prefix + connector + direction + ": " + node_summary(child))
          print_children(child, child_prefix)

    seen.add(id(self.root))
    print(node_summary(self.root))
    print_children(self.root, "")


def get_height(node):
  """Provided: return height of node (-1 for None, 0 for leaf)."""
  if node is None:
    return -1
  return node.height


def update_height(node):
  """Provided: recalculate node's height based on its left and right children."""
  if node is not None:
    node.height = 1 + max(get_height(node.left), get_height(node.right))


def balance_factor(node):
  """Calculate balance factor: height(node.left) - height(node.right).

  Return 0 if node is None.
  """
  # TODO 4.2A: Return get_height(node.left) - get_height(node.right).
  raise NotImplementedError("Complete balance_factor")


def rotate_left(tree, x):
  """Perform a single left rotation around node x.

  Pivots on x's right child y. Updates child pointers, parent pointers,
  tree.root (if x was root), and recalculates heights for x and y.
  """
  # TODO 4.2B: Rewire pointers so y = x.right rises into x's position; update heights of x then y.
  raise NotImplementedError("Complete rotate_left")


def rotate_right(tree, y):
  """Perform a single right rotation around node y.

  Pivots on y's left child x. Updates child pointers, parent pointers,
  tree.root (if y was root), and recalculates heights for y and x.
  """
  # TODO 4.2C: Rewire pointers so x = y.left rises into y's position; update heights of y then x.
  raise NotImplementedError("Complete rotate_right")


def rotate_left_right(tree, z):
  """Perform a double Left-Right (LR) rotation around node z.

  Rotates left on z's left child, then rotates right on z.
  """
  # TODO 4.2D: Call rotate_left on z.left, then rotate_right on z.
  raise NotImplementedError("Complete rotate_left_right")


def rotate_right_left(tree, z):
  """Perform a double Right-Left (RL) rotation around node z.

  Rotates right on z's right child, then rotates left on z.
  """
  # TODO 4.2E: Call rotate_right on z.right, then rotate_left on z.
  raise NotImplementedError("Complete rotate_right_left")


def avl_insert_iterative(tree, key):
  """Insert a distinct key iteratively, rebalance the AVL tree, and return its Node.

  First perform an iterative BST insertion. Then walk upward toward the root,
  updating heights and applying the appropriate LL, RR, LR, or RL rotation.
  Preserve every child and parent pointer, including tree.root.parent == None.
  """
  # TODO 5.1: Insert with a loop, then retrace the parent path and rebalance.
  raise NotImplementedError("Complete avl_insert_iterative")


def avl_insert_recursive(tree, key):
  """Insert a distinct key recursively, rebalance the AVL tree, and return its Node.

  Use a recursive helper that returns the root of the updated subtree. On the
  way back up the call stack, update heights and repair any AVL violation.
  Preserve every child and parent pointer, including tree.root.parent == None.
  """
  # TODO 5.2: Recursively insert, then update and rebalance while unwinding.
  raise NotImplementedError("Complete avl_insert_recursive")


if __name__ == "__main__":
  from lab_checks import check_rotations
  raise SystemExit(
    check_rotations(
      balance_factor,
      rotate_left,
      rotate_right,
      rotate_left_right,
      rotate_right_left,
      avl_insert_iterative,
      avl_insert_recursive
    )
  )
