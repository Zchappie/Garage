class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        elementSet = set(nums)
        for i in elementSet:
            if nums.count(i) > int(len(nums)/2):
                return i
                