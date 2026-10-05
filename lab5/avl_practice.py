#!/usr/bin/env python3

class Node:
    def __init__(self, key, parent=None):
        self.key = key
        self.left = None
        self.right = None
        self.parent = parent
        self.height = 0


class Tree:
    def __init__(self):
        self.root = None

    def print_tree(self, node=None, prefix="", is_left=None):
        """Pretty-print the tree with heights and balance factors."""
        if node is None:
            node = self.root
        if node is None:
            print("(empty tree)")
            return

        if is_left is None:
            print(f"{node.key} (h={node.height}, bf={balance_factor(node)})")
        else:
            connector = "├── " if is_left else "└── "
            print(f"{prefix}{connector}{node.key} (h={node.height}, bf={balance_factor(node)})")

        if node.left is not None or node.right is not None:
            if node.left is not None:
                self.print_tree(node.left, prefix + ("│   " if is_left else "    "), True)
            else:
                print(f"{prefix}{'│   ' if is_left else '    '}├── (empty)")
            if node.right is not None:
                self.print_tree(node.right, prefix + ("│   " if is_left else "    "), False)
            else:
                print(f"{prefix}{'│   ' if is_left else '    '}└── (empty)")


def update_height(node):
    """Recalculate node's height based on children."""
    if node is None:
        return
    left_h = node.left.height if node.left else -1
    right_h = node.right.height if node.right else -1
    node.height = 1 + max(left_h, right_h)


def balance_factor(node):
    """Return BF(node) = height(left) - height(right)."""
    if node is None:
        return 0
    left_h = node.left.height if node.left else -1
    right_h = node.right.height if node.right else -1
    return left_h - right_h


def tree_search(node, key):
    """Search for key in subtree rooted at node."""
    if node is None:
        return None
    if key == node.key:
        return node
    if key < node.key:
        return tree_search(node.left, key)
    return tree_search(node.right, key)


def tree_minimum(node):
    """Find minimum key in subtree rooted at node."""
    current = node
    while current.left is not None:
        current = current.left
    return current


def transplant(tree, u, v):
    """Replace subtree rooted at u with subtree rooted at v."""
    if u.parent is None:
        tree.root = v
    elif u == u.parent.left:
        u.parent.left = v
    else:
        u.parent.right = v
    if v is not None:
        v.parent = u.parent


def bst_delete(tree, key):
    """
    Delete the node with the given key from the BST.
    Return the deleted node (or None if not found).
    Uses in-order successor for 2-child case.
    """
    z = tree_search(tree.root, key)
    if z is None:
        return None

    if z.left is None:
        transplant(tree, z, z.right)
    elif z.right is None:
        transplant(tree, z, z.left)
    else:
        # Two children: find in-order successor
        y = tree_minimum(z.right)
        if y.parent != z:
            transplant(tree, y, y.right)
            y.right = z.right
            y.right.parent = y
        transplant(tree, z, y)
        y.left = z.left
        y.left.parent = y

    return z


def rotate_left(tree, x):
    """Single left rotation around x."""
    y = x.right
    x.right = y.left
    if y.left is not None:
        y.left.parent = x
    y.parent = x.parent
    if x.parent is None:
        tree.root = y
    elif x == x.parent.left:
        x.parent.left = y
    else:
        x.parent.right = y
    y.left = x
    x.parent = y
    update_height(x)
    update_height(y)


def rotate_right(tree, y):
    """Single right rotation around y."""
    x = y.left
    y.left = x.right
    if x.right is not None:
        x.right.parent = y
    x.parent = y.parent
    if y.parent is None:
        tree.root = x
    elif y == y.parent.left:
        y.parent.left = x
    else:
        y.parent.right = x
    x.right = y
    y.parent = x
    update_height(y)
    update_height(x)


def rotate_left_right(tree, z):
    """Double rotation: left on z.left, then right on z."""
    rotate_left(tree, z.left)
    rotate_right(tree, z)


