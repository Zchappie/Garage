class Solution:
    def reverseBits(self, n: int) -> int:
        bit_str = '{0:032b}'.format(n)
        return int(bit_str[::-1], 2)

"""
Reed through the description when meeting something unfamiliar!
Input is an integer, and output is an integer. Not Binary!
"""

s = Solution()
print(s.reverseBits(43261596))