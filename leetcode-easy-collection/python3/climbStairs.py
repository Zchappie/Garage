class Solution:
    # def climbStairs(self, n: int) -> int:
    #     """
    #     aj+2 = aj+1 + aj
    #     Time out because of the great amount of duplicated calculation.
    #     """

    #     if n <= 2:
    #         return n
    #     return self.climbStairs(n-1) + self.climbStairs(n-2) 

    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n
        
        a2 = 1
        a1 = 2
        ans = 3
        for i in range(3, n):
            a2 = a1
            a1 = ans
            ans = a1 + a2
        return ans

s = Solution()
print(s.climbStairs(8))