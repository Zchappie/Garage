from typing import List
# class Solution:
#     def rotate(self, nums: List[int], k: int) -> None:
#         """
#         Do not return anything, modify nums in-place instead.
#         """
        # # solution 1:
        # for i in range(k):
        #     nums.insert(0, nums.pop(-1))
        
        # # solution 2:
        # nums[:] = nums[-k%len(nums):] + nums[:-k%len(nums)]

# # solution 3:
"""
1. Swap all the elements in nums
2. Now they are backward, the last k in original nums are the first k. Swap them so they are in original order.
3. the last (n-k) in your list can now be reversed so that n[0] -> nums[k] and nums[n-k-1] -> nums[-1]
"""
class Solution:
    def rotate(self, nums, k):
        def numReverse(start, end):
            while start < end:
                nums[start], nums[end] = nums[end], nums[start]
                start += 1
                end -= 1
        k, n = k % len(nums), len(nums)
        if k:
            numReverse(0, n - 1)
            numReverse(0, k - 1)
            numReverse(k, n - 1)

s = Solution()
nums = [1,2,3,4,5,6,7]
k = 9
s.rotate(nums, k)
print(nums)