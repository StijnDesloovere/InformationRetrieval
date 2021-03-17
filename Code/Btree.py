# coding=utf-8
from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)
from Code.positional_index import create_positional_index

"""
Btree code taken from: https://gist.github.com/mateor/885eb950df7231f178a5
Edited to support key value pairs 
Extended with a range function
"""

"""
author = Mateor
PYTHON 3.3.5
"""


class BTree(object):
    """A BTree implementation with search and insert functions. Capable of any order t."""

    class Node(object):
        """A simple B-Tree Node."""

        def __init__(self, t):
            self.keys = []
            self.children = []
            self.leaf = True
            # t is the order of the parent B-Tree. Nodes need this value to define max size and splitting.
            self._t = t

        def split(self, parent, key_value):
            """Split a node and reassign keys/children."""
            new_node = self.__class__(self._t)

            mid_point = self.size // 2
            split_value = self.keys[mid_point]
            parent.add_key(split_value)

            # Add keys and children to appropriate nodes
            new_node.children = self.children[mid_point + 1:]
            self.children = self.children[:mid_point + 1]
            new_node.keys = self.keys[mid_point + 1:]
            self.keys = self.keys[:mid_point]

            # If the new_node has children, set it as internal node
            if len(new_node.children) > 0:
                new_node.leaf = False

            parent.children = parent.add_child(new_node)
            if key_value < split_value:
                return self
            else:
                return new_node

        @property
        def _is_full(self):
            return self.size == 2 * self._t - 1

        @property
        def size(self):
            return len(self.keys)

        def add_key(self, value):
            """Add a key to a node. The node will have room for the key by definition."""
            self.keys.append(value)
            self.keys.sort()

        def add_child(self, new_node):
            """
      Add a child to a node. This will sort the node's children, allowing for children
      to be ordered even after middle nodes are split.
      returns: an order list of child nodes
      """
            i = len(self.children) - 1
            while i >= 0 and self.children[i].keys[0] > new_node.keys[0]:
                i -= 1
            return self.children[:i + 1] + [new_node] + self.children[i + 1:]

    def __init__(self, t):
        """
    Create the B-tree. t is the order of the tree. Tree has no keys when created.
    This implementation allows duplicate key values, although that hasn't been checked
    strenuously.
    """
        self._t = t
        if self._t <= 1:
            raise ValueError("B-Tree must have a degree of 2 or more.")
        self.root = self.Node(t)

    def insert(self, key_value):
        """Insert a new key of value key_value into the B-Tree."""
        node = self.root
        # Root is handled explicitly since it requires creating 2 new nodes instead of the usual one.
        if node._is_full:
            new_root = self.Node(self._t)
            new_root.children.append(self.root)
            new_root.leaf = False
            # node is being set to the node containing the ranges we want for key_value insertion.
            node = node.split(new_root, key_value)
            self.root = new_root
        while not node.leaf:
            i = node.size - 1
            while i > 0 and key_value < node.keys[i]:
                i -= 1
            if key_value > node.keys[i]:
                i += 1

            next = node.children[i]
            if next._is_full:
                node = next.split(node, key_value)
            else:
                node = next
        # Since we split all full nodes on the way down, we can simply insert the key_value in the leaf.
        node.add_key(key_value)

    def search(self, key, node=None):
        """Return True if the B-Tree contains a key that matches the value."""
        if node is None:
            node = self.root
        key_terms = list(map(lambda x: x[0], node.keys))
        if key in key_terms:
            index = key_terms.index(key)
            return node.keys[index][1]
        elif node.leaf:
            # If we are in a leaf, there is no more to check.
            return False
        else:
            i = 0
            while i < node.size and key > node.keys[i][0]:
                i += 1
            return self.search(key, node.children[i])

    def print_order(self):
        """Print an level-order representation."""
        this_level = [self.root]
        level = 0
        while this_level:
            next_level = []
            output = ""
            for node in this_level:
                if node.children:
                    next_level.extend(node.children)
                keys = list(map(lambda x: x[0], node.keys))
                output += str(keys) + " "
            print("level " + str(level))
            print(output)
            level = level + 1
            this_level = next_level

    """
    Range function: Own method created to find all values in a certain range 
    """
    def range(self, min_term, max_term, path, result, node=None, return_index=False):
        if node is None:
            node = self.root
        key_terms = list(map(lambda x: x[0], node.keys))
        if node.leaf:
            for idx, key in enumerate(key_terms):
                if min_term <= key < max_term:
                    result[key] = node.keys[idx][1]

            if not path:
                return result
            else:
                previous = path.pop(-1)
                previous_node = previous[0]
                previous_index = previous[1]
                return self.range(min_term, max_term, path, result, previous_node, previous_index)

        # Go down in the tree
        elif return_index is False:
            i = 0
            while i < node.size and min_term > key_terms[i]:
                i += 1
            # Add path to nodes that have potential to have predecessors which fall in range
            if i != node.size and key_terms[i] < max_term:
                path.append((node, i))
            return self.range(min_term, max_term, path, result, node.children[i])
        # Go down in the tree after climbing back a node
        else:
            # Add term to result if it falls within the range
            result[node.keys[return_index][0]] = node.keys[return_index][1]
            i = return_index + 1
            # Add path to nodes that have potential to have predecessors which fall in range
            if i != node.size and key_terms[i] < max_term:
                path.append((node, i))
            return self.range(min_term, max_term, path, result, node.children[i])


def create_btree(dictionary):

    tree_index = BTree(2)

    for term in dictionary:
        tree_index.insert((term, dictionary[term]))

    return tree_index


# Example range(m,n)
# Test_tree = BTree(2)
# Test_tree.insert(("apple", 1))
# Test_tree.insert(("banana", 2))
# Test_tree.insert(("kiwi", 3))
# Test_tree.insert(("melon", 4))
# Test_tree.insert(("mandarin", 5))
# Test_tree.insert(("mammee", 6))
# Test_tree.insert(("mamoncillo", 7))
# Test_tree.insert(("nectarine", 8))
# Test_tree.insert(("neem", 9))
# Test_tree.insert(("nere", 10))
# Test_tree.insert(("cherry", 11))
# Test_tree.insert(("grape", 12))
# Test_tree.insert(("lemon", 13))





