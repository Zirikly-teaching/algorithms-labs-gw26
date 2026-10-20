"""Part 2: implement BST pointer insertion and deletion.

Node structure, search, minimum, and subtree transplant helpers are provided.
"""


class Node:
  """Binary Search Tree node with parent pointer and height."""

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


def bst_search(node, key):
  """Provided: search for node containing key; return Node or None."""
  while node is not None and key != node.key:
    if key < node.key:
      node = node.left
    else:
      node = node.right
  return node


def tree_minimum(node):
  """Provided: return node with minimum key in subtree rooted at node."""
  while node.left is not None:
    node = node.left
  return node


def transplant(tree, u, v):
  """Provided: replace subtree rooted at node u with subtree rooted at node v.

  Updates parent's child pointer and v.parent. Does not update u.left or u.right.
  """
  if u.parent is None:
    tree.root = v
  elif u == u.parent.left:
    u.parent.left = v
  else:
    u.parent.right = v
  if v is not None:
    v.parent = u.parent


def bst_insert(tree, key):
  """Insert key into tree with parent pointers; return the new Node.

  Preconditions: key is comparable and distinct from existing keys in tree.
  Postconditions: tree satisfies BST search invariant; new node has correct parent.
  """
  # TODO 2.3A: Traverse downward to find parent slot, attach Node(key, parent=...), and update tree.root if empty.
  new_node = Node(key)
  parent = None
  current = tree.root
  while current is not None:
    parent = current
    if key < current.key:
      current = current.left
    elif key > current.key:
      current = current.right
    else:
      return current
  new_node.parent = parent
  if parent is None:
    tree.root = new_node
  elif key < parent.key:
    parent.left = new_node
  else:
    parent.right = new_node
  return new_node


def bst_delete(tree, key):
  """Delete key from tree, splicing/replacing nodes; return deleted Node (or None).

  Handles 0-child, 1-child, and 2-child cases using the in-order successor.
  Preserves BST search invariant and all parent pointers.
  """
  # TODO 2.3B: Find target node z; handle 0-child, 1-child, and 2-child cases using transplant and successor.
  deleted_node = bst_search(tree.root, key)
  if deleted_node is None:
    return None

  if deleted_node.left is None:
    transplant(tree, deleted_node, deleted_node.right)
  elif deleted_node.right is None:
    transplant(tree, deleted_node, deleted_node.left)
  else:
    min_node = tree_minimum(deleted_node.right)
    if min_node.parent != deleted_node:
      transplant(tree, min_node, min_node.right)
      min_node.right = deleted_node.right
      min_node.right.parent = min_node

    transplant(tree, deleted_node, min_node)
    min_node.left = deleted_node.left
    min_node.left.parent = min_node

  return deleted_node


if __name__ == "__main__":
  from lab_checks import check_bst
  raise SystemExit(check_bst(bst_insert, bst_delete))
