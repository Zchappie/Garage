# https://leetcode.com/explore/featured/card/top-interview-questions-easy/92/array/727/
from typing import List
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        i = 1
        if len(nums) == i:
            return i
        while i < len(nums):
            if nums[i] in nums[:i]:
                del nums[i]
            else:
                i += 1
        return i

    """
    Use the property of set, to get unique items 
    """
    # def removeDuplicates(self, nums: List[int]) -> int:
    #     nums[:] = sorted(set(nums))
    #     return len(nums)