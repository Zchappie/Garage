class Solution:
    def divide(self, dividend: int, divisor: int) -> int:
        dividendAbs = abs(dividend)
        divisorAbs = abs(divisor)

        counter = 0
        res = divisorAbs
        while res <= dividendAbs:
            res += divisorAbs
            counter += 1
        if (dividend < 0 and divisor >0) or (dividend > 0 and divisor < 0):
            return -counter
        else:
            return counter
            
"""
When dividing, using divisor, 2*divisor, 4*divisor, 8*divisor...
will make the speed faster.
"""
class Solution:
    # @return an integer
    def divide(self, dividend, divisor):
        positive = (dividend < 0) is (divisor < 0)
        dividend, divisor = abs(dividend), abs(divisor)
        res = 0
        while dividend >= divisor:
            temp, i = divisor, 1
            while dividend >= temp:
                dividend -= temp
                res += i
                i <<= 1
                temp <<= 1
        if not positive:
            res = -res
        return min(max(-2147483648, res), 2147483647)

s = Solution()
print(s.divide(-10, 3))