def rotate_right_left(tree, z):
    """Double rotation: right on z.right, then left on z."""
    rotate_right(tree, z.right)
    rotate_left(tree, z)


def avl_delete(tree, key):
    """
    TODO 3.1: Implement AVL deletion with rebalancing.

    Steps:
    1. Locate the node to delete (z).
    2. If z is a leaf (0 children), remove it and rebalance from z.parent.
    3. If z has 1 child, replace it and rebalance from z.parent.
    4. If z has 2 children:
       a. Find in-order successor y (minimum of z.right).
       b. If y != z.right, remove y and rebalance from y.parent first.
       c. Replace z with y and rebalance from the appropriate node.
    5. Continue rebalancing up to the root.

    Remember:
    - Unlike insertion, deletion may require multiple rotations at different ancestors.
    - Use balance factor signs to determine rotation type (no inserted key available).
    - Continue rebalancing all the way to the root.
    """
    z = tree_search(tree.root, key)
    if z is None:
        return None

    rebalance_from = None

    # Handle deletion cases
    if z.left is None:
        # Case 0 or 1: no left child
        rebalance_from = z.parent
        transplant(tree, z, z.right)
    elif z.right is None:
        # Case 1: no right child
        rebalance_from = z.parent
        transplant(tree, z, z.left)
    else:
        # Case 2: two children
        y = tree_minimum(z.right)
        if y.parent != z:
            # y is not z's immediate right child
            # First, rebalance from y's parent after removing y
            rebalance_from = y.parent
            transplant(tree, y, y.right)
            y.right = z.right
            y.right.parent = y
        else:
            # y is z's immediate right child
            rebalance_from = y
        # Replace z with y
        transplant(tree, z, y)
        y.left = z.left
        y.left.parent = y

    # Rebalance from the affected node up to the root
    current = rebalance_from
    while current is not None:
        update_height(current)
        bf = balance_factor(current)

        if bf > 1:  # Left-heavy
            if balance_factor(current.left) >= 0:
                rotate_right(tree, current)
            else:
                rotate_left_right(tree, current)
        elif bf < -1:  # Right-heavy
            if balance_factor(current.right) <= 0:
                rotate_left(tree, current)
            else:
                rotate_right_left(tree, current)

        current = current.parent

    return z


def inorder_traversal(node):
    """Return in-order traversal of subtree as a list."""
    if node is None:
        return []
    return inorder_traversal(node.left) + [node.key] + inorder_traversal(node.right)


def check_bst_property(node):
    """Verify BST property: all left < node < all right."""
    if node is None:
        return True
    if node.left and tree_search(node.left, node.key) is not None:
        return False
    if node.right and tree_search(node.right, node.key) is not None:
        return False
    return check_bst_property(node.left) and check_bst_property(node.right)


def check_avl_property(node):
    """Verify AVL property: all nodes have |BF| <= 1."""
    if node is None:
        return True
    if abs(balance_factor(node)) > 1:
        return False
    return check_avl_property(node.left) and check_avl_property(node.right)


if __name__ == "__main__":
    # Quick manual test
    tree = Tree()
    keys = [30, 10, 20]
    for k in keys:
        node = Node(k)
        if tree.root is None:
            tree.root = node
        else:
            current = tree.root
            while True:
                if k < current.key:
                    if current.left is None:
                        node.parent = current
                        current.left = node
                        break
                    current = current.left
                else:
                    if current.right is None:
                        node.parent = current
                        current.right = node
                        break
                    current = current.right
            # Simple height update
            current = node.parent
            while current:
                update_height(current)
                current = current.parent

    print("Tree before deletion:")
    tree.print_tree()
    print(f"Inorder: {inorder_traversal(tree.root)}")
    print(f"AVL property satisfied: {check_avl_property(tree.root)}")

    avl_delete(tree, 10)
    print("\nTree after deleting 10:")
    tree.print_tree()
    print(f"Inorder: {inorder_traversal(tree.root)}")
    print(f"AVL property satisfied: {check_avl_property(tree.root)}")
