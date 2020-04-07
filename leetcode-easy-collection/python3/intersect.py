from typing import List
class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        inter = []
        while nums1 and nums1:
            i = nums1.pop()
            if i in nums2:
                inter += [i]
                nums2.pop(nums2.index(i))
        return inter