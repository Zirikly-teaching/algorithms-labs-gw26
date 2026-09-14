"""
Lab 2: Representing Binary Trees via Arrays
CSCI 3212 - Algorithms

In this module, we explore how binary trees can be stored in contiguous arrays
(lists) rather than linked nodes with left/right object pointers.

Key Concepts:
-------------
1. 0-Based Indexing (Standard Python convention):
   - Root is at index 0
   - Left Child of node at index i:  2 * i + 1
   - Right Child of node at index i: 2 * i + 2
   - Parent of node at index i:      (i - 1) // 2   (for i > 0)

2. 1-Based Indexing (Common in textbooks / algorithms literature):
   - Root is at index 1 (index 0 is unused or None)
   - Left Child of node at index i:  2 * i
   - Right Child of node at index i: 2 * i + 1
   - Parent of node at index i:      i // 2         (for i > 1)

3. Why Arrays for Trees?
   - Zero pointer overhead (saves 16-24 bytes per node in C++/Java/Python).
   - Excellent CPU cache locality: nodes visited in level-order are adjacent in memory.
   - Ideal for Complete Binary Trees (like Binary Heaps).
   - Drawback for sparse/skewed trees: an incomplete tree of height h may require up to 2^h - 1
     array slots, wasting space if many intermediate nodes are empty (None).
"""

from typing import List, Optional, Any
import math


class ArrayBinaryTree:
    """
    Represents a binary tree stored within a flat array (Python list).
    Missing/empty nodes are represented as None.
    """

    def __init__(self, elements: List[Any], zero_indexed: bool = True):
        self.zero_indexed = zero_indexed
        if zero_indexed:
            self.tree = list(elements)
        else:
            # If 1-indexed, place None at index 0 if not already present
            if elements and elements[0] is not None:
                self.tree = [None] + list(elements)
            else:
                self.tree = list(elements)

    def size(self) -> int:
        """Returns the total capacity/length of the underlying array."""
        return len(self.tree)

    def node_count(self) -> int:
        """Counts the number of non-empty (non-None) nodes in the tree."""
        start = 0 if self.zero_indexed else 1
        return sum(1 for x in self.tree[start:] if x is not None)

    # -----------------------------------------------------------------
    # Index Arithmetic
    # -----------------------------------------------------------------

    def left_child_index(self, i: int) -> int:
        """Returns the array index of the left child of node i."""
        if self.zero_indexed:
            return 2 * i + 1
        return 2 * i

    def right_child_index(self, i: int) -> int:
        """Returns the array index of the right child of node i."""
        if self.zero_indexed:
            return 2 * i + 2
        return 2 * i + 1

    def parent_index(self, i: int) -> Optional[int]:
        """Returns the array index of the parent of node i, or None if i is root."""
        if self.zero_indexed:
            if i == 0:
                return None
            return (i - 1) // 2
        else:
            if i <= 1:
                return None
            return i // 2

    # -----------------------------------------------------------------
    # Node Existence & Value Access
    # -----------------------------------------------------------------

    def has_node(self, i: int) -> bool:
        """Checks if a valid, non-None node exists at index i."""
        return 0 <= i < len(self.tree) and self.tree[i] is not None

    def has_left(self, i: int) -> bool:
        return self.has_node(self.left_child_index(i))

    def has_right(self, i: int) -> bool:
        return self.has_node(self.right_child_index(i))

    def has_parent(self, i: int) -> bool:
        p = self.parent_index(i)
        return p is not None and self.has_node(p)

    def get_val(self, i: int) -> Optional[Any]:
        if 0 <= i < len(self.tree):
            return self.tree[i]
        return None

    # -----------------------------------------------------------------
    # Tree Traversals on Array-Backed Trees
    # -----------------------------------------------------------------

    def preorder(self, i: Optional[int] = None) -> List[Any]:
        """Pre-order traversal: Root -> Left -> Right"""
        if i is None:
            i = 0 if self.zero_indexed else 1
        if not self.has_node(i):
            return []
        res = [self.tree[i]]
        res.extend(self.preorder(self.left_child_index(i)))
        res.extend(self.preorder(self.right_child_index(i)))
        return res

    def inorder(self, i: Optional[int] = None) -> List[Any]:
        """In-order traversal: Left -> Root -> Right"""
        if i is None:
            i = 0 if self.zero_indexed else 1
        if not self.has_node(i):
            return []
        res = []
        res.extend(self.inorder(self.left_child_index(i)))
        res.append(self.tree[i])
        res.extend(self.inorder(self.right_child_index(i)))
        return res

    def postorder(self, i: Optional[int] = None) -> List[Any]:
        """Post-order traversal: Left -> Right -> Root"""
        if i is None:
            i = 0 if self.zero_indexed else 1
        if not self.has_node(i):
            return []
        res = []
        res.extend(self.postorder(self.left_child_index(i)))
        res.extend(self.postorder(self.right_child_index(i)))
        res.append(self.tree[i])
        return res

    def level_order(self) -> List[Any]:
        """Level-order traversal: visits nodes level-by-level (left to right)."""
        start = 0 if self.zero_indexed else 1
        return [x for x in self.tree[start:] if x is not None]

    # -----------------------------------------------------------------
    # Tree Properties
    # -----------------------------------------------------------------

    def height(self, i: Optional[int] = None) -> int:
        """Returns height of subtree rooted at i (-1 for empty tree)."""
        if i is None:
            i = 0 if self.zero_indexed else 1
        if not self.has_node(i):
            return -1
        left_h = self.height(self.left_child_index(i))
        right_h = self.height(self.right_child_index(i))
        return 1 + max(left_h, right_h)

    def is_max_heap(self) -> bool:
        """Checks whether the array represents a valid complete Max-Heap."""
        start = 0 if self.zero_indexed else 1
        n = len(self.tree)
        for i in range(start, n):
            if not self.has_node(i):
                continue
            # Left child check
            left = self.left_child_index(i)
            if self.has_node(left) and self.tree[left] > self.tree[i]:
                return False
            # Right child check
            right = self.right_child_index(i)
            if self.has_node(right) and self.tree[right] > self.tree[i]:
                return False
        return True

    # -----------------------------------------------------------------
    # ASCII Visualizer
    # -----------------------------------------------------------------

    def display(self) -> None:
        """Prints a visual ASCII representation of the tree levels."""
        start = 0 if self.zero_indexed else 1
        elements = self.tree[start:]
        if not elements:
            print("(empty tree)")
            return

        h = math.floor(math.log2(len(elements))) + 1 if elements else 0
        print(f"\nArray Representation: {self.tree}")
        print(f"Indexing Scheme:      {'0-based' if self.zero_indexed else '1-based'}")
        print(f"Tree Height:          {self.height()}")
        print(f"Total Nodes:          {self.node_count()}")
        print("-" * 55)

        level = 0
        curr_idx = 0
        while curr_idx < len(elements):
            level_count = 2 ** level
            level_nodes = elements[curr_idx : curr_idx + level_count]
            node_strs = [str(x) if x is not None else "." for x in level_nodes]
            spacing = "   " * max(1, (h - level))
            print(f"Level {level}: {spacing}{' '.join(node_strs)}")
            curr_idx += level_count
            level += 1
        print("-" * 55)


