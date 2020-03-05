from typing import List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> TreeNode:
        if type(nums) == int:
            return TreeNode(nums)
        elif not nums:
            return 

        """
        Idea: find the middle number of the sorted list.
        Divide the sorted list into two sub-lists.
        Recursively, until both sublists are empty.
        """

        root = TreeNode(nums[int((len(nums) - 1)/2)])

        curr = root
        left = nums[:int((len(nums) - 1)/2)]
        right = nums[int((len(nums) + 1)/2):]
        
        curr.left = self.sortedArrayToBST(left)
        curr.right = self.sortedArrayToBST(right)

        # # case left
        # curr = curr.left
        # left = left[:int(len(left) - 1)]
        # right = left[int(len(left) + 1):]

        return root

s = Solution()
print(s.sortedArrayToBST([-10,-3,0,5,9]))      