from typing import List
class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        if n == 0:
            pass
        else:
            nums1[m : m+n] = nums2
            nums1[:m+n] = sorted(nums1[:m+n])

    """
    Without built-in functions like sort.
    """
    def merge(self, nums1, m, nums2, n):
        while m > 0 and n > 0:
            if nums1[m - 1] > nums2[n - 1]:
                nums1[m + n - 1] = nums1[m - 1]
                m -= 1
            else:
                nums1[m + n - 1] = nums2[n - 1]
                n -= 1
        nums1[:n] = nums2[:n]

nums1 = [1,2,3,0,0,0]
m = 3
nums2 = [0]
n = 1

s = Solution()
s.merge(nums1, m, nums2, n)
print(nums1)