from typing import List

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        """
        Dynamic programming problem.
        Space: O(1)
        Time: O(n)
        """
        if max(nums) <= 0:
            return max(nums)

        max_ending_here = max_so_far = 0
        for x in nums:
            max_ending_here = max(0, max_ending_here + x)
            max_so_far = max(max_so_far, max_ending_here)
        return max_so_far

    """
    Store the best value (subarray sum) in nums. This is BRILLIANT!!!
    """
    # def maxSubArray(self, nums: List[int]) -> int:
    #     for i in range(1, len(nums)):
    #         if nums[i-1] > 0:
    #             nums[i] += nums[i-1]
    #     return max(nums)
solu = Solution()
print(solu.maxSubArray([2, -1, 2]))