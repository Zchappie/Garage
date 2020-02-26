class Solution:
    # def mySqrt(self, x: int) -> int:
    #     root = 0
    #     while root*root <= x:
    #         root += 1
    #     return root-1

    def mySqrt(self, x: int) -> int:
        """
        Binary search.
        Many variants using Binary Search, the key difference is the search range. 
        Search range summary:

        [1, Integer.MAX_VALUE](easy but not recommend, since you are not showing the use of your brain)
        [1, x](recommend, no math needed)
        [1, x/2](you need to do math to prove it: x/2 should include the sqrt(x), i.e. (x/2)^2 >= x, then x >= 2. Easy but I prefer to avoid math during interview, and this must be included as the corner case)
        For case 2 and case 3, the point I want to emphasise is how to deal with the corner cases? We need to take care of corner cases by making sure right >= left for [left, right], so:
        2. x >= 1 for [1, x] => so we need to take care of the corner case: x < 1
        3. x/2 >= 1 for [1, x/2]=> x >= 2 => so we need to take care of the corner case: x < 2
        """
        if x == 0:
            return 0
        # elif x < 4:
        #     return 1
        
        head = 1
        end = int(x/2)

        while head != end:
            mid = int((end+head)/2)
            if mid*mid <= x:
                if mid == head:
                    return mid
                head = mid
            else:
                end = mid
        return head

solu = Solution()
print(solu.mySqrt(1))