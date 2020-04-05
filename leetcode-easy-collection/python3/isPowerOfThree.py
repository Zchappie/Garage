class Solution:
    def isPowerOfThree(self, n: int) -> bool:
        if int(str(n)[-1]) not in [1,3,7,9]:
            return False
        
        if n == 1:
            return True
        
        num = 1
        while num < n:
            if num*3 == n:
                return True
            else:
                num *= 3
        return False

    def isPowerOfThree(self, n: int) -> bool:
        """
        Think about math!!! Use your brain!!!
        """
        from math import log10
        # return (n>0 and int(log(n, 3))== log(n, 3))
        # be careful about above code
        # because log(3) is actually slightly larger than its true value due to round off
        # so for log(243, 3) != 5, and log(243, 3) == 4.99999999...
        return (log10(n) / log10(3)) % 1 == 0

    def isPowerOfThree(self, n: int) -> bool:
        return n > 0 and 1162261467 % n == 0