# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def maxDepth(self, root: TreeNode) -> int:
        if not root:
            return 0
        currLevelNode = [root]
        nextLevelNode = []
        level = 1
        while len(nextLevelNode) != 0 or len(currLevelNode) != 0:
            while len(currLevelNode) != 0:
                node = currLevelNode.pop(0)
                if node != None:
                    if node.left != None:
                        nextLevelNode.append(node.left)
                    if node.right != None:
                        nextLevelNode.append(node.right)

            currLevelNode = nextLevelNode
            nextLevelNode = []
            level += 1

        return level-1

    """
    As always, some one-line shxt.
    Use recursive.
    """
    def maxDepth(self, root: TreeNode) -> int:
        if not root:
            return 0
        return 1+max(self.maxDepth(root.left),self.maxDepth(root.right))

n1 = TreeNode(1)
n2 = TreeNode(2)
n3 = TreeNode(2)
n4 = TreeNode(None)
n5 = TreeNode(3)
n6 = TreeNode(None)
n7 = TreeNode(3)

n1.left = n2
n1.right = n3
n2.left = n4
n2.right = n5
n3.left = n6
n3.right = n7
x = None

s = Solution()
print(s.maxDepth(n1))      