from typing import List
class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]

        for i in range(len(nums)):
            if nums[i] in nums[:i] or nums[i] in nums[i+1:]:
                pass
            else:
                return nums[i]

    def singleNumber2(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]
        
        while len(nums) > 1:
            if nums[0] in nums[1:]:
                nums.pop(nums[1:].index(nums[0])+1) 
                nums.pop(0)
            else:
                return nums[0]
        return nums[0]
    
    def singleNumber3(self, nums):
        """
        Do you know what is XOR?
        """
        res = 0
        for num in nums:
            res ^= num
        return res
s = Solution()
print(s.singleNumber3([2,2,1]))
