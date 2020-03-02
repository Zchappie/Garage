# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        if root.left == None or root.right == None:
            if root.left == None and root.right == None:
                return True
            else: 
                return False
        levelTreeVal = []
        levelTreeNode = [root.left, root.right]
        level = 1
        currNode = root
        while levelTreeNode.count(None) != len(levelTreeNode):
            newLevelNode = []
            for node in levelTreeNode:
                levelTreeVal += [self.helper(node)]
                newLevelNode += self.getNextNode(node)
            if levelTreeVal == levelTreeVal[::-1]:
                level += 1
                levelTreeVal = []
                levelTreeNode = newLevelNode
            else:
                return False
        return True

    def helper(self, x):
        if type(x) == TreeNode:
            return x.val
        else:
            return None

    def getNextNode(self, x):
        if x == None:
            return None
        else: 
            return [x.left, x.right]

    # def isSymmetric(self, root):
    #     if root is None:
    #         return True
    #     stack = [(root.left, root.right)]
    #     while stack:
    #         left, right = stack.pop()
    #         if left is None and right is None:
    #             continue
    #         if left is None or right is None:
    #             return False
    #         if left.val == right.val:
    #             stack.append((left.left, right.right))
    #             stack.append((left.right, right.left))
    #         else:
    #             return False
    #     return True

# [1,2,2,null,3,null,3]
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

s = Solution()
print(s.isSymmetric(n1))