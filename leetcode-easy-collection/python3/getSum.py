class Solution:
    def getSum(self, a: int, b: int) -> int:
        return sum([a, b])


    """
    Bits manipulation! Thought about it but never considered it as the core point.
    Always remember, python integer doesn't have max value.
    Pre-define 32 bits or 16 bits is needed.
    """
    def getSum(self, a: int, b: int) -> int:     
        mask = 0xFFFFFFFF
        while b != 0:
            carry = ((a & b) << 1) & mask
            a = (a ^ b) & mask
            b = carry
        if a >> 31 == 1:
            a = ~(a ^ mask)
        return a