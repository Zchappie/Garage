# https://leetcode.com/problems/two-sum/
from typing import List
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i in range(len(nums)-1):
            try:
                j = nums.index(target - nums[i], i+1, len(nums))
                return [i,j]
            except ValueError:
                pass

    """
    O(n) solution: store all previous numbers and target-num as pairs in a dictionary.
    For every new number, search in the dictionary.
    """
    # def twoSum(self, nums: List[int], target: int) -> List[int]:
    #     dic = {}
    #     for i in range(len(nums)):
    #         if nums[i] in dic:
    #             return [dic[nums[i]], i]
    #         else:
    #             dic[target - nums[i]] = i

solu = Solution()
print(solu.twoSum([3,2,4], 6))
