from typing import List
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        zeros = nums.count(0)
        nums += [0]*zeros
        for i in range(zeros):
            nums.pop(nums.index(0))

s = Solution()
nums = [0,1,0,3,12]
s.moveZeroes(nums)
print(nums)