from typing import List
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if not prices:
            return 0
        elif len(prices) == 1:
            return 0
        
        profit = 0
        for i in range(len(prices)-1):
            profit = max(profit, max(0, max(prices[i+1:]) - prices[i]))
        return profit

s = Solution()
print(s.maxProfit([7,6,4,3,1]))