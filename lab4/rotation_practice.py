"""Parts 3-4: implement AVL balance factor, rotations, and iterative and recursive AVL insertion.

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
    """Print the full tree with child labels, heights, balance factors, and parents."""
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
  # TODO 3.2A: Return get_height(node.left) - get_height(node.right).
  if node is None:
    return 0
  return get_height(node.left) - get_height(node.right)


def rotate_left(tree, x):
  """Perform a single left rotation around node x.

  Pivots on x's right child y. Updates child pointers, parent pointers,
  tree.root (if x was root), and recalculates heights for x and y.
  """
  # TODO 3.2B: Rewire pointers so y = x.right rises into x's position; update heights of x then y.
  y = x.right
  if y is None:
    return

  x.right = y.left
  if y.left is not None:
    y.left.parent = x
  y.parent = x.parent
  if x.parent is None:
    tree.root = y
  elif x is x.parent.left:
    x.parent.left = y
  else:
    x.parent.right = y
  y.left = x
  x.parent = y
  update_height(x)
  update_height(y)


def rotate_right(tree, y):
  """Perform a single right rotation around node y.

  Pivots on y's left child x. Updates child pointers, parent pointers,
  tree.root (if y was root), and recalculates heights for y and x.
  """
  # TODO 3.2C: Rewire pointers so x = y.left rises into y's position; update heights of y then x.
  x = y.left
  if x is None:
    return

  y.left = x.right
  if x.right is not None:
    x.right.parent = y
  x.parent = y.parent
  if y.parent is None:
    tree.root = x
  elif y is y.parent.left:
    y.parent.left = x
  else:
    y.parent.right = x
  x.right = y
  y.parent = x
  update_height(y)
  update_height(x)


def rotate_left_right(tree, z):
  """Perform a double Left-Right (LR) rotation around node z.

  Rotates left on z's left child, then rotates right on z.
  """
  # TODO 3.2D: Call rotate_left on z.left, then rotate_right on z.
  rotate_left(tree, z.left)
  rotate_right(tree, z)


def rotate_right_left(tree, z):
  """Perform a double Right-Left (RL) rotation around node z.

  Rotates right on z's right child, then rotates left on z.
  """
  # TODO 3.2E: Call rotate_right on z.right, then rotate_left on z.
  rotate_right(tree, z.right)
  rotate_left(tree, z)


def avl_insert_iterative(tree, key):
  """Insert a key iteratively, restore AVL balance, and return its Node."""
  # TODO 4.1A: BST-insert with a loop, then walk parent pointers upward updating heights and rotating at the first unbalanced node.
  parent = None
  current = tree.root
  while current is not None:
    if key == current.key:
      return current
    parent = current
    if key < current.key:
      current = current.left
    else:
      current = current.right

  inserted_node = Node(key, parent)
  if parent is None:
    tree.root = inserted_node
    return inserted_node
  if key < parent.key:
    parent.left = inserted_node
  else:
    parent.right = inserted_node

  current = parent
  while current is not None:
    update_height(current)
    node_balance = balance_factor(current)

    if node_balance > 1:
      if balance_factor(current.left) >= 0:
        rotate_right(tree, current)
      else:
        rotate_left_right(tree, current)
      break
    if node_balance < -1:
      if balance_factor(current.right) <= 0:
        rotate_left(tree, current)
      else:
        rotate_right_left(tree, current)
      break
    current = current.parent

  return inserted_node


def avl_insert_recursive(tree, key):
  """Insert a key recursively, restore AVL balance, and return its Node."""
  # TODO 4.1B: Recurse down to an empty slot; on the way back up, update heights, rotate if unbalanced, and return the subtree root.
  inserted_node = None

  def insert_subtree(node, parent):
    nonlocal inserted_node

    if node is None:
      inserted_node = Node(key, parent)
      return inserted_node

    if key == node.key:
      inserted_node = node
      return node
    if key < node.key:
      node.left = insert_subtree(node.left, node)
    else:
      node.right = insert_subtree(node.right, node)

    update_height(node)
    node_balance = balance_factor(node)

    if node_balance > 1:
      if key < node.left.key:
        rotate_right(tree, node)
      else:
        rotate_left_right(tree, node)
      return node.parent
    if node_balance < -1:
      if key > node.right.key:
        rotate_left(tree, node)
      else:
        rotate_right_left(tree, node)
      return node.parent
    return node

  tree.root = insert_subtree(tree.root, None)
  tree.root.parent = None
  return inserted_node


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
