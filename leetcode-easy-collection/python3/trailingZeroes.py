from math import factorial
class Solution:
    def trailingZeroes(self, n: int) -> int:
        return 0 if n == 0 else int(n / 5) + self.trailingZeroes(int(n / 5))


"""
这道题的意思：算出来的数，尾部有几个零！！尾部！尾部！
英语这么坑……
"""

s = Solution()
print(s.trailingZeroes(5))