from typing import List

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        return len(list(set(nums))) < len(nums)

s = Solution()
print(s.containsDuplicate([1,2,3]))