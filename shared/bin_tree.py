# encoding: utf-8

import logging

logging.basicConfig(level=logging.DEBUG)

class BTNode(object):
    """A binary tree that grows to the right."""
    def __init__(self, d):
        self.left = None
        self.right = None
        self.d = d


    def is_leaf(self):
        if not self.left and not self.right:
            return True
        return False


    def left_leaf(self):
        return self.left


    def right_leaf(self):
        if self.is_leaf():
            return None
        else:
            return self.right.right_leaf()


    def append(self, d):
        if not self.left:
            self.left = BTNode(d)
        elif not self.right:
            self.right = BTNode(d)
        else:
            self.right.append(d)


    def traverse(self, f):
        self._traverse(self, f)


    @staticmethod
    def _traverse(node, f):
        if node:
            f(node.d)

            logging.debug(node.d)

            BTNode._traverse(node.left, f)
            BTNode._traverse(node.right, f)



if __name__ == '__main__':
    root = BTNode(0)
    for i in range(1, 10):
        root.append(i)

    root.traverse(lambda _: _)

