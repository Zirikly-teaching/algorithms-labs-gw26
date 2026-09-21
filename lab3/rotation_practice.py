"""Part 4: implement AVL balance factor calculation, single rotations, and double rotations.

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


if __name__ == "__main__":
  from lab_checks import check_rotations
  raise SystemExit(
    check_rotations(
      balance_factor,
      rotate_left,
      rotate_right,
      rotate_left_right,
      rotate_right_left
    )
  )
