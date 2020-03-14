class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        elementSet = set(nums)
        for i in elementSet:
            if nums.count(i) > int(len(nums)/2):
                return i

    def majorityElement(self, nums: List[int]) -> int:
        """
        More simple one, if one integer has more than half in number,
        then the middle point of the sorted list should be this element.

        This only increase the speed, but not the memory.
        """
        nums.sort()
        return nums[int(len(nums)/2)]