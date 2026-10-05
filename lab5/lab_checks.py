#!/usr/bin/env python3

import sys
import random
import time
from avl_practice import (
    Tree, Node, avl_delete, inorder_traversal, check_avl_property,
    check_bst_property, balance_factor, rotate_left, rotate_right,
    rotate_left_right, rotate_right_left, update_height, bst_delete,
    tree_search
)


def insert_simple(tree, key):
    """Simple BST insertion (non-AVL)."""
    node = Node(key)
    if tree.root is None:
        tree.root = node
    else:
        current = tree.root
        while True:
            if key < current.key:
                if current.left is None:
                    node.parent = current
                    current.left = node
                    break
                current = current.left
            elif key > current.key:
                if current.right is None:
                    node.parent = current
                    current.right = node
                    break
                current = current.right
            else:
                return None  # Duplicate
        # Update heights up the tree
        current = node.parent
        while current:
            update_height(current)
            current = current.parent
    update_height(tree.root)
    return node


class TestRunner:
    def __init__(self):
        self.passed = []
        self.failed = []

    def test(self, name, condition, message=""):
        if condition:
            self.passed.append(name)
            print(f"✓ {name}")
        else:
            self.failed.append(name)
            print(f"✗ {name}")
            if message:
                print(f"  {message}")

    def summary(self):
        total = len(self.passed) + len(self.failed)
        print(f"\n{'='*60}")
        print(f"Results: {len(self.passed)}/{total} passed")
        if self.failed:
            print(f"Failed: {', '.join(self.failed)}")
            return 1
        return 0


runner = TestRunner()

# Test 1: Simple deletion of leaf
print("Test 1: Delete leaf from tree [30, 10, 20]")
tree = Tree()
for k in [30, 10, 20]:
    insert_simple(tree, k)
deleted = avl_delete(tree, 10)
runner.test(
    "Leaf deletion returns correct node",
    deleted is not None and deleted.key == 10,
    f"Expected node with key 10, got {deleted}"
)
runner.test(
    "Inorder after deletion is [20, 30]",
    inorder_traversal(tree.root) == [20, 30],
    f"Got {inorder_traversal(tree.root)}"
)
runner.test(
    "Tree remains BST",
    check_bst_property(tree.root),
    "BST property violated"
)
runner.test(
    "Tree remains AVL",
    check_avl_property(tree.root),
    "AVL property violated"
)

# Test 2: Deletion with single rotation (LL case)
print("\nTest 2: Delete key that triggers rotation")
tree = Tree()
for k in [20, 10, 30, 5, 15, 25, 35]:
    insert_simple(tree, k)
# Delete 30 and 35 to create imbalance on left
avl_delete(tree, 30)
avl_delete(tree, 35)
inorder = inorder_traversal(tree.root)
runner.test(
    "Inorder after deletions is [5, 10, 15, 20, 25]",
    inorder == [5, 10, 15, 20, 25],
    f"Got {inorder}"
)
runner.test(
    "Tree remains BST after rotations",
    check_bst_property(tree.root),
    "BST property violated"
)
runner.test(
    "Tree remains AVL after rotations",
    check_avl_property(tree.root),
    "AVL property violated"
)

# Test 3: Deletion of node with two children
print("\nTest 3: Delete node with two children")
tree = Tree()
for k in [40, 20, 60, 10, 30, 50, 70]:
    insert_simple(tree, k)
deleted = avl_delete(tree, 20)
runner.test(
    "Two-child deletion returns correct node",
    deleted is not None and deleted.key == 20,
    f"Expected key 20, got {deleted}"
)
inorder = inorder_traversal(tree.root)
runner.test(
    "Inorder after two-child deletion is sorted",
    inorder == sorted(inorder) and 20 not in inorder,
    f"Got {inorder}"
)
runner.test(
    "Tree remains BST",
    check_bst_property(tree.root),
    "BST property violated"
)
runner.test(
    "Tree remains AVL",
    check_avl_property(tree.root),
    "AVL property violated"
)

# Test 4: Deletion of root
print("\nTest 4: Delete root node")
tree = Tree()
for k in [30, 10, 20]:
    insert_simple(tree, k)
deleted = avl_delete(tree, 30)
runner.test(
    "Root deletion returns correct node",
    deleted is not None and deleted.key == 30,
    f"Expected key 30, got {deleted}"
)
inorder = inorder_traversal(tree.root)
runner.test(
    "Inorder after root deletion is [10, 20]",
    inorder == [10, 20],
    f"Got {inorder}"
)
runner.test(
    "Tree remains BST",
    check_bst_property(tree.root),
    "BST property violated"
)
runner.test(
    "Tree remains AVL",
    check_avl_property(tree.root),
    "AVL property violated"
)

# Test 5: Delete non-existent key
print("\nTest 5: Delete non-existent key")
tree = Tree()
for k in [30, 10, 20]:
    insert_simple(tree, k)
deleted = avl_delete(tree, 999)
runner.test(
    "Deleting non-existent key returns None",
    deleted is None,
    f"Expected None, got {deleted}"
)
runner.test(
    "Tree unchanged after failed deletion",
    inorder_traversal(tree.root) == [10, 20, 30],
    f"Got {inorder_traversal(tree.root)}"
)

# Test 6: Delete all keys one by one
print("\nTest 6: Iteratively delete all keys")
tree = Tree()
keys = [50, 25, 75, 12, 37, 62, 87]
for k in keys:
    insert_simple(tree, k)
for k in keys:
    avl_delete(tree, k)
    if tree.root is not None:
        runner.test(
            f"Tree is AVL after deleting {k}",
            check_avl_property(tree.root),
            "AVL property violated"
        )
runner.test(
    "Tree is empty after deleting all keys",
    tree.root is None,
    f"Tree should be empty, but has {inorder_traversal(tree.root)}"
)

# Test 7: Many sequential deletions on a small AVL tree
print("\nTest 7: Sequential deletions from a balanced tree (30 keys)")
tree = Tree()
# Build a balanced tree by inserting in specific order
test_keys = [16, 8, 24, 4, 12, 20, 28, 2, 6, 10, 14, 18, 22, 26, 30, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29]
for k in test_keys:
    insert_simple(tree, k)

initial_inorder = inorder_traversal(tree.root)
runner.test(
    "Initial tree has all 30 keys",
    len(initial_inorder) == 30 and initial_inorder == sorted(test_keys),
    f"Got {len(initial_inorder)} keys: {initial_inorder}"
)

# Delete every 3rd key
delete_keys = set(test_keys[::3])
for k in delete_keys:
    avl_delete(tree, k)

final_inorder = inorder_traversal(tree.root)
expected_keys = sorted([k for k in test_keys if k not in delete_keys])
runner.test(
    "Remaining keys are correct",
    final_inorder == expected_keys,
    f"Expected {expected_keys}, got {final_inorder}"
)
runner.test(
    "Final tree is valid AVL",
    check_avl_property(tree.root),
    f"AVL property violated at some node"
)

# Summary
sys.exit(runner.summary())
