from typing import List
class Solution:
    # def missingNumber(self, nums: List[int]) -> int:
    #     nums.sort()
    #     for i in range(len(nums)):
    #         if nums[i] != i:
    #             return i
    #     return i+1

    def missingNumber(self, nums: List[int]) -> int:
        n = len(nums)
        for i in range(n+1):
            if i in nums:
                pass
            else:
                return i

    def missingNumber(self, nums):
        missing = len(nums)
        for i, num in enumerate(nums):
            missing ^= i ^ num
        return missing

    

"""
Gauss 求和公式的应用真的是没想到！！！太绝了！
"""
    def missingNumber(self, nums):
        expected_sum = len(nums)*(len(nums)+1)//2
        actual_sum = sum(nums)
        return expected_sum - actual_sum