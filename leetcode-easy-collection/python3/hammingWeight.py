class Solution:
    def hammingWeight(self, n: int) -> int:
        bit_str = '{0:032b}'.format(n)
        print(bit_str)
        return bit_str.count('1')

s = Solution()
print(s.hammingWeight(486870))