from typing import List
class Solution:
    """
    This solution could be valid, but exceed the time limit.
    """
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        res = []
        for i in range(len(nums) - 1):
            for j in range(i+1, len(nums)):
                # newList = nums.copy()
                search = -1*(nums[i] + nums[j])
                # newList.pop(j)
                # newList.pop(i)
                if (search in nums[i+1:j] or search in nums[j+1:]) and sorted([nums[i], nums[j], search]) not in res:
                    res += [sorted([nums[i], nums[j], search])]
        return res

class Solution(object):
    """
    Details check here: https://leetcode.com/problems/3sum/discuss/232712/Best-Python-Solution-(Explained)
    """
	def threeSum(self, nums):
		res = []
		nums.sort()
		for i in range(len(nums)-2): #[8]
			if nums[i]>0: break #[7]
			if i>0 and nums[i]==nums[i-1]: continue #[1]

			l, r = i+1, len(nums)-1 #[2]
			while l<r:
				total = nums[i]+nums[l]+nums[r]

				if total<0: #[3]
					l+=1
				elif total>0: #[4]
					r-=1
				else: #[5]
					res.append([nums[i], nums[l], nums[r]])
					while l<r and nums[l]==nums[l+1]: #[6]
						l+=1
					while l<r and nums[r]==nums[r-1]: #[6]
						r-=1
					l+=1
					r-=1
		return res

s = Solution()
print(s.threeSum([-1, 0, 1, 2, -1, -4]))