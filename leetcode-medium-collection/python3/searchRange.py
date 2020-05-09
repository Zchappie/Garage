from typing import List
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        if not nums:
            return [-1,-1]
        if nums[0] > target or nums[-1] < target:
            return [-1, -1]
        head = 0
        tail = len(nums) - 1
        base1, base2 = -1, -1 #indicator of first and last given element
        while base1 < 0 and base2 < 0:
            ind = int((tail + head)/2)
            if nums[ind] > target:
                tail = ind
            elif nums[ind] < target:
                head = ind
                if head == tail - 1 and nums[tail] == target:
                    return [tail, tail]
                elif head == tail - 1:
                    return [-1, -1]
            else:
                base1, base2 = ind, ind
        
        foundFirst = False
        foundLast = False
        while (not foundFirst) or (not foundLast):
            if not foundFirst:
                indHead = int((base1 + head)/2)
                if nums[indHead] == target:
                    base1 = indHead
                else:
                    head = indHead
                if (head == base1 - 1 and nums[head] != target) or head == base1:
                    foundFirst = True
            if not foundLast:
                indTail = int((base2 + tail)/2)
                if nums[indTail] == target:
                    base2 = indTail
                else:
                    tail = indTail
                if tail == base2 + 1 or tail == base2:
                    if nums[tail] == target:
                        base2 = tail
                    foundLast = True
        return [base1, base2]
            
            
s = Solution()
print(s.searchRange([0,0,0,1,2,3], 0))