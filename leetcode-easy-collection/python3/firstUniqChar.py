class Solution:
    def firstUniqChar(self, s: str) -> int:
        sSet = dict.fromkeys(s)
        for element in sSet:
            foundLeft, foundRight = False, False
            i = s.index(element)
            # left
            try:
                s[:i].index(element)
                foundLeft = True
            except ValueError:
                pass
            
            # right
            try:
                s[i+1:].index(element)
                foundRight = True
            except ValueError:
                pass

            if not (foundLeft or foundRight):
                return i
            
        return -1

s = Solution()
print(s.firstUniqChar("loveleetcode"))

"""
Important: set is not order-preserved.
However, dict is well-order-preserve function.
"""