def demonstrate_array_tree():
    print("=" * 65)
    print("DEMO: Array Representation of a Binary Tree (0-based)")
    print("=" * 65)

    # Represents the binary tree:
    #             50
    #          /      \
    #        30        20
    #       /  \      /  \
    #      15  10    8   16
    sample = [50, 30, 20, 15, 10, 8, 16]
    tree = ArrayBinaryTree(sample, zero_indexed=True)
    tree.display()

    print("\nParent-Child Relationship Checks:")
    for idx in range(len(sample)):
        val = sample[idx]
        left_idx = tree.left_child_index(idx)
        right_idx = tree.right_child_index(idx)
        p_idx = tree.parent_index(idx)

        left_val = tree.get_val(left_idx)
        right_val = tree.get_val(right_idx)
        parent_val = tree.get_val(p_idx) if p_idx is not None else "None (Root)"

        print(f"  Index {idx} [val={val}]: parent={parent_val}, left={left_val}, right={right_val}")

    print("\nTree Traversals:")
    print(f"  Pre-order (Root, Left, Right): {tree.preorder()}")
    print(f"  In-order  (Left, Root, Right): {tree.inorder()}")
    print(f"  Post-order(Left, Right, Root): {tree.postorder()}")
    print(f"  Level-order (Breadth-first):  {tree.level_order()}")
    print(f"  Is Valid Max-Heap?            {tree.is_max_heap()}")


if __name__ == "__main__":
    demonstrate_array_tree()
