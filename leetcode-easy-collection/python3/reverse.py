import typing

class Solution:
    def reverse(self, x: int) -> int:
        string = str(abs(x))
        reversed_str = str(string[::-1])
        neg_reversed = -int(reversed_str)
        if x < 0 and neg_reversed >= -0x80000000:
            return neg_reversed
        elif x >=0 and -neg_reversed < 0x7fffffff:
            return -neg_reversed
        else:
            return 0

    """
    Get the sign, get the reversed absolute integer.
    Return their product if r didn't "overflow".

    IMPORTANT:
    False - True = -1
    False + True = 1
    False * True = 0
    """
    # def reverse(self, x):
    #     s = (x > 0) - (x < 0)
    #     r = int(str(x*s)[::-1])
    #     return s*r * (r < 2**31)

solu = Solution()
print(solu.reverse(1534236469))