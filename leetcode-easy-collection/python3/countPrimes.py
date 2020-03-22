from math import sqrt
class Solution:
    def countPrimes(self, n: int) -> int:
        if not n:
            return 0

        largest_thr = int(sqrt(n))
        ls_nums = [1 for i in range(n+1)]
        ls_nums[0], ls_nums[1] = 0, 0
        step = 2
        counter = 0
        while step <= largest_thr:
            for j in range(step, len(ls_nums), step):
                ls_nums[j] = 0
            counter += 1
            step = ls_nums.index(1)
        
        if ls_nums[-1] == 1:
            return sum(ls_nums)+counter-1
        else:
            return sum(ls_nums)+counter


s = Solution()
print(s.countPrimes(